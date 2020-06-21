from django.http import HttpResponse
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
import uuid
import redis
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.cache import cache_page
from django.template import loader
from django.views.generic import CreateView
from callboard_app.forms import AnnouncementForm, CommentForm, TagForm
from callboard_app.models import Announcement, Comment, Tag
from django.core.cache import DEFAULT_CACHE_ALIAS, caches
import hashlib
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text, iri_to_uri
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView
from django.contrib.auth import login, authenticate, logout


def start_redirect(request):
    if request.user.is_authenticated:
        return redirect('/list/')
    return redirect('start/')


def start_page(request):
    return render(request, 'start.html')


class RegisterView(FormView):
    form_class = UserCreationForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        login(self.request,
              authenticate(username=username, password=raw_password))
        return super(RegisterView, self).form_valid(form)


def update_cache(url):
    ctx = hashlib.md5()
    url = hashlib.md5(force_bytes(iri_to_uri(url)))
    full_key1 = 'views.decorators.cache.cache_header..' + str(
        url.hexdigest() + '.en-us.UTC')
    full_key2 = 'views.decorators.cache.cache_page..GET.' + str(
        url.hexdigest()) + '.' + str(ctx.hexdigest()) + '.en-us.UTC'
    cache.delete(full_key1)
    cache.delete(full_key2)


def login_view(request):
    if request.method == 'POST':
        r = redis.Redis()
        r.flushdb()
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(reverse_lazy('list_of_announcement_url'))
    else:
        context = {'form': AuthenticationForm()}
        return render(request, 'login.html', context)


def logout_view(request):
    r = redis.Redis()
    r.flushdb()
    logout(request)
    return HttpResponseRedirect(reverse_lazy('start_page_url'))


@cache_page(60 * 60)
def list_of_topic(request):
    template = loader.get_template('list_of_topic.html')
    announcement = Announcement.objects.all()
    announcement_list = {
        "announcement_list": announcement
    }
    if request.user.is_authenticated:
        announcement_list['username'] = request.user.username
    return HttpResponse(template.render(announcement_list, request))


@cache_page(60 * 60)
def announcement_detail(request, slug):
    template = loader.get_template('announcement.html')
    announcement = Announcement.objects.get(slug__iexact=slug)
    try:
        comments = Comment.objects.filter(announcement__slug=announcement.slug)
    except ObjectDoesNotExist:
        comments = None
    try:
        tags = Tag.objects.filter(announcement__slug=announcement.slug)
    except ObjectDoesNotExist:
        tags = None
    form = CommentForm()
    form2 = TagForm()
    announcement_data = {
        "announcement_data": announcement,
        "comments": comments,
        "tags": tags,
        "form": form,
        "form2": form2,
    }
    if request.user.is_authenticated:
        announcement_data['username'] = request.user.username
    return HttpResponse(template.render(announcement_data, request))


def announcement_edit(request):
    url = 'http://localhost:8000/list/'
    update_cache(url)
    form = AnnouncementForm()
    template = loader.get_template('announcement_edit.html')
    data = {'form': form}
    if request.method == 'GET':
        return HttpResponse(template.render(data, request))
    else:
        Announcement.objects.create(topic=request.POST['topic'], author=request.user, slug=request.POST['slug'],
                                    text_of_announcement=request.POST['text_of_announcement'])
        ann = Announcement.objects.get(slug__iexact=request.POST['slug'])
        try:
            ann.tags.set(request.POST['tags'])
        except MultiValueDictKeyError:
            pass
        return redirect('/list/')


def add_comment(request, slug):
    url = 'http://localhost:8000/post/{}/'.format(slug)
    update_cache(url)
    ann = Announcement.objects.get(slug__iexact=slug)
    Comment.objects.create(text=request.POST['text'], announcement=ann, author_of_comment=request.user)
    return redirect('/post/{}/'.format(slug))


def add_tag(request, slug):
    url = 'http://localhost:8000/post/{}/'.format(slug)
    update_cache(url)
    ann = Announcement.objects.get(slug__iexact=slug)
    try:
        tag = Tag.objects.get(title=request.POST['title'])
    except ObjectDoesNotExist:
        tag = Tag.objects.create(title=request.POST['title'], slug=uuid.uuid4())
    ann.tags.add(tag)
    return redirect('/post/{}/'.format(slug))


def announcement_detail_count(request, slug):
    a = Tag.objects.filter(announcement__slug=slug).count()
    b = Comment.objects.filter(announcement__slug=slug).count()
    return HttpResponse('<h1> Количество тэгов: {} <br> Количество комментариев: {} </h1>'.format(a, b))
