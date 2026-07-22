from __future__ import annotations

from django.contrib import admin

from .models import AuthorProfile, BlogPost, Comment, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "topic", "status", "created_at")
    list_filter = ("status", "topic", "created_at")
    search_fields = ("title", "content", "author__username")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author_name", "created_at")
    search_fields = ("author_name", "body")
