from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from callboard_app.views import *

urlpatterns = [
    path('', start_redirect, name='start_redirect_url'),
    path('list/', list_of_topic, name='list_of_announcement_url'),
    path('post/<slug>/', announcement_detail,
         name='announcement_detail_url'),
    path('create_announcement/', announcement_edit,
         name='create_announcement_url'),
    path('comment/<slug>/', add_comment, name='add_comment_url'),
    path('tag/<slug>/', add_tag, name='add_tag_url'),
    path('post/<slug>/count/', announcement_detail_count,
         name='announcement_detail_count_url'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(
        template_name='register.html',
        success_url=reverse_lazy('list_of_announcement_url')
    ), name='register'),
    path('start/', start_page, name='start_page_url')
]
