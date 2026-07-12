# Deployment Notes for Wealthora

Wealthora currently runs on MySQL via XAMPP for local development. When
you're ready to deploy it live (e.g. to show a working demo link on your
resume/portfolio), here are the realistic options:

## Option A: PythonAnywhere (simplest for MySQL projects)
PythonAnywhere offers a free tier with **MySQL support built in** — no
database swap needed. This is the path of least resistance since your
app is already written against MySQL.

Rough steps:
1. Create a free PythonAnywhere account
2. Upload your code (via git clone or file upload)
3. Create a MySQL database in their dashboard
4. Update your `.env` with PythonAnywhere's MySQL credentials
5. Set `DEBUG = False` and add your PythonAnywhere domain to `ALLOWED_HOSTS`
6. Run `python manage.py collectstatic` and `migrate` on their console
7. Configure the WSGI file to point to `wealthora.wsgi`

## Option B: Render (popular, but requires a database swap)
Render doesn't offer a free MySQL tier — only free PostgreSQL. If you
want to use Render, you'd need to:
1. Swap `mysqlclient` for `psycopg2-binary` in requirements.txt
2. Change `DATABASES['default']['ENGINE']` to `django.db.backends.postgresql`
3. Update `.env` with PostgreSQL connection details instead

This is more work since it touches your database layer, but Render's
deploy experience is generally smoother for Django apps overall.

## Before deploying anywhere (regardless of host)
- [ ] Set `DEBUG = False` in settings (or better: control it via `.env`,
      which we already do — just set `DEBUG=False` in your production `.env`)
- [ ] Set `ALLOWED_HOSTS` to your actual domain
- [ ] Generate a fresh `SECRET_KEY` for production (never reuse your local
      dev one) — you can generate one with:
      `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- [ ] Run `python manage.py collectstatic` so Bootstrap/custom CSS/JS serve correctly
- [ ] Double-check `.env` is in `.gitignore` and was never committed with
      real credentials in your git history

## Recommendation
For a portfolio project, **PythonAnywhere (Option A)** is the lower-effort
path since it avoids a database migration to Postgres. Worth doing once
you're happy with the app's feature set — a live demo link is a strong
addition to a resume, even a simple free-tier one.
