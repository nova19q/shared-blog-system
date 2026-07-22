# Shared Blog System

Shared Blog System is a Django + HTMX web application for the SE01 Web Engineering final project. It follows the Exercise 2 proposal by allowing users to write blog posts, browse newest posts, search by title, filter by author/topic/date, and use pagination.

## Project Overview

- UI: server-rendered Django templates with responsive CSS.
- Business logic: post/comment workflow functions in `blog_app/services.py`.
- Database-backed storage: Django models and SQLite for topics, posts, comments, and Django users.
- Forms: Django forms for post creation, comments, and search/filter input.
- Dynamic interaction: HTMX partial updates for search results and comments.
- Deployment: Render-compatible `render.yaml`, WhiteNoise, Gunicorn, and Waitress.

## Setup

Recommended runtime:

- Python 3.11 or newer
- `uv`

Install dependencies:

```bash
python3 -m uv sync
```

Create and apply database migrations:

```bash
python3 -m uv run python manage.py migrate
```

Optionally seed demo content:

```bash
python3 -m uv run python manage.py shell -c "from blog_app.services import seed_demo_content; seed_demo_content()"
```

Run the development server:

```bash
python3 -m uv run python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Main URLs

| URL | Name | Purpose |
| --- | --- | --- |
| `/` | `blog:post_list` | Blog list with search, filters, pagination, and overview metrics |
| `/posts/new/` | `blog:post_create` | POST form for creating a blog post |
| `/posts/<id>/` | `blog:post_detail` | Blog post detail and comments |
| `/posts/<id>/comments/` | `blog:comment_create` | POST form/action for comments |
| `/partials/posts/` | `blog:post_list_partial` | HTMX partial response for post filtering |
| `/seed-demo/` | `blog:seed_demo` | POST action to create demo users, topics, and posts |
| `/healthz/` | `healthz` | Deployment health check |

## Data Model

- Django `User`: built-in authentication user model for blog authors.
- `Topic`: blog topic/category.
- `AuthorProfile`: optional author display profile linked with `OneToOneField`.
- `BlogPost`: post title, content, author, topic, status, and timestamps.
- `Comment`: public comments linked to a blog post.

The schema includes more than two tables, a `ForeignKey`, and a `OneToOneField`.

## Quality Checks

```bash
python3 -m uv run ruff check .
python3 -m uv run python manage.py check
python3 -m uv run pytest
```

## Deployment

Live deployment:

- Application: https://shared-blog-system.onrender.com/
- Health check: https://shared-blog-system.onrender.com/healthz/

Local production-style deployment:

```bash
export DJANGO_DEBUG=0
export DJANGO_SECRET_KEY="replace-this-with-a-secret-key"
export DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost"
python3 -m uv run python manage.py migrate
python3 -m uv run python manage.py collectstatic --noinput
python3 -m uv run waitress-serve --listen=127.0.0.1:8000 blog_site.wsgi:application
```

Render deployment:

- Build command: `pip install -U pip && pip install --force-reinstall . && PYTHONPATH=src python manage.py collectstatic --noinput`
- Start command: `PYTHONPATH=src python manage.py migrate && PYTHONPATH=src gunicorn blog_site.wsgi:application --bind 0.0.0.0:$PORT`
- Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, and `DJANGO_ALLOWED_HOSTS`.

SQLite is used for the course demo. A managed PostgreSQL database would be the next step for long-running production use.

## Course Evidence

- `AGENTS.md`: coding-agent project rules.
- `docs/project-review.md`: rubric and quality review.
- `docs/final-demo-notes.md`: presentation and demo notes.
- `render.yaml`: external deployment configuration.
- `tests/`: Django model, service, view, and HTMX behavior tests.
