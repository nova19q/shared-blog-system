# Final Demo Notes

## Demo Goal

Show that Shared Blog System is a working Django + HTMX web application with database-backed posts, user input, responsive templates, tests, and deployment documentation.

## Demo Flow

1. Open the deployed or local application.
2. Click "Seed demo data" to create demo authors, topics, and posts if needed.
3. Browse newest posts.
4. Search by title.
5. Filter by author or topic.
6. Use pagination.
7. Create a new blog post.
8. Open a post detail page.
9. Add a comment and show the HTMX partial update.
10. Show README deployment instructions and project review evidence.
11. Show GitHub issues, pull request, and review comments as managerial practice evidence.

## Code Areas to Explain

- Database schema: `src/blog_app/models.py`
- Forms: `src/blog_app/forms.py`
- Business logic: `src/blog_app/services.py`
- Query logic: `src/blog_app/selectors.py`
- Views and URLs: `src/blog_app/views.py`, `src/blog_app/urls.py`
- Templates: `src/blog_app/templates/blog_app/`
- Static UI: `src/blog_app/static/blog_app/styles.css`
- Deployment: `src/blog_site/settings.py`, `render.yaml`, `README.md`

## Short Presentation Summary

Shared Blog System is a small blog application. It uses Django models for persistent data, forms for user input, services for workflow logic, templates for HTML rendering, HTMX for partial updates, and WhiteNoise/Waitress/Gunicorn for deployment preparation.
