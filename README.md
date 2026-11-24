# Professional Network — Volume III starter

This is an executable **development prototype**, not a production-ready social network.

## Stack
- Python + Django: backend and business rules
- Django REST Framework: JSON API
- SQLite for local learning; PostgreSQL for staging/production
- Token authentication for a simple API prototype
- Django Admin for trusted staff review

## Run locally
1. Install Python 3.11+.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and replace the secret key.
5. Create database tables: `python manage.py makemigrations network` then `python manage.py migrate`
6. Create an administrator: `python manage.py createsuperuser`
7. Start: `python manage.py runserver`
8. Open `http://127.0.0.1:8000/admin/` for administration.

## First API endpoints
- `POST /api/auth/register/` — create account
- `POST /api/auth/token/` — obtain token
- `GET /api/profiles/` and `GET /api/profiles/<id>/`
- `GET/POST /api/posts/` — read and publish professional posts
- `GET/POST /api/opportunities/` — read and publish opportunities
- `POST /api/reports/` — report an account
- `POST /api/appeals/` — submit an appeal

For authenticated requests, send `Authorization: Token YOUR_TOKEN`.

## Test
Run `python manage.py test`.

## Important gaps before real users
- Email verification, password reset and secure recovery with multiple independent methods
- MFA/passkeys, session/device management, credential stuffing protection
- PostgreSQL configuration, backups, migrations pipeline and object storage
- Moderation queue, staff audit log, two-person review for severe restrictions
- User-facing appeal status, evidence upload, reason codes and human escalation
- Privacy notice, consent, retention/deletion workflows and Rwanda legal review
- Frontend, accessibility, mobile responsiveness, observability and incident response

## Security warnings
- Do not deploy with `DEBUG=True` or the development secret key.
- DRF token authentication is deliberately simple; production should use short-lived, revocable sessions or a mature OAuth/OIDC implementation, MFA/passkeys, rotation and abuse controls.
- The starter returns an API token at registration and has no email verification. Restrict it to local testing.
- `is_verified_professional` must never be self-awarded; require documented criteria and a review/audit trail.
- A report is an allegation, not proof. Restricting an account requires evidence, proportionality, notice, and an appeal route.


## Volume IV — Frontend
The responsive web interface is served by Django at `/`. It uses the same origin as the API, so no separate frontend server or CORS configuration is needed for this prototype.

After migrations, start Django and open `http://127.0.0.1:8000/`.
Available screens: registration/sign-in, professional feed, opportunity board, people directory, reporting and appeals.

The frontend stores the development API token in browser local storage. This is acceptable only for a local prototype. A production app should use secure, HttpOnly, SameSite cookies or a carefully designed OIDC/session architecture, with CSRF protection and token/session revocation.

Not implemented yet: direct/private messaging, profile editing, email verification, password reset, MFA/passkeys, appeal-status tracking, moderation queue, evidence uploads, notifications, search ranking, file/media uploads and production deployment.
