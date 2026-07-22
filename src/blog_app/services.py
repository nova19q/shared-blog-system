from __future__ import annotations

from django.contrib.auth.models import User
from django.db import transaction

from .models import BlogPost, Comment, Topic


@transaction.atomic
def create_post(
    *,
    author: User,
    topic: Topic,
    title: str,
    content: str,
    status: str,
) -> BlogPost:
    return BlogPost.objects.create(
        author=author,
        topic=topic,
        title=title.strip(),
        content=content.strip(),
        status=status,
    )


@transaction.atomic
def create_comment(*, post: BlogPost, author_name: str, body: str) -> Comment:
    return Comment.objects.create(
        post=post,
        author_name=author_name.strip(),
        body=body.strip(),
    )


@transaction.atomic
def seed_demo_content() -> None:
    if User.objects.exists() or Topic.objects.exists() or BlogPost.objects.exists():
        return
    topics = {
        "Django": Topic.objects.create(name="Django", slug="django"),
        "Campus": Topic.objects.create(name="Campus", slug="campus"),
        "Study": Topic.objects.create(name="Study", slug="study"),
    }
    users = [
        User.objects.create_user(username="masato", password="demo-password"),
        User.objects.create_user(username="aoi", password="demo-password"),
        User.objects.create_user(username="ren", password="demo-password"),
        User.objects.create_user(username="mika", password="demo-password"),
        User.objects.create_user(username="sora", password="demo-password"),
    ]
    titles = [
        ("Starting a Django project", "Django"),
        ("My favorite study routine", "Study"),
        ("Useful campus places", "Campus"),
        ("Template tips for beginners", "Django"),
        ("How I review lecture notes", "Study"),
        ("Quiet places between classes", "Campus"),
        ("Using forms for user input", "Django"),
        ("Planning a final presentation", "Study"),
        ("Lunch break recommendations", "Campus"),
        ("Filtering blog posts with HTMX", "Django"),
        ("Weekly learning reflection", "Study"),
        ("Campus event checklist", "Campus"),
        ("Model relationships in Django", "Django"),
        ("Avoiding deadline stress", "Study"),
        ("Library workflow notes", "Campus"),
        ("Pagination for many posts", "Django"),
        ("Building a reading habit", "Study"),
        ("Group work spaces", "Campus"),
        ("Separating services and views", "Django"),
        ("What I learned this week", "Study"),
    ]
    for index, (title, topic_name) in enumerate(titles):
        BlogPost.objects.create(
            author=users[index % len(users)],
            topic=topics[topic_name],
            title=title,
            content=(
                "This demo post is part of the Shared Blog System. It gives "
                "the interface enough data for browsing, filtering, search, "
                "pagination, and code review evidence."
            ),
            status=BlogPost.Status.PUBLISHED,
        )
