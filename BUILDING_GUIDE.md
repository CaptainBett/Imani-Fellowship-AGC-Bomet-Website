# Imani Fellowship AGC, Bomet — Website Building Guide

## Overview

A full-featured church website for Imani Fellowship AGC in Bomet, Kenya. Built with Flask + PostgreSQL, designed mobile-first for the Kenyan audience with M-Pesa integration as the primary payment method.

---

## Tech Stack

- **Backend:** Python Flask (Application Factory pattern with Blueprints)
- **Database:** PostgreSQL with Flask-SQLAlchemy ORM + Flask-Migrate
- **Frontend:** HTML/CSS (Bootstrap 5) + HTMX for dynamic interactions
- **Rich Text Editor:** TinyMCE (free tier) for admin content editing
- **Payments:** M-Pesa Daraja API (STK Push), Flutterwave (cards, future)
- **Auth:** Flask-Login (session-based, admin-only)
- **File Storage:** Local filesystem (dev), DigitalOcean Spaces (prod)
- **Hosting:** DigitalOcean Droplet + Nginx + Gunicorn + Let's Encrypt SSL
- **Video:** YouTube/Vimeo embeds (not self-hosted)

---

## Project Structure

```
Church_website/
├── run.py                          # Entry point: from app import create_app
├── config.py                       # Config classes (Dev, Prod, Test)
├── requirements.txt
├── .env                            # Secrets (never committed)
├── .env.example                    # Template for .env
├── .gitignore
├── migrations/                     # Flask-Migrate (Alembic)
│
├── app/
│   ├── __init__.py                 # create_app() factory
│   ├── extensions.py               # db, migrate, login_manager, mail, csrf
│   │
│   ├── models/
│   │   ├── __init__.py             # Import all models
│   │   ├── user.py                 # Admin users
│   │   ├── page.py                 # Editable static pages
│   │   ├── announcement.py         # Announcements / blog posts
│   │   ├── event.py                # Calendar events
│   │   ├── ministry.py             # Ministries + sub-content
│   │   ├── fellowship.py           # Fellowships
│   │   ├── team_member.py          # Pastoral team, choir members
│   │   ├── sermon.py               # Sermons, devotionals, notes
│   │   ├── media.py                # Photos, gallery, uploaded files
│   │   ├── prayer_request.py       # Prayer requests
│   │   ├── construction.py         # Construction progress + fundraising groups
│   │   ├── giving.py               # Donation records + categories
│   │   ├── connection_card.py      # Newcomer connection cards
│   │   └── volunteer.py            # Volunteer sign-ups
│   │
│   ├── blueprints/
│   │   ├── main/                   # Home, about, static pages
│   │   ├── auth/                   # Admin login/logout
│   │   ├── admin_panel/            # Custom CMS admin panel
│   │   ├── ministries/             # Ministry pages
│   │   ├── events/                 # Calendar & events
│   │   ├── giving/                 # Giving page + M-Pesa
│   │   ├── media/                  # Sermons, gallery, choir
│   │   ├── prayer/                 # Prayer requests
│   │   ├── connect/                # Newcomers, volunteer sign-up
│   │   ├── construction/           # Church building progress
│   │   └── api/                    # HTMX targets, M-Pesa callbacks
│   │
│   ├── services/
│   │   ├── mpesa.py                # Daraja API integration
│   │   ├── email.py                # Email notifications
│   │   └── uploads.py              # File upload + Pillow resize
│   │
│   ├── templates/
│   │   ├── base.html               # Master layout
│   │   ├── admin/                  # Admin panel templates
│   │   ├── main/                   # Home, about, services
│   │   ├── ministries/             # Ministry listing + detail
│   │   ├── events/                 # Calendar + event detail
│   │   ├── giving/                 # Giving page + M-Pesa status
│   │   ├── media/                  # Sermons, gallery, choir
│   │   ├── prayer/                 # Prayer request form
│   │   ├── connect/                # Newcomers, volunteer, connection card
│   │   ├── construction/           # Construction progress
│   │   ├── announcements/          # Announcement listing + detail
│   │   ├── devotionals/            # Devotional listing + detail
│   │   └── partials/               # HTMX fragments
│   │
│   └── static/
│       ├── css/custom.css          # Custom styles on top of Bootstrap
│       ├── js/app.js               # Minimal custom JS
│       ├── img/                    # Static images (logo, icons)
│       └── uploads/                # User uploads (dev only)
│
├── scripts/
│   ├── seed_db.py                  # Initial data seeding
│   └── create_admin.py             # CLI to create first admin user
│
└── tests/
```

