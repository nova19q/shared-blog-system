# Project Review

## Reviewed Scope

- Exercise 2 proposal: Shared Blog System
- Django models, forms, services, selectors, views, templates, static CSS, tests, and deployment configuration
- GitHub project management evidence: Issues #1, #2, #3, and #4

## Rubric Alignment

| Rubric item | Evidence |
| --- | --- |
| Tools/AI setup | AGENTS.md, .gitignore, pyproject.toml, uv.lock, render.yaml |
| Managerial practices | Issues #1-#4, this evidence branch, pull request review comments, and linked commits |
| Database schema | Django User, Topic, AuthorProfile, BlogPost, Comment models with relationships |
| Business logic/views | services.py, selectors.py, views.py, named URLs |
| Use of templates | Django templates and static CSS; no page design in Python |
| User input | Post form, comment form, search/filter form, seed demo action |
| Rich interface/HTMX | HTMX post list filtering and comment partial update |
| Tests, specs, documentation | tests/, README.md, AGENTS.md, docs/ |
| Project deployment | Live Render URL, WhiteNoise, Waitress local production, Gunicorn Render hosting, render.yaml |
| Presentation performance | Demo notes and code explanation notes in docs/final-demo-notes.md |

## Tests Run

- python3 -m uv run ruff check .
- python3 -m uv run python manage.py check
- python3 -m uv run pytest

Result: all checks passed, and 9 tests passed.

## Known Limitations

- The app uses simple author selection instead of a full registration/login workflow to keep the course demo focused.
- SQLite is used for the course demo; PostgreSQL is recommended for long-running production use.
- The app is deployed at https://shared-blog-system.onrender.com/.
