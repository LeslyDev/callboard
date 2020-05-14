from django import forms

from callboard_app.models import Announcement, Comment, Tag


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
