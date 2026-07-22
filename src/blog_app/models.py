from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="blog_profile")
    display_name = models.CharField(max_length=80)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ["display_name"]

    def __str__(self) -> str:
        return self.display_name


class BlogPost(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name="posts")
    title = models.CharField(max_length=140)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("blog:post_detail", kwargs={"post_id": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    author_name = models.CharField(max_length=80)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self) -> str:
        return f"Comment by {self.author_name}"
