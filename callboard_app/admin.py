from django.contrib import admin


# Register your models here.
from callboard_app.models import Announcement, Tag, Comment


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
