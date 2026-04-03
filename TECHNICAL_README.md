# Imani Fellowship AGC — Technical README

Developer documentation for the Imani Fellowship AGC church website.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.11+, Flask 3.1 |
| **Database** | PostgreSQL (production), SQLite (dev/testing) |
| **ORM** | Flask-SQLAlchemy + Flask-Migrate (Alembic) |
| **Auth** | Flask-Login (session-based) |
| **Forms** | Flask-WTF (CSRF protection, file uploads) |
| **Frontend** | Bootstrap 5.3, Bootstrap Icons, HTMX |
| **Rich Text** | TinyMCE 6 (cloud-hosted) |
| **Payments** | Safaricom M-Pesa Daraja API (STK Push) |
| **Image Processing** | Pillow |
| **Storage** | Local filesystem or S3/DigitalOcean Spaces |
| **WSGI Server** | Gunicorn |
| **Fonts** | Google Fonts (Inter, Playfair Display) |

## Project Structure

```
Church_website/
├── app/
│   ├── __init__.py              # Application factory (create_app)
│   ├── extensions.py            # db, migrate, login_manager, csrf, mail
│   ├── blueprints/
│   │   ├── main/                # Homepage, about, construction (public)
│   │   ├── auth/                # Login/logout
│   │   ├── admin_panel/         # All admin CRUD routes + forms
│   │   ├── ministries/          # Ministries index, detail, fellowships
│   │   ├── connect/             # Newcomers, connection card, volunteer, services
│   │   ├── media/               # Sermons, gallery, choir
│   │   ├── giving/              # Public giving page
│   │   ├── api/                 # M-Pesa STK push, callback, HTMX status polling
│   │   ├── prayer/              # Prayer request form + prayer wall
│   │   └── events/              # Calendar, event detail
│   ├── models/
│   │   ├── user.py              # User (admin accounts)
│   │   ├── site_setting.py      # Key-value site settings
│   │   ├── announcement.py      # Announcements/news
│   │   ├── event.py             # Events with recurrence
│   │   ├── team_member.py       # Pastoral team, elders, deacons
│   │   ├── page.py              # CMS pages (rich text + image)
│   │   ├── ministry.py          # Ministry + MinistryContent sections
│   │   ├── fellowship.py        # Fellowship groups
│   │   ├── connection_card.py   # Newcomer connection cards
│   │   ├── volunteer.py         # Volunteer sign-ups
│   │   ├── sermon.py            # Sermons/devotionals with embed URLs
│   │   ├── media.py             # Gallery media items
│   │   ├── giving.py            # GivingCategory + Donation records
│   │   ├── prayer_request.py    # Prayer requests
│   │   └── construction.py      # ConstructionUpdate + FundraisingGroup
│   ├── services/
│   │   ├── uploads.py           # save_image / delete_image (local + S3)
│   │   └── mpesa.py             # Daraja OAuth, STK Push, callback handler
│   ├── static/
│   │   ├── css/custom.css       # All custom styles
│   │   ├── img/                 # Static images (logo, hero, construction)
│   │   └── uploads/             # User-uploaded files (gitignored)
│   └── templates/
│       ├── base.html            # Master layout (navbar, offcanvas, footer)
│       ├── admin/
│       │   ├── base.html        # Admin layout with sidebar
│       │   ├── dashboard.html
│       │   ├── announcements/   # list.html, form.html
│       │   ├── events/          # list.html, form.html
│       │   ├── team/            # list.html, form.html
│       │   ├── pages/           # list.html, form.html
│       │   ├── ministries/      # list.html, form.html, content_form.html
│       │   ├── fellowships/     # list.html, form.html
│       │   ├── sermons/         # list.html, form.html
│       │   ├── gallery/         # list.html, form.html
│       │   ├── giving/          # categories.html, category_form.html, donations.html
│       │   ├── prayer_requests/ # list.html, detail.html
│       │   └── construction/    # dashboard.html, update_form.html, group_form.html
│       ├── main/                # home.html, about.html, construction.html
│       ├── auth/                # login.html
│       ├── ministries/          # index.html, detail.html
│       ├── fellowships/         # index.html
│       ├── connect/             # newcomers.html, connection_card.html, volunteer.html, services.html
│       ├── sermons/             # index.html, detail.html, _cards.html (HTMX partial)
│       ├── gallery/             # index.html, choir.html
│       ├── giving/              # index.html
│       ├── prayer/              # index.html
│       └── events/              # index.html, _calendar.html (HTMX partial), detail.html
├── migrations/                  # Alembic migration versions
├── config.py                    # Config classes (Dev, Prod, Testing)
├── requirements.txt
├── .env                         # Environment variables (gitignored)
└── run.py                       # Entry point: python run.py
```

## Setup & Installation

### Prerequisites

