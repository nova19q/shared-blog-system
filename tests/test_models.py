from __future__ import annotations

import pytest
from django.contrib.auth.models import User

from blog_app.models import BlogPost, Comment, Topic


@pytest.mark.django_db
def test_blog_post_absolute_url():
    user = User.objects.create_user(username="masato")
    topic = Topic.objects.create(name="Django", slug="django")
    post = BlogPost.objects.create(
        author=user,
        topic=topic,
        title="First post",
        content="Body",
    )

    assert post.get_absolute_url() == f"/posts/{post.id}/"


@pytest.mark.django_db
def test_comment_belongs_to_post():
    user = User.objects.create_user(username="masato")
    topic = Topic.objects.create(name="Study", slug="study")
    post = BlogPost.objects.create(author=user, topic=topic, title="Notes", content="Body")
    comment = Comment.objects.create(post=post, author_name="Aoi", body="Good post")

    assert list(post.comments.all()) == [comment]