---

## Database Schema

### users
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| email | VARCHAR(120) UNIQUE | |
| password_hash | VARCHAR(256) | werkzeug pbkdf2:sha256 |
| display_name | VARCHAR(100) | |
| role | VARCHAR(20) | 'admin', 'editor', 'viewer' |
| is_active | BOOLEAN | DEFAULT TRUE |
| created_at | TIMESTAMP | |

### pages
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| slug | VARCHAR(100) UNIQUE | 'about', 'welcome', 'daycare' |
| title | VARCHAR(200) | |
| content | TEXT | Rich text / HTML |
| meta_description | VARCHAR(300) | |
| updated_at | TIMESTAMP | |
| updated_by | FK → users | |

### announcements
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| title | VARCHAR(200) | |
| slug | VARCHAR(200) UNIQUE | |
| body | TEXT | Rich text |
| excerpt | VARCHAR(500) | |
| image_url | VARCHAR(500) | |
| is_published | BOOLEAN | DEFAULT FALSE |
| published_at | TIMESTAMP | |
| author_id | FK → users | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

### events
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| title | VARCHAR(200) | |
| description | TEXT | |
| location | VARCHAR(200) | |
| start_datetime | TIMESTAMP | |
| end_datetime | TIMESTAMP | |
| image_url | VARCHAR(500) | |
| is_recurring | BOOLEAN | DEFAULT FALSE |
| recurrence_rule | VARCHAR(100) | WEEKLY, MONTHLY, etc. |
| is_published | BOOLEAN | DEFAULT TRUE |
| created_at | TIMESTAMP | |

### ministries
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| name | VARCHAR(100) | |
| slug | VARCHAR(100) UNIQUE | |
| description | TEXT | |
| image_url | VARCHAR(500) | |
| sort_order | INTEGER | |
| is_active | BOOLEAN | DEFAULT TRUE |

### ministry_content
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| ministry_id | FK → ministries | CASCADE |
| title | VARCHAR(200) | |
| body | TEXT | |
| image_url | VARCHAR(500) | |
| sort_order | INTEGER | |

### fellowships
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| name | VARCHAR(100) | Berea, Chepkosa |
| slug | VARCHAR(100) UNIQUE | |
| description | TEXT | |
| meeting_day | VARCHAR(20) | |
| meeting_time | VARCHAR(50) | |
| location | VARCHAR(200) | |
| contact_person | VARCHAR(100) | |
| contact_phone | VARCHAR(20) | |
| is_active | BOOLEAN | DEFAULT TRUE |

### team_members
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| name | VARCHAR(100) | |
| title | VARCHAR(100) | Senior Pastor, Choir Director |
| bio | TEXT | |
| photo_url | VARCHAR(500) | |
| category | VARCHAR(50) | 'pastoral', 'choir', 'elder' |
| ministry_id | FK → ministries | nullable |
| sort_order | INTEGER | |
| is_active | BOOLEAN | DEFAULT TRUE |

### sermons
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| title | VARCHAR(200) | |
| slug | VARCHAR(200) UNIQUE | |
| speaker | VARCHAR(100) | |
| date | DATE | |
| series | VARCHAR(100) | |
| description | TEXT | |
| body | TEXT | For sermon notes / devotionals |
| content_type | VARCHAR(20) | 'sermon', 'devotional', 'note' |
| audio_url | VARCHAR(500) | |
| video_url | VARCHAR(500) | YouTube/Vimeo embed |
| image_url | VARCHAR(500) | |
| is_published | BOOLEAN | DEFAULT FALSE |
| created_at | TIMESTAMP | |

### media_items
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| title | VARCHAR(200) | |
| description | TEXT | |
| file_url | VARCHAR(500) | |
| file_type | VARCHAR(20) | 'image', 'video', 'audio' |
| category | VARCHAR(50) | 'gallery', 'choir', 'construction' |
| related_id | INTEGER | Polymorphic FK |
| related_type | VARCHAR(50) | 'ministry', 'construction', 'event' |
| thumbnail_url | VARCHAR(500) | |
| sort_order | INTEGER | |
| uploaded_at | TIMESTAMP | |
| uploaded_by | FK → users | |

