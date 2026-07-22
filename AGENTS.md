# AGENTS.md

## Project

Shared Blog System is a Django + HTMX web application for the SE01 Web Engineering final project.

## Structure

- `blog_site` - Django settings, URL routing, and deployment configuration
- `blog_app` - models, forms, selectors, services, views, templates, and static files
- `tests` - pytest and Django behavior tests
- `docs` - short project evidence for the course rubric

## Rules

- Keep business workflow logic in `services.py`.
- Keep reusable read/query logic in `selectors.py`.
- Keep views thin and focused on HTTP request/response handling.
- Keep page markup in Django templates and visual styling in static CSS.
- Do not put HTML layout or CSS strings in Python views.
- Add migrations for model changes; do not edit old migrations.

## Checks

Run these before submission:

```bash
python3 -m uv run ruff check .
python3 -m uv run python manage.py check
python3 -m uv run pytest
```
