from django.http import HttpResponse
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import uuid
from django.views.decorators.cache import cache_page
from django.template import loader
from django.views.generic import CreateView
from callboard_app.forms import AnnouncementForm, CommentForm, TagForm
from callboard_app.models import Announcement, Comment, Tag
from django.core.cache import DEFAULT_CACHE_ALIAS, caches
import hashlib
from django.utils.encoding import force_bytes, force_text, iri_to_uri


def start_redirect(request):
    return redirect('list/')


def update_cache(url):
    ctx = hashlib.md5()
    url = hashlib.md5(force_bytes(iri_to_uri(url)))
    full_key1 = 'views.decorators.cache.cache_header..' + str(
        url.hexdigest() + '.en-us.UTC')
    full_key2 = 'views.decorators.cache.cache_page..GET.' + str(
        url.hexdigest()) + str(ctx.hexdigest()) + '.en-us.UTC'
    cache.delete(full_key1)
    cache.delete(full_key2)


@cache_page(60 * 60)
def list_of_topic(request):
    template = loader.get_template('list_of_topic.html')
    announcement = Announcement.objects.all()
    announcement_list = {
        "announcement_list": announcement
    }
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
    return HttpResponse(template.render(announcement_data, request))


class AnnouncementEdit(CreateView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        url = 'http://localhost:8000/list/'
        update_cache(url)
    model = Announcement
    form_class = AnnouncementForm
    success_url = '/list'
    template_name = 'announcement_edit.html'


def add_comment(request, slug):
    url = 'http://localhost:8000/post/{}/'.format(slug)
    update_cache(url)
    ann = Announcement.objects.get(slug__iexact=slug)
    Comment.objects.create(text=request.POST['text'], announcement=ann)
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
