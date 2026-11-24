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
The files in this repository form a monolithic Python/Django full-stack application where the frontend and backend meet inside Django's URL routing (urls.py) and views (views.py), communicating over HTTP via a Django REST Framework (DRF) JSON API.
(Note: Individual source files like urls.py and views.py are not directly accessible from this view, so this breakdown is based on the repository's file structure and README architecture.)

1. Where the Codes Meet (The Integration Points)

There are three primary bridges connecting the different files in your project:
• The Web Entry Point (urls.py + views.py \(\leftrightarrow \) index.html + styles.css):
Django serves the frontend directly at the root URL (/). When a user opens http://127.0.0, urls.py routes the request to a view in views.py that renders index.html along with styles.css. Because both run on the same origin, no separate frontend server or CORS setup is required.
• The Data Contract (urls.py + views.py + serializers.py \(\leftrightarrow \) Frontend JavaScript):
The frontend interacts with the backend through REST API endpoints (such as /api/posts/, /api/profiles/, and /api/opportunities/). serializers.py acts as the translator at this boundary—converting Python database objects into JSON for the frontend to display, and validating incoming JSON from the frontend before saving it.
• The Security & Identity Bridge (permissions.py + settings.py \(\leftrightarrow \) Browser localStorage):
When a user logs in via /api/auth/token/, the backend generates an authentication token. The frontend stores this token in the browser's localStorage and attaches it (Authorization: Token YOUR_TOKEN) to future API requests, where permissions.py verifies who the user is before allowing actions.

2. How the Files Collaborate (Request Lifecycle)

When a user interacts with the app (for example, publishing a post or viewing the opportunity board), the files work together in a specific sequence:

A. Application Startup & Configuration

• manage.py & settings.py: manage.py starts the server and loads global settings from settings.py (database configuration, installed apps, DRF token settings, and static file paths for CSS).
• wsgi.py / asgi.py: Act as the server gateway interfaces that pass incoming web traffic into Django.

B. Handling a User Action (Data Flow)

1. Frontend Request (index.html): JavaScript inside index.html sends an HTTP GET or POST request with JSON data and the user's Token header.
2. Routing (urls.py): Matches the requested URL path (e.g., /api/posts/) and forwards it to the corresponding handler in views.py.
3. Authorization (permissions.py): views.py checks permissions.py to confirm the user is authenticated and allowed to perform the action.
4. Validation & Translation (serializers.py): serializers.py validates the incoming data fields (or formats outgoing database records into JSON).
5. Database Operations (models.py): views.py and serializers.py read from or write to the SQLite database using the data schemas defined in models.py (Profiles, Posts, Opportunities, Reports, Appeals).
6. Response (index.html & styles.css): Django returns a JSON response, and the frontend updates the HTML DOM styled by styles.css.

C. Administration & Quality Control

• admin.py: Connects models.py to Django's built-in admin dashboard (/admin/), allowing staff to review reports, appeals, and user profiles.
• tests.py: Imports models.py, views.py, and API routes to simulate requests and verify that all parts collaborate without breaking.

Summary Map


Layer	Files	Role in Collaboration
Presentation	index.html, styles.css	Renders the UI and sends fetch/API calls with the stored auth token.
Routing & Logic	urls.py, views.py, permissions.py	The meeting hub—routes traffic, enforces permissions, and coordinates responses.
Data & Serialization	serializers.py, models.py	Translates JSON \(\leftrightarrow \) Python objects and manages database storage.
Core & Ops	settings.py, manage.py, admin.py, tests.py	Configures the environment, powers staff moderation, and runs automated tests.

If you'd like to trace a specific feature or fix a bug, share the code from urls.py, views.py, or index.html, and I can show you the exact line-by-line connection between them.