- Python 3.11+
- PostgreSQL (for production) or SQLite (auto-created for development)
- A TinyMCE API key (free at [tiny.cloud](https://www.tiny.cloud/))
- Safaricom Daraja API credentials (for M-Pesa integration)

### 1. Clone and install

```bash
git clone https://github.com/CaptainBett/Imani-Fellowship-AGC-Bomet-Website.git
cd Imani-Fellowship-AGC-Bomet-Website
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the project root:

```env
# Flask
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Database (PostgreSQL for prod, omit for SQLite dev fallback)
DATABASE_URL=postgresql://user:pass@localhost:5432/imani_fellowship

# TinyMCE (rich text editor)
TINYMCE_API_KEY=your-tinymce-api-key

# M-Pesa Daraja
MPESA_CONSUMER_KEY=your-consumer-key
MPESA_CONSUMER_SECRET=your-consumer-secret
MPESA_SHORTCODE=your-shortcode
MPESA_PASSKEY=your-passkey
MPESA_ENV=sandbox          # or "production"
MPESA_CALLBACK_URL=https://yourdomain.com/api/mpesa/callback

# Optional: Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Optional: S3/Spaces for file uploads
UPLOAD_STORAGE=local       # or "s3"
S3_BUCKET=your-bucket
S3_REGION=your-region
S3_ENDPOINT=https://your-endpoint
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key
```

### 3. Initialize database

```bash
flask db upgrade
```

### 4. Create admin user

```bash
flask shell
>>> from app.extensions import db
>>> from app.models.user import User
>>> admin = User(username='admin', email='admin@church.co.ke')
>>> admin.set_password('your-secure-password')
>>> db.session.add(admin)
>>> db.session.commit()
>>> exit()
```

### 5. Run

```bash
# Development
python run.py

# Production
gunicorn "app:create_app('production')" --bind 0.0.0.0:8000 --workers 4
```

The app will be available at `http://localhost:5000` (dev) or `http://localhost:8000` (gunicorn).

## Architecture

### Application Factory

`app/__init__.py` uses Flask's application factory pattern (`create_app`). Config is selected by the `FLASK_ENV` environment variable or passed as a parameter. All extensions are initialized with `init_app()`, blueprints are registered, and a context processor injects global template variables (site settings, current datetime).

### Blueprints

| Blueprint | URL Prefix | Purpose |
|-----------|-----------|---------|
| `main` | `/` | Homepage, about, construction |
| `auth` | `/auth` | Login/logout |
| `admin_panel` | `/admin` | All admin CRUD (protected by `@login_required`) |
| `ministries` | `/` | Ministry listing, detail, fellowships |
| `connect` | `/` | Newcomers, connection card, volunteer, services |
| `media` | `/` | Sermons, gallery, choir |
| `giving` | `/` | Public giving page |
| `api` | `/api` | M-Pesa STK Push, callback (CSRF-exempt), status polling |
| `prayer` | `/` | Prayer request form + wall |
| `events` | `/` | Calendar, event detail |

### HTMX Usage

The site uses HTMX for interactive features without heavy JavaScript:

- **Sermon load-more** — Infinite scroll on `/sermons`, loads `_cards.html` partial
- **Calendar navigation** — Month arrows swap `_calendar.html` partial via `hx-get`
- **M-Pesa payment polling** — After STK push, polls `/api/mpesa/status/<id>` every 3 seconds
- **Form submissions** — Connection card, volunteer, and prayer request forms submit via HTMX and show inline success/error messages

HTMX requests are detected server-side via `request.headers.get('HX-Request')`.

### M-Pesa Integration

`app/services/mpesa.py` implements the full Safaricom Daraja flow:

1. **OAuth** — Fetches access token from Daraja API (cached until expiry)
2. **STK Push** — Sends a payment prompt to the donor's phone via `POST /api/mpesa/stk-push`
3. **Callback** — Safaricom sends payment result to `POST /api/mpesa/callback` (CSRF-exempt)
4. **Status polling** — Frontend polls `GET /api/mpesa/status/<checkout_id>` via HTMX

Phone numbers are normalized to `254XXXXXXXXX` format. The callback URL must be publicly accessible (use ngrok for testing).

### Image Uploads

`app/services/uploads.py` handles file uploads:

- **Local storage** — Saves to `app/static/uploads/<category>/` with UUID filenames
- **S3 storage** — Uploads to configured S3/Spaces bucket (when `UPLOAD_STORAGE=s3`)
- Images are resized to max 1200px width using Pillow to save bandwidth
- Supported formats: JPG, JPEG, PNG, WebP, GIF

### Models

All models use Flask-SQLAlchemy with Alembic migrations. Key relationships:

- `Ministry` has many `MinistryContent` sections (one-to-many)
- `Ministry` has many `TeamMember` (via category)
- `GivingCategory` has many `Donation` records
- `User` has many `Page` edits (via `updated_by`)
- `ConstructionUpdate` and `FundraisingGroup` are independent top-level models

## Database Migrations

```bash
# After model changes
flask db migrate -m "description of change"
flask db upgrade

# Rollback
flask db downgrade
```

**Note:** SQLite does not support `ALTER TABLE DROP COLUMN`. If a migration fails on SQLite, delete the `instance/` database file and re-run all migrations with `flask db upgrade`.

## Key Routes Reference

### Public Routes

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Homepage |
| GET | `/about` | About page |
| GET | `/construction` | Construction progress + fundraising |
| GET | `/ministries` | Ministry listing |
| GET | `/ministries/<slug>` | Ministry detail |
| GET | `/fellowships` | Fellowship groups |
| GET | `/sermons` | Sermon archive |
| GET | `/sermons/<slug>` | Sermon detail |
| GET | `/gallery` | Photo gallery |
| GET | `/choir` | Choir page |
| GET | `/events` | Events calendar |
| GET | `/events/<id>` | Event detail |
| GET | `/give` | M-Pesa giving page |
| GET/POST | `/prayer` | Prayer request form + wall |
| GET | `/newcomers` | Welcome page |
| GET/POST | `/connect` | Connection card form |
| GET/POST | `/volunteer` | Volunteer sign-up |
| GET | `/services` | Services & facilities |

### API Routes

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/mpesa/stk-push` | Initiate M-Pesa STK Push |
| POST | `/api/mpesa/callback` | M-Pesa payment callback (CSRF-exempt) |
| GET | `/api/mpesa/status/<id>` | Poll payment status (HTMX) |

### Admin Routes

All admin routes are prefixed with `/admin/` and require `@login_required`. CRUD follows a consistent pattern:

```
GET    /admin/<resource>                    # List
GET    /admin/<resource>/create             # Create form
POST   /admin/<resource>/create             # Create submit
GET    /admin/<resource>/<id>/edit           # Edit form
POST   /admin/<resource>/<id>/edit           # Edit submit
POST   /admin/<resource>/<id>/delete         # Delete
```

Resources: `announcements`, `events`, `team`, `pages`, `ministries`, `fellowships`, `sermons`, `gallery`, `giving/categories`, `construction/updates`, `construction/groups`, `prayer-requests`, `connection-cards`, `volunteers`.

## Testing

```bash
# Run with testing config (in-memory SQLite, CSRF disabled)
FLASK_ENV=testing python -m pytest

# Or run individual test scripts
PYTHONPATH=. python tests/test_phase3.py
PYTHONPATH=. python tests/test_phase4.py
```

The testing config uses `sqlite:///:memory:` and disables CSRF for easier form testing. Always call `db.create_all()` within the app context before seeding test data.

## Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure PostgreSQL `DATABASE_URL`
- [ ] Run `flask db upgrade`
- [ ] Create admin user via `flask shell`
- [ ] Set `MPESA_ENV=production` with live Daraja credentials
- [ ] Set `MPESA_CALLBACK_URL` to your public domain
- [ ] Configure S3/Spaces for file uploads (recommended) or ensure persistent disk for local uploads
- [ ] Serve behind Nginx/Caddy as reverse proxy
- [ ] Enable HTTPS (required for M-Pesa callbacks)
- [ ] Set up log rotation for Gunicorn

### Gunicorn + Nginx

```bash
gunicorn "app:create_app('production')" \
    --bind 127.0.0.1:8000 \
    --workers 4 \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log
```

Nginx config:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    client_max_body_size 16M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/Church_website/app/static/;
        expires 30d;
    }
}
```

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Flask session secret |
| `FLASK_ENV` | No | `development` (default), `production`, `testing` |
| `DATABASE_URL` | Yes (prod) | PostgreSQL connection string |
| `TINYMCE_API_KEY` | Yes | TinyMCE cloud API key |
| `MPESA_CONSUMER_KEY` | Yes | Daraja consumer key |
| `MPESA_CONSUMER_SECRET` | Yes | Daraja consumer secret |
| `MPESA_SHORTCODE` | Yes | M-Pesa till/paybill number |
| `MPESA_PASSKEY` | Yes | Daraja passkey |
| `MPESA_ENV` | No | `sandbox` (default) or `production` |
| `MPESA_CALLBACK_URL` | Yes (prod) | Public URL for M-Pesa callbacks |
| `UPLOAD_STORAGE` | No | `local` (default) or `s3` |
| `S3_BUCKET` | If S3 | S3 bucket name |
| `S3_REGION` | If S3 | S3 region |
| `S3_ENDPOINT` | If S3 | S3-compatible endpoint URL |
| `S3_ACCESS_KEY` | If S3 | S3 access key |
| `S3_SECRET_KEY` | If S3 | S3 secret key |
| `MAIL_SERVER` | No | SMTP server |
| `MAIL_PORT` | No | SMTP port (default 587) |
| `MAIL_USERNAME` | No | SMTP username |
| `MAIL_PASSWORD` | No | SMTP password |
| `MAX_CONTENT_LENGTH` | No | Max upload size in bytes (default 16MB) |
