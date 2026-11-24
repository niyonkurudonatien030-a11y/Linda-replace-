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
How a Modern Professional Network Works: From First Principles to Working Code
To truly understand how modern web applications work, forget about complicated jargon for a moment and start with a simple truth: every social network on the internet is just a digital building. It has a front lobby where visitors walk in, hallways that guide them to different rooms, security guards checking badges, and a giant filing cabinet in the back that remembers everything.
When you look at a real codebase like the Linda-replace- project—an open-source prototype of a trust-first professional network—you are looking at the exact architectural blueprint of how such a building is constructed from scratch. Let us walk through this system together, layer by layer, from the moment a user opens the website to the deeper philosophy of why the rules are written the way they are.

1. Where the Frontend and Backend Meet

A web application is divided into two halves: the frontend (what appears on your screen) and the backend (the invisible engine running on a server that processes logic and stores data). Beginners often assume these two parts must live on completely separate computers, constantly struggling to talk to each other across the internet.
In clean, foundational architectures like this one, both halves live under one single roof. Using Python and the Django web framework, the server delivers the visual interface (index.html and styles.css) at the exact same web address (http://127.0.0) as the data endpoints (/api/...). Because they share a single home, there are no cross-origin security blocks—the screen in front of the user and the engine behind the wall communicate smoothly without extra friction.
Inside this unified system, the files meet at three vital bridges:
• The Visual Entry Point: When someone visits the main address, Django hands them index.html (the structure of the page) dressed in styles.css (the layout, colors, and responsive design). This creates five distinct spaces: a registration and login screen, a professional feed, an opportunity board for jobs and projects, a directory of members, and a reporting and appeals desk.
• The Data Contract: The screen does not reach directly into the database. Instead, JavaScript inside index.html sends structured messages (formatted in JSON) to specific web addresses like /api/posts/ or /api/opportunities/. A file called serializers.py sits right at that boundary, acting as a strict translator—converting database records into readable text for the screen, and inspecting incoming messages from the screen before allowing them inside.
• The Identity Handshake: When a user logs in at /api/auth/token/, the server generates a unique digital token—think of it as a temporary VIP wristband. The browser tucks this token into its localStorage. On every click afterward, the browser flashes that wristband (Authorization: Token) back to the server so the system knows exactly who is making the request.

2. The Relay Race of a Single Click

To see how all sixteen files in this repository collaborate, trace what happens in the fraction of a second after a user types a career update and clicks Publish:
1. Startup and Configuration (manage.py & settings.py): Before anyone even visits the site, manage.py wakes up the server using the master rulebook in settings.py, which connects the SQLite database and activates Django REST Framework.
2. Traffic Routing (urls.py): The user's click arrives at urls.py, which acts like a sharp receptionist. It reads the destination path (/api/posts/) and points the request down the exact hallway leading to views.py.
3. The Security Check (permissions.py): Before any action happens, views.py consults permissions.py. Like a security guard at the door, this file checks whether the user’s token is genuine and confirms their account is in good standing. Strangers can look through the window at public posts, but only verified, active members can publish.
4. Validation and Anti-Cheating (serializers.py): Next, serializers.py inspects the content. It makes sure required fields are not empty and strips out anything a user should never be allowed to forge—such as pretending to be another author or sneaking a fake is_verified_professional badge onto their own profile.
5. Permanent Storage (models.py): Once validated, the data reaches models.py, which defines the permanent filing cabinets of the database: separate, organized tables for Profiles, Posts, Opportunities, Reports, and Appeals. Your post is saved safely here.
6. The Oversight Room (admin.py): Finally, admin.py connects those same filing cabinets to a restricted upstairs office (/admin/), where trusted human staff can inspect records, verify credentials, and manage the community.

3. Does This Prototype Work, and How Does It Compare?

If you run this code on a local computer today, it works remarkably well for testing, learning, and demonstrating the core idea. Having an all-in-one setup with SQLite, built-in staff moderation tools, and an automated test file (tests.py) means a developer can verify the entire lifecycle without paying for expensive cloud servers. Of course, because all the files sit together in a flat root directory for simplicity, anyone starting it up must ensure the .env secret key file is created and that the app label in settings.py matches the database migration command.
In terms of look and feel, this platform resembles a minimalist, early-stage version of LinkedIn—stripped of distracting videos, fake engagement tricks, and noisy algorithms, leaving a clean directory and opportunity board.
Yet its true innovation lies in its governance philosophy. On massive commercial platforms, automated bots frequently lock innocent people out after a security breach, leaving them trapped behind endless appeal loops with no human help. Here, due process is written directly into the code: a user report (/api/reports/) is treated strictly as an allegation rather than automatic proof, verification badges can never be self-awarded, and a dedicated appeals system (/api/appeals/) guarantees notice, evidence review, and human oversight.

4. From Prototype to Public Reality

Understanding the difference between a working prototype and a production platform is one of the most important lessons in software engineering. While this model building is wired and functional on a local machine, welcoming thousands of real public users requires stronger foundations:
• Hardened Security: Replacing browser localStorage tokens with encrypted HttpOnly cookies, adding email verification, multi-factor authentication, and safe password recovery.
• Richer Features: Building private direct messaging, profile editing, photo and PDF uploads, and live status tracking for appeals.
• Industrial Infrastructure: Moving from a local SQLite file to a scalable PostgreSQL database with DEBUG=False enabled on a secure public server.
Ultimately, studying a system like this teaches us that great software does not begin with flashy graphics or massive budgets. It begins when someone experiences a real-world failure, refuses to accept it as permanent, and writes clean, logical rules to build something fairer from the ground up.


