from django.urls import path

from callboard_app.views import *

urlpatterns = [
    path('', start_redirect, name='start_redirect_url'),
    path('list/', list_of_topic, name='list_of_announcement_url'),
    path('post/<slug>/', announcement_detail,
         name='announcement_detail_url'),
    path('create_announcement/', AnnouncementEdit.as_view(),
         name='create_announcement_url'),
    path('comment/<slug>/', add_comment, name='add_comment_url'),
    path('tag/<slug>/', add_tag, name='add_tag_url'),
    path('post/<slug>/count/', announcement_detail_count,
         name='announcement_detail_count_url'),
]
