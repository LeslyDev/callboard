from django import forms

from callboard_app.models import Announcement, Comment, Tag


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['topic', 'slug', 'text_of_announcement', 'tags']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'author_of_comment']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
