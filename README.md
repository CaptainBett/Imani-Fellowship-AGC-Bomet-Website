# Imani Fellowship AGC Bomet - Church Website

A complete, modern website for **Imani Fellowship Africa Gospel Church (AGC), Bomet, Kenya**. The site serves church members, visitors, and administrators with information about services, ministries, events, sermons, giving, and the ongoing sanctuary construction project.

---

## Table of Contents

- [What This Website Does](#what-this-website-does)
- [Public Website Guide](#public-website-guide)
  - [Homepage](#homepage)
  - [About Us](#about-us)
  - [Ministries](#ministries)
  - [Fellowships](#fellowships)
  - [Sermons & Devotionals](#sermons--devotionals)
  - [Gallery & Choir](#gallery--choir)
  - [Events & Calendar](#events--calendar)
  - [Giving (M-Pesa)](#giving-m-pesa)
  - [Prayer Requests](#prayer-requests)
  - [Sanctuary Construction](#sanctuary-construction)
  - [Connect Pages](#connect-pages)
- [Admin Panel Guide](#admin-panel-guide)
  - [Logging In](#logging-in)
  - [Dashboard](#dashboard)
  - [Managing Announcements](#managing-announcements)
  - [Managing Events](#managing-events)
  - [Managing Team Members](#managing-team-members)
  - [Managing Ministries](#managing-ministries)
  - [Managing Fellowships](#managing-fellowships)
  - [Managing Sermons](#managing-sermons)
  - [Managing Gallery](#managing-gallery)
  - [Managing Giving Categories & Donations](#managing-giving-categories--donations)
  - [Managing Prayer Requests](#managing-prayer-requests)
  - [Construction Management](#construction-management)
  - [Managing Pages (CMS)](#managing-pages-cms)
  - [Site Settings](#site-settings)
  - [Connection Cards & Volunteers](#connection-cards--volunteers)
- [Technical README](#technical-readme)

---

## What This Website Does

This website is the online home for Imani Fellowship AGC. It allows:

- **Church members** to view upcoming events, read sermons, submit prayer requests, give offerings via M-Pesa, join fellowships, volunteer, and track the sanctuary construction progress.
- **Visitors and newcomers** to learn about the church, find service times, fill out a connection card, and explore what the church offers.
- **Church administrators** (pastors, elders, media team) to manage all website content — announcements, events, sermons, gallery photos, ministries, giving categories, prayer requests, and construction updates — all from an easy-to-use admin panel.

---

## Public Website Guide

These are the pages that anyone visiting the website can see.

### Homepage

**What you see:** The first page when you open the website.

- **Hero Banner** — A large welcome section with the church image in the background. It has two buttons: "Give" (for offerings) and "I'm New" (for first-time visitors).
- **Year Theme** — Displays the church's current year theme with the Bible verse.
- **Our Ministries** — Cards showing each active ministry (Youth, Women, Men, Children, etc.). Clicking a card takes you to that ministry's full page.
- **Construction Section** — A section about the ongoing sanctuary construction with a background image. Has a "View Progress" button that goes to the full construction page, and a "Give Towards Construction" button.
- **Upcoming Events** — Shows the next 3 upcoming events. Clicking an event shows its full details.
- **Quick Links** — Buttons for: View All Events, Watch Sermons, Submit Prayer Request, and I'm New Here.
- **Service Times** — Shows when the church meets (Sunday Service, Wednesday Bible Study, Friday Prayer, Youth Saturday).
- **WhatsApp Button** — A green floating button in the bottom-right corner that opens a WhatsApp chat with the church (if the WhatsApp number is configured in settings).

### About Us

**URL:** `/about`

Shows information about the church including:
- Church history and vision
- Mission statement and core values
- Pastoral team with photos
- Church elders

### Ministries

**URL:** `/ministries`

A page listing all active ministries as cards. Each card shows the ministry name, icon, and a short description. Clicking a card opens the ministry detail page which can include:
- Full description
- Content sections with images (added from admin)
- Team members assigned to that ministry

### Fellowships

**URL:** `/fellowships`

Lists all fellowship groups (e.g., Berea Fellowship, etc.) as cards showing:
- Fellowship name and description
- Meeting day, time, and location
- Contact person
- **"Join via WhatsApp" button** — Tapping this opens WhatsApp with a pre-filled message to the fellowship's contact person saying you'd like to join

### Sermons & Devotionals

**URL:** `/sermons`

An archive of all published sermons, devotionals, and study notes. Each sermon card shows:
- Title, speaker, date, and scripture reference
- Cover image (if uploaded)
- Short summary

Clicking a sermon opens its full page with:
- Embedded YouTube/Vimeo video (if a video link was added)
- Audio player (if an audio link was added)
- Full sermon notes/content

The page loads more sermons as you scroll down (no need to click "next page").

### Gallery & Choir

**URL:** `/gallery` and `/choir`

- **Gallery** — A grid of church photos organized by category. Clicking a photo opens it in a lightbox (large view). Categories include General, Events, Church Life, and Construction.
- **Choir** — A dedicated page for the church choir with photos and information.

### Events & Calendar

**URL:** `/events`

A monthly calendar view showing all published events. You can:
- Navigate between months using the arrow buttons
- See events highlighted on the calendar
- Click an event to see full details (date, time, location, description, image)

Events can be marked as recurring (weekly, biweekly, or monthly).

### Giving (M-Pesa)

**URL:** `/give`

Members can give offerings and tithes directly through the website via M-Pesa. The flow:

1. Select a giving category (e.g., Tithe, Offering, Construction, Missions)
2. Enter the amount in KES
3. Enter your M-Pesa phone number
4. Click "Give Now"
5. You will receive an **M-Pesa STK Push** prompt on your phone — enter your M-Pesa PIN to confirm
6. The page automatically checks for payment confirmation and shows a success message

All donations are recorded and can be viewed by administrators.

### Prayer Requests

**URL:** `/prayer`

Members can submit prayer requests through a form. Options include:
- Your name (or submit anonymously)
- Your prayer request
- Choose whether it appears on the public prayer wall

The **Prayer Wall** section on the same page shows approved public prayer requests so the community can pray together.

### Sanctuary Construction

**URL:** `/construction`

A dedicated page tracking the church's ongoing sanctuary construction project:

- **Hero Banner** — Construction photo background showing total fundraising progress
- **Overall Progress Bar** — Shows total amount raised vs. target across all groups
- **Construction Timeline** — A visual timeline of construction phases (e.g., Foundation, Walls, Roofing). Each phase shows:
  - Phase name and description
  - Progress percentage bar
  - Photo of the phase (if uploaded)
  - Status badge: "Completed", "In Progress", or percentage
- **Fundraising Groups** — Cards for each fundraising group showing:
  - Group name and description
  - Target amount vs. amount raised with progress bar
  - Contact person
  - **"Join Group via WhatsApp"** button to contact the group leader
- **Construction Gallery** — Photos of the construction progress
- **"Give Now" Call-to-Action** — Button linking to the giving page

### Connect Pages

- **Newcomers** (`/newcomers`) — Welcome page for first-time visitors with information about what to expect
- **Connection Card** (`/connect`) — A form for newcomers to fill out their details (name, email, phone, interests, prayer needs). The church team receives these and can follow up.
- **Volunteer** (`/volunteer`) — A sign-up form for members who want to volunteer in a ministry. They select which ministry they're interested in and provide their contact details.
- **Services & Facilities** (`/services`) — Information about church services and facilities available to the community (e.g., Daycare, Conference Venue). Each can have a featured image.

---

## Admin Panel Guide

The admin panel is where authorized church leaders manage all the content on the website. Everything you see on the public site can be controlled from here.

### Logging In

**URL:** `/auth/login`

1. Go to the website and add `/auth/login` to the address
2. Enter your username and password
3. Click "Log In"
4. You will be taken to the Admin Dashboard

Only registered administrators can log in. Contact the website developer to create new admin accounts.

### Dashboard

**URL:** `/admin/`

After logging in, you see the dashboard with:
- A welcome message
- Quick summary of content across the site
- Sidebar menu on the left with links to all management sections

The sidebar is organized into sections:

| Section | What It Manages |
|---------|----------------|
| **Dashboard** | Overview page |
| **Announcements** | Church announcements/news |
| **Events** | Calendar events |
| **Team Members** | Pastoral team, elders, deacons |
| **Construction** | Building phases and fundraising groups |
| **Gallery** | Photo/video gallery |
| **Sermons** | Sermon recordings and notes |
| **Ministries** | Ministry pages and content |
| **Fellowships** | Fellowship group information |
| **Giving** | Giving categories and donation records |
| **Prayer Requests** | Prayer requests from members |
| **Pages** | Custom content pages (Daycare, Conference, etc.) |
| **Connection Cards** | Forms submitted by newcomers |
| **Volunteers** | Volunteer sign-ups |
| **Site Settings** | Church phone, email, social links, year theme |

### Managing Announcements

**Where:** Admin > Announcements

- **View all** — See a list of all announcements with their publish status
- **Create new** — Click "New Announcement", fill in:
  - Title
  - Short excerpt (summary)
  - Full content (rich text editor with formatting, images, links)
  - Featured image (upload a photo)
  - Publish checkbox (uncheck to save as draft)
- **Edit** — Click the edit button on any announcement to update it
- **Delete** — Click the delete button to remove an announcement

### Managing Events

**Where:** Admin > Events

- **Create new** — Click "New Event", fill in:
  - Title (e.g., "Youth Retreat 2026")
  - Description
  - Location
  - Start date and time
  - End date and time (optional)
  - Event image (upload)
  - Recurring — Check if the event repeats (weekly, biweekly, monthly)
  - Published checkbox
- **Edit/Delete** — Same as announcements

Events appear on the public calendar and on the homepage if they're upcoming.

### Managing Team Members

**Where:** Admin > Team Members

Add and manage church leadership displayed on the About page:
- **Name** and **Title/Role** (e.g., "Senior Pastor")
- **Biography** — Short bio
- **Photo** — Upload a photo
- **Category** — Pastoral Team, Church Elders, Deacons, Choir Members, or Ministry Leaders
- **Display Order** — Number controlling the order they appear (lower = first)
- **Active** checkbox — Uncheck to hide without deleting

### Managing Ministries

**Where:** Admin > Ministries

Ministries appear as cards on the homepage and have their own detail pages.

- **Create new ministry:**
  - Name (e.g., "Youth Ministry")
  - URL Slug (auto-generated from name, e.g., "youth-ministry")
  - Description
  - Image (upload)
  - Bootstrap Icon Class (the icon shown on the card, e.g., `bi-people`)
  - Display Order and Active status

- **Content Sections** — Each ministry page can have multiple content sections. After creating a ministry, you can add sections with:
  - Section title
  - Body text (rich text editor)
  - Section image
  - Display order

### Managing Fellowships

**Where:** Admin > Fellowships

- **Create new fellowship:**
  - Name (e.g., "Berea Bible Study Fellowship")
  - URL Slug
  - Description
  - Meeting Day (dropdown: Monday–Sunday)
  - Meeting Time (e.g., "4:00 PM")
  - Location
  - Contact Person name
  - Contact Phone (e.g., "254712345678" — this is used for the WhatsApp join button)
  - Image (upload)
  - Active status

### Managing Sermons

**Where:** Admin > Sermons

- **Create new sermon:**
  - Title
  - Speaker (e.g., "Pastor John")
  - Series (e.g., "Faith Foundations")
  - Scripture Reference (e.g., "Romans 8:28-30")
  - Short Summary
  - Full Content/Notes (rich text editor)
  - Video URL — Paste a YouTube or Vimeo link and it will embed automatically
  - Audio URL — Link to an audio file
  - Cover Image (upload)
  - Type — Sermon, Devotional, or Study Note
  - Date
  - Published and Featured checkboxes

### Managing Gallery

**Where:** Admin > Gallery

Upload photos and videos to the church gallery:
- **Title** and **Description**
- **Media Type** — Image or Video
- **Category** — General Gallery, Choir, Event, Church Life, or Construction
- **Upload Image** — Select a photo from your device
- **Video URL** — For videos, paste a YouTube/Vimeo link
- **Display Order** and **Published** status

### Managing Giving Categories & Donations

**Where:** Admin > Giving

**Categories** — Define what members can give towards:
- Name (e.g., "Tithe", "Building Fund", "Missions")
- Description
- Display Order
- Active status

**Donations** — View a list of all M-Pesa donations received through the website, including:
- Donor phone number
- Amount
- Category
- M-Pesa receipt number
- Status (Pending, Completed, Failed)
- Date

### Managing Prayer Requests

**Where:** Admin > Prayer Requests

View all prayer requests submitted by members:
- **List view** — Shows all requests with name, excerpt, date, and status
- **Detail view** — Click a request to see the full text
- **Status** — Change between: New, Praying, Answered
- **Notes** — Add private pastoral notes about follow-up
- **Delete** — Remove a request

Only prayer requests marked as "public" by the submitter appear on the public prayer wall.

### Construction Management

**Where:** Admin > Construction

This is where you manage the sanctuary construction progress page.

**Construction Phases:**
- Click "Add Phase" to create a new construction phase
- **Phase Name** (e.g., "Foundation", "Wall Construction", "Roofing")
- **Description** — What this phase involves
- **Progress (%)** — Enter 0 to 100 to show how complete this phase is
- **Phase Image** — Upload a photo showing this phase
- **Display Order** — Controls the order in the timeline
- **Mark as Current Phase** — Check this for the phase currently underway (shows a pulsing green dot on the public page)

**Fundraising Groups:**
- Click "Add Group" to create a new fundraising group
- **Group Name** (e.g., "Group 1 - Imani Builders")
- **Description**
- **Target Amount (KES)** — The fundraising goal for this group
- **Amount Raised (KES)** — How much has been raised so far (update this regularly)
- **Contact Person** — Group leader's name
- **Contact Phone** — For the WhatsApp join button (e.g., "254712345678")
- **Group Image** (optional)
- **Active** checkbox

The dashboard shows summary cards with total phases, total target, and total raised.

### Managing Pages (CMS)

**Where:** Admin > Pages

Create and edit custom content pages used across the site. Some pages are pre-defined and used by specific sections:

| Page Slug | Where It Appears |
|-----------|-----------------|
| `daycare` | Services & Facilities page — Daycare section |
| `conference-venue` | Services & Facilities page — Conference section |
| `services` | Services & Facilities page — General content |

- **Page Title** — The heading
- **Content** — Rich text editor (TinyMCE) where you can format text, add images, create lists, insert links, and more
- **Featured Image** — Upload a main image for the page
- **Meta Description** — Short description for search engines (SEO)

### Site Settings

**Where:** Admin > Settings

Configure global website settings:

| Setting | What It Controls |
|---------|-----------------|
| **Year Theme** | Displayed on the homepage banner (e.g., "Year of Open Doors") |
| **Year Theme Bible Verse** | Scripture reference for the year theme |
| **WhatsApp Number** | The floating WhatsApp button number (format: 254712345678) |
| **Church Phone** | Phone number shown in the footer and contact sections |
| **Church Email** | Email shown in the footer and contact sections |
| **Facebook URL** | Link to the church Facebook page |
| **YouTube URL** | Link to the church YouTube channel |
| **Instagram URL** | Link to the church Instagram |
| **Twitter/X URL** | Link to the church Twitter/X account |

### Connection Cards & Volunteers

**Where:** Admin > Connection Cards and Admin > Volunteers

- **Connection Cards** — View forms submitted by newcomers/visitors with their name, contact info, how they heard about the church, interests, and prayer needs. You can delete processed cards.
- **Volunteers** — View volunteer sign-ups with the person's name, contact, preferred ministry, and message. You can update their status (Pending, Contacted, Active, Inactive).

---

## Technical README

For developer setup, architecture, and deployment instructions, see **[TECHNICAL_README.md](TECHNICAL_README.md)**.
