from __future__ import annotations

from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list_view, name="post_list"),
    path("posts/new/", views.post_create_view, name="post_create"),
    path("posts/<int:post_id>/", views.post_detail_view, name="post_detail"),
    path("posts/<int:post_id>/comments/", views.comment_create_view, name="comment_create"),
    path("seed-demo/", views.seed_demo_view, name="seed_demo"),
    path("partials/posts/", views.post_list_partial, name="post_list_partial"),
]
