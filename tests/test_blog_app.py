from __future__ import annotations

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from blog_app.models import BlogPost, Comment, Topic
from blog_app.selectors import PostFilters, published_posts
from blog_app.services import create_comment, create_post, seed_demo_content


@pytest.mark.django_db
def test_create_post_service():
    user = User.objects.create_user(username="masato")
    topic = Topic.objects.create(name="Django", slug="django")

    post = create_post(
        author=user,
        topic=topic,
        title="  New post  ",
        content="  Content  ",
        status=BlogPost.Status.PUBLISHED,
    )

    assert post.title == "New post"
    assert post.content == "Content"
    assert post.author == user


@pytest.mark.django_db
def test_create_comment_service():
    user = User.objects.create_user(username="masato")
    topic = Topic.objects.create(name="Django", slug="django")
    post = BlogPost.objects.create(author=user, topic=topic, title="Post", content="Body")

    comment = create_comment(post=post, author_name="  Ren  ", body="  Nice  ")

    assert comment.author_name == "Ren"
    assert comment.body == "Nice"


@pytest.mark.django_db
def test_published_posts_filters_by_title_and_author():
    user = User.objects.create_user(username="masato")
    other = User.objects.create_user(username="aoi")
    topic = Topic.objects.create(name="Django", slug="django")
    matching = BlogPost.objects.create(
        author=user,
        topic=topic,
        title="Django forms",
        content="Body",
    )
    BlogPost.objects.create(author=other, topic=topic, title="Campus notes", content="Body")

    posts = published_posts(PostFilters(query="forms", author_id=user.id))

    assert list(posts) == [matching]


@pytest.mark.django_db
def test_seed_demo_content_is_idempotent():
    seed_demo_content()
    seed_demo_content()

    assert User.objects.count() == 5
    assert Topic.objects.count() == 3
    assert BlogPost.objects.count() == 20


@pytest.mark.django_db
def test_post_list_view(client):
    seed_demo_content()

    response = client.get(reverse("blog:post_list"))

    assert response.status_code == 200
    assert "Shared Blog System" in response.content.decode()


@pytest.mark.django_db
def test_post_create_view(client):
    user = User.objects.create_user(username="masato")
    topic = Topic.objects.create(name="Django", slug="django")

    response = client.post(
        reverse("blog:post_create"),
        {
            "author": user.id,
            "topic": topic.id,
            "title": "Post title",
            "content": "Post content",
            "status": BlogPost.Status.PUBLISHED,
        },
    )

    assert response.status_code == 302
    assert BlogPost.objects.filter(title="Post title").exists()


@pytest.mark.django_db
def test_htmx_comment_create_returns_partial(client):
    user = User.objects.create_user(username="masato")
    topic = Topic.objects.create(name="Django", slug="django")
    post = BlogPost.objects.create(author=user, topic=topic, title="Post", content="Body")

    response = client.post(
        reverse("blog:comment_create", kwargs={"post_id": post.id}),
        {"author_name": "Aoi", "body": "Thanks"},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert Comment.objects.filter(post=post, author_name="Aoi").exists()
    assert "Thanks" in response.content.decode()
