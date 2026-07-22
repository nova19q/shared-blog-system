from __future__ import annotations

from django import forms
from django.contrib.auth.models import User

from .models import BlogPost, Topic


class BlogPostForm(forms.Form):
    author = forms.ModelChoiceField(queryset=User.objects.order_by("username"))
    topic = forms.ModelChoiceField(queryset=Topic.objects.order_by("name"))
    title = forms.CharField(max_length=140)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 8}))
    status = forms.ChoiceField(choices=BlogPost.Status.choices)


class CommentForm(forms.Form):
    author_name = forms.CharField(max_length=80)
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": 4}))


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label="Search title")
    author = forms.ModelChoiceField(
        queryset=User.objects.order_by("username"),
        required=False,
        empty_label="All authors",
    )
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.order_by("name"),
        required=False,
        empty_label="All topics",
    )
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
