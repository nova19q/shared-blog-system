from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from django.contrib.auth.models import User
from django.db.models import Count, QuerySet

from .models import BlogPost, Topic


@dataclass(frozen=True)
class PostFilters:
    query: str = ""
    author_id: int | None = None
    topic_id: int | None = None
    date_from: date | None = None


def published_posts(filters: PostFilters | None = None) -> QuerySet[BlogPost]:
    posts = BlogPost.objects.select_related("author", "topic").filter(
        status=BlogPost.Status.PUBLISHED
    )
    if not filters:
        return posts
    if filters.query:
        posts = posts.filter(title__icontains=filters.query)
    if filters.author_id:
        posts = posts.filter(author_id=filters.author_id)
    if filters.topic_id:
        posts = posts.filter(topic_id=filters.topic_id)
    if filters.date_from:
        posts = posts.filter(created_at__date__gte=filters.date_from)
    return posts


def post_detail(post_id: int) -> BlogPost:
    return BlogPost.objects.select_related("author", "topic").prefetch_related("comments").get(
        pk=post_id
    )


def author_overview() -> QuerySet[User]:
    return User.objects.annotate(post_count=Count("blog_posts")).order_by("username")


def topic_overview() -> QuerySet[Topic]:
    return Topic.objects.annotate(post_count=Count("posts")).order_by("name")