### prayer_requests
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| name | VARCHAR(100) | nullable (anonymous) |
| email | VARCHAR(120) | |
| phone | VARCHAR(20) | |
| request | TEXT | |
| is_anonymous | BOOLEAN | DEFAULT FALSE |
| status | VARCHAR(20) | 'new', 'praying', 'answered' |
| created_at | TIMESTAMP | |
| notes | TEXT | Internal pastor/team notes |

### construction_updates
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| title | VARCHAR(200) | |
| description | TEXT | |
| date | DATE | |
| phase | VARCHAR(100) | Foundation, Walls, Roofing |
| progress_pct | INTEGER | 0-100 |
| is_published | BOOLEAN | DEFAULT TRUE |
| created_at | TIMESTAMP | |

### fundraising_groups
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| name | VARCHAR(100) | Group 1 through 10 |
| description | TEXT | |
| target_amount | DECIMAL(12,2) | |
| raised_amount | DECIMAL(12,2) | DEFAULT 0 |
| leader_name | VARCHAR(100) | |
| leader_phone | VARCHAR(20) | |
| sort_order | INTEGER | |

### giving_categories
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| name | VARCHAR(100) | Tithe, Offering, Construction |
| slug | VARCHAR(100) UNIQUE | |
| description | TEXT | |
| is_active | BOOLEAN | DEFAULT TRUE |
| sort_order | INTEGER | |

### donations
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| category_id | FK → giving_categories | |
| fundraising_group_id | FK → fundraising_groups | nullable |
| amount | DECIMAL(12,2) | |
| currency | VARCHAR(3) | DEFAULT 'KES' |
| payment_method | VARCHAR(20) | 'mpesa', 'card' |
| transaction_id | VARCHAR(100) UNIQUE | M-Pesa receipt / card txn |
| phone_number | VARCHAR(20) | |
| donor_name | VARCHAR(100) | |
| status | VARCHAR(20) | 'pending', 'completed', 'failed' |
| mpesa_checkout_id | VARCHAR(100) | Daraja CheckoutRequestID |
| callback_data | JSONB | Full callback for audit |
| created_at | TIMESTAMP | |
| completed_at | TIMESTAMP | |

### connection_cards
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| name | VARCHAR(100) | |
| email | VARCHAR(120) | |
| phone | VARCHAR(20) | |
| how_heard | VARCHAR(100) | |
| interests | TEXT | |
| prayer_needs | TEXT | |
| is_first_visit | BOOLEAN | DEFAULT TRUE |
| visit_date | DATE | |
| created_at | TIMESTAMP | |

### volunteer_signups
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| name | VARCHAR(100) | |
| email | VARCHAR(120) | |
| phone | VARCHAR(20) | |
| ministry_id | FK → ministries | |
| message | TEXT | |
| status | VARCHAR(20) | 'new', 'contacted', 'active' |
| created_at | TIMESTAMP | |

### site_settings
| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | |
| key | VARCHAR(100) UNIQUE | 'year_theme', 'whatsapp_number' |
| value | TEXT | |
| updated_at | TIMESTAMP | |

---

## Admin Panel Design

Custom CMS (not Flask-Admin) with Bootstrap UI for non-technical staff.

### Sections
- **Dashboard** — Quick stats: recent prayer requests, upcoming events, donation totals
- **Announcements** — CRUD with TinyMCE rich text, image upload, publish/draft
- **Events** — CRUD with date/time pickers
- **Ministries** — Manage ministry pages and sub-content
- **Fellowships** — Manage fellowship details
- **Team Members** — Manage pastoral team, choir, elders with photo upload
- **Sermons & Devotionals** — CRUD with audio/video URL fields
- **Media Gallery** — Bulk image upload with Dropzone.js
- **Construction** — Progress updates + fundraising groups
- **Giving** — View donation transactions, filter, export CSV
- **Prayer Requests** — View/manage with status updates and internal notes
- **Connection Cards** — View newcomer submissions
- **Volunteer Sign-ups** — View with status management
- **Pages** — Edit static content (About, Welcome, Services)
- **Settings** — Year theme, WhatsApp number, social media links

### Roles
- **admin** — Full access, can manage users
- **editor** — Create/edit content, no user management or donation details
- **viewer** — Read-only dashboard access

---

## M-Pesa Daraja API Integration

### STK Push Flow
1. User selects giving category → enters amount + phone (254XXXXXXXXX)
2. POST to `/api/mpesa/stk-push` with amount, phone, category_id
3. Backend:
   - Get OAuth token: `GET https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials`
   - Generate password: `base64(ShortCode + Passkey + Timestamp)`
   - POST to `https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest`
   - Save CheckoutRequestID to donations table (status: pending)
