from __future__ import annotations

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BlogPostForm, CommentForm, SearchForm
from .models import BlogPost
from .selectors import PostFilters, author_overview, published_posts, topic_overview
from .services import create_comment, create_post, seed_demo_content


def _filters_from_request(request: HttpRequest) -> PostFilters:
    form = SearchForm(request.GET or None)
    if not form.is_valid():
        return PostFilters()
    return PostFilters(
        query=form.cleaned_data.get("q") or "",
        author_id=form.cleaned_data["author"].id if form.cleaned_data.get("author") else None,
        topic_id=form.cleaned_data["topic"].id if form.cleaned_data.get("topic") else None,
        date_from=form.cleaned_data.get("date_from"),
    )


def _posts_page(request: HttpRequest):
    posts = published_posts(_filters_from_request(request))
    paginator = Paginator(posts, 6)
    return paginator.get_page(request.GET.get("page"))


def post_list_view(request: HttpRequest) -> HttpResponse:
    posts = published_posts(_filters_from_request(request))
    context = {
        "form": SearchForm(request.GET or None),
        "page_obj": _posts_page(request),
        "authors": author_overview(),
        "topics": topic_overview(),
        "total_posts": posts.count(),
        "comment_count": BlogPost.objects.aggregate(total=Count("comments"))["total"],
    }
    return render(request, "blog_app/post_list.html", context)


def post_list_partial(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "blog_app/partials/post_results.html",
        {"page_obj": _posts_page(request)},
    )


def post_create_view(request: HttpRequest) -> HttpResponse:
    form = BlogPostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = create_post(**form.cleaned_data)
        messages.success(request, "Blog post created.")
        return redirect(post)
    return render(request, "blog_app/post_form.html", {"form": form})


def post_detail_view(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(
        BlogPost.objects.select_related("author", "topic").prefetch_related("comments"),
        pk=post_id,
    )
    return render(request, "blog_app/post_detail.html", {"post": post, "form": CommentForm()})


def comment_create_view(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(BlogPost, pk=post_id)
    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        create_comment(post=post, **form.cleaned_data)
        messages.success(request, "Comment added.")
        if request.htmx:
            post = BlogPost.objects.prefetch_related("comments").get(pk=post.pk)
            return render(request, "blog_app/partials/comment_list.html", {"post": post})
        return redirect(post)
    return render(request, "blog_app/post_detail.html", {"post": post, "form": form})


def seed_demo_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        seed_demo_content()
        messages.success(request, "Demo blog data is ready.")
    return redirect("blog:post_list")
