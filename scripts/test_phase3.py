"""Test all Phase 3 routes."""
from app import create_app
from app.extensions import db
from app.models.ministry import Ministry, MinistryContent
from app.models.fellowship import Fellowship
from app.models.page import Page
from app.models.user import User

app = create_app('testing')
client = app.test_client()

with app.app_context():
    db.create_all()

    user = User(email='admin@test.com', display_name='Admin', role='admin', is_active=True)
    user.set_password('admin1234')
    m1 = Ministry(name='Youth Ministry', slug='youth-ministry', description='Empowering the next generation.', icon='bi-people', sort_order=1, is_active=True)
    m2 = Ministry(name='Worship Ministry', slug='worship-ministry', description='Leading worship through music.', icon='bi-music-note-beamed', sort_order=2, is_active=True)
    f1 = Fellowship(name='Men Fellowship', slug='men-fellowship', description='Brotherhood in Christ.', meeting_day='Saturday', meeting_time='2:00 PM', location='Main Hall', contact_person='John Doe', is_active=True)
    f2 = Fellowship(name='Women Fellowship', slug='women-fellowship', description='Sisters in faith.', meeting_day='Thursday', meeting_time='10:00 AM', location='Room 2', contact_person='Jane Doe', is_active=True)
    p1 = Page(title='Daycare', slug='daycare', content='<p>Quality daycare services.</p>')
    p2 = Page(title='Conference Venue', slug='conference-venue', content='<p>Modern facilities.</p>')
    db.session.add_all([user, m1, m2, f1, f2, p1, p2])
    db.session.flush()

    mc1 = MinistryContent(ministry_id=m1.id, title='Our Vision', body='To raise a godly generation.', sort_order=1)
    db.session.add(mc1)
    db.session.commit()

routes = [
    ('GET', '/ministries/', 'Ministries listing'),
    ('GET', '/ministries/youth-ministry', 'Ministry detail'),
    ('GET', '/fellowships/', 'Fellowships listing'),
    ('GET', '/newcomers', 'Newcomers page'),
    ('GET', '/connect', 'Connection card form'),
    ('GET', '/volunteer', 'Volunteer form'),
    ('GET', '/services', 'Services page'),
]

print('=== Public Routes ===')
passed = 0
failed = 0
for method, url, desc in routes:
    resp = client.get(url)
    status = resp.status_code
    if status in (301, 302, 308):
        resp = client.get(resp.headers['Location'])
        status = resp.status_code
    if status == 200:
        print(f'  [PASS] {desc} ({url})')
        passed += 1
    else:
        print(f'  [FAIL ({status})] {desc} ({url})')
        failed += 1

# Admin login
print()
resp = client.post('/auth/login', data={'email': 'admin@test.com', 'password': 'admin1234'}, follow_redirects=True)
print(f'Admin login: {resp.status_code}')

admin_routes = [
    ('GET', '/admin/ministries', 'Admin ministries list'),
    ('GET', '/admin/ministries/create', 'Admin ministry create form'),
    ('GET', '/admin/fellowships', 'Admin fellowships list'),
    ('GET', '/admin/fellowships/create', 'Admin fellowship create form'),
    ('GET', '/admin/connection-cards', 'Admin connection cards'),
    ('GET', '/admin/volunteers', 'Admin volunteers'),
]

print()
print('=== Admin Routes ===')
for method, url, desc in admin_routes:
    resp = client.get(url)
    status = resp.status_code
    if status in (301, 302, 308):
        resp = client.get(resp.headers['Location'])
        status = resp.status_code
    if status == 200:
        print(f'  [PASS] {desc} ({url})')
        passed += 1
    else:
        print(f'  [FAIL ({status})] {desc} ({url})')
        failed += 1

# Test HTMX form submissions
print()
print('=== Form Submissions ===')
resp = client.post('/connect', data={
    'name': 'Test Visitor',
    'email': 'visitor@test.com',
    'phone': '0712345678',
    'how_heard': 'Friend',
    'is_first_visit': 'y',
}, headers={'HX-Request': 'true'})
label = 'PASS' if resp.status_code == 200 else f'FAIL ({resp.status_code})'
print(f'  [{label}] Connection card submit')
if resp.status_code == 200:
    passed += 1
else:
    failed += 1

resp = client.post('/volunteer', data={
    'name': 'Test Volunteer',
    'email': 'vol@test.com',
    'phone': '0712345678',
    'ministry_id': '1',
    'message': 'I want to serve!',
}, headers={'HX-Request': 'true'})
label = 'PASS' if resp.status_code == 200 else f'FAIL ({resp.status_code})'
print(f'  [{label}] Volunteer signup')
if resp.status_code == 200:
    passed += 1
else:
    failed += 1

print()
print(f'Results: {passed} passed, {failed} failed out of {passed + failed} tests')