4. Safaricom pushes STK to user's phone → user enters PIN
5. Safaricom POSTs callback to `/api/mpesa/callback`:
   - ResultCode 0 → mark completed, store MpesaReceiptNumber
   - Non-zero → mark failed
   - Always return `{"ResultCode": 0, "ResultDesc": "Accepted"}`
6. Frontend polls `/api/mpesa/status/<checkout_id>` via HTMX every 3s

### Environment Variables
```
MPESA_CONSUMER_KEY=
MPESA_CONSUMER_SECRET=
MPESA_SHORTCODE=
MPESA_PASSKEY=
MPESA_ENV=sandbox   # or production
MPESA_CALLBACK_URL=https://yourdomain.co.ke/api/mpesa/callback
```

---

## Frontend Guidelines

### Mobile-First Performance
- Bootstrap 5 via CDN (no jQuery dependency)
- HTMX (~14KB gzipped) for dynamic interactions
- Lazy-load images with `loading="lazy"`
- Compress images on upload (Pillow: max 1200px width, JPEG quality 80)
- Nginx serves static files with `expires 30d`
- Target: first meaningful paint under 3s on Slow 3G

### HTMX Usage
- M-Pesa payment status polling
- Load more pagination (announcements, sermons, gallery)
- Calendar month navigation
- Form submissions (prayer request, connection card, volunteer)
- Admin panel: inline editing, search/filter

### Template Hierarchy
- `base.html` → navbar, footer, WhatsApp button, Bootstrap/HTMX includes
- `admin/base.html` → sidebar layout for admin panel
- All public pages extend `base.html`
- All admin pages extend `admin/base.html`
- `partials/` folder for HTMX fragment responses

---

## Deployment (DigitalOcean)

### Server Stack
```
Ubuntu 24.04 LTS
├── Nginx (reverse proxy, static files, SSL)
├── Gunicorn (3 workers, unix socket)
├── PostgreSQL 16
├── Certbot (Let's Encrypt SSL)
└── UFW firewall (ports 80, 443, 22)
```

### Gunicorn Command
```bash
gunicorn --workers 3 --bind unix:/tmp/imanifellowship.sock --timeout 120 "app:create_app('production')"
```

### Deployment Steps
1. SSH → `git pull origin main`
2. `pip install -r requirements.txt`
3. `flask db upgrade`
4. `sudo systemctl restart imanifellowship`

### Backups
- DigitalOcean automated droplet backups
- Daily PostgreSQL dump via cron

---

## Build Phases

### Phase 1: Foundation
- [x] Flask app factory, extensions, config
- [ ] User model, auth blueprint (login/logout)
- [ ] base.html with Bootstrap 5, navbar, footer, WhatsApp button
- [ ] Home page placeholder, admin login page
- [ ] Flask-Migrate setup, create_admin.py CLI

### Phase 2: Admin CMS Core
- [ ] Announcement, Event, TeamMember, Page, SiteSetting models
- [ ] Admin CRUD views with TinyMCE + image upload
- [ ] Dynamic home page (year theme, announcements, events)
- [ ] About page

### Phase 3: Ministries & Content
- [ ] Ministry, Fellowship, ConnectionCard, VolunteerSignup models
- [ ] Ministry listing + detail pages
- [ ] Newcomers, volunteer sign-up, services pages

### Phase 4: Media & Sermons
- [ ] Sermon model + admin + public archive
- [ ] MediaItem + gallery management + bulk upload
- [ ] Choir page, devotionals section

### Phase 5: M-Pesa & Giving
- [ ] GivingCategory, FundraisingGroup, Donation models
- [ ] Full Daraja API integration (services/mpesa.py)
- [ ] Giving page with HTMX status polling
- [ ] Construction page + fundraising groups
- [ ] Admin donation reports

### Phase 6: Prayer Requests & Calendar
- [ ] PrayerRequest model + form + admin management
- [ ] Email notifications (Flask-Mail)
- [ ] Interactive calendar with HTMX

### Phase 7: Polish & Deploy
- [ ] DigitalOcean setup (Nginx, Gunicorn, SSL, Spaces)
- [ ] Performance optimization
- [ ] SEO (sitemap, robots.txt, Open Graph)
- [ ] Database backups

### Phase 8: Post-Launch (Future)
- [ ] Card payments (Flutterwave)
- [ ] SMS notifications (Africa's Talking)
- [ ] Swahili/English toggle
- [ ] PWA support
