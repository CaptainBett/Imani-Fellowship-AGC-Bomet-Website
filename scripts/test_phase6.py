"""Test all Phase 6 routes."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone, timedelta
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.event import Event
from app.models.prayer_request import PrayerRequest

app = create_app('testing')
client = app.test_client()

with app.app_context():
    db.create_all()

    user = User(email='admin@test.com', display_name='Admin', role='admin', is_active=True)
    user.set_password('admin1234')

    now = datetime.now(timezone.utc)
    e1 = Event(title='Sunday Service', start_datetime=now + timedelta(days=1),
               location='Main Sanctuary', is_published=True)
    e2 = Event(title='Bible Study', start_datetime=now + timedelta(days=3),
               location='Room 2', is_published=True, is_recurring=True, recurrence_rule='WEEKLY')
    e3 = Event(title='Draft Event', start_datetime=now + timedelta(days=5), is_published=False)

    pr1 = PrayerRequest(name='Jane', request='Please pray for my family.', is_public=True, status='praying')
    pr2 = PrayerRequest(request='Healing prayer needed.', is_anonymous=True, is_public=True, status='new')
    pr3 = PrayerRequest(name='John', request='Private request.', is_public=False, status='new')

    db.session.add_all([user, e1, e2, e3, pr1, pr2, pr3])
    db.session.commit()
    e1_id, e3_id = e1.id, e3.id
    pr1_id, pr2_id = pr1.id, pr2.id

passed = 0
failed = 0

# Public routes
routes = [
    ('GET', '/events', 'Events calendar page'),
    ('GET', f'/events/{e1_id}', 'Event detail'),
    ('GET', '/events?year=2026&month=5', 'Calendar month nav'),
    ('GET', '/prayer', 'Prayer request page'),
]

print('=== Public Routes ===')
for method, url, desc in routes:
    resp = client.get(url)
    status = resp.status_code
    if status in (301, 302, 308):
        resp = client.get(resp.headers['Location'])
        status = resp.status_code
    if status == 200:
        print(f'  [PASS] {desc}')
        passed += 1
    else:
        print(f'  [FAIL ({status})] {desc}')
        failed += 1

# Draft event should be 404
resp = client.get(f'/events/{e3_id}')
if resp.status_code == 404:
    print(f'  [PASS] Draft event returns 404')
    passed += 1
else:
    print(f'  [FAIL ({resp.status_code})] Draft event should be 404')
    failed += 1

# HTMX calendar request
resp = client.get('/events?year=2026&month=4', headers={'HX-Request': 'true'})
html = resp.data.decode()
if resp.status_code == 200 and 'April' in html:
    print(f'  [PASS] HTMX calendar returns partial')
    passed += 1
else:
    print(f'  [FAIL] HTMX calendar')
    failed += 1

# Prayer wall shows public requests
resp = client.get('/prayer')
html = resp.data.decode()
if 'Jane' in html and 'Anonymous' in html and 'Private request' not in html:
    print(f'  [PASS] Prayer wall shows public only')
    passed += 1
else:
    print(f'  [FAIL] Prayer wall filtering')
    failed += 1

# Prayer form HTMX submit
resp = client.post('/prayer', data={
    'name': 'Test User',
    'request': 'Please pray for my exams next week.',
    'is_public': 'y',
}, headers={'HX-Request': 'true'})
if resp.status_code == 200 and 'Prayer Request Submitted' in resp.data.decode():
    print(f'  [PASS] Prayer form HTMX submit')
    passed += 1
else:
    print(f'  [FAIL ({resp.status_code})] Prayer form submit')
    failed += 1

# Admin login
print()
resp = client.post('/auth/login', data={'email': 'admin@test.com', 'password': 'admin1234'}, follow_redirects=True)
print(f'Admin login: {resp.status_code}')

admin_routes = [
    ('GET', '/admin/prayer-requests', 'Admin prayer requests list'),
    ('GET', '/admin/prayer-requests?status=new', 'Admin prayer filter'),
    ('GET', f'/admin/prayer-requests/{pr1_id}', 'Admin prayer detail'),
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
        print(f'  [PASS] {desc}')
        passed += 1
    else:
        print(f'  [FAIL ({status})] {desc}')
        failed += 1

# Admin status update
resp = client.post(f'/admin/prayer-requests/{pr2_id}/status', data={'status': 'praying'}, follow_redirects=True)
if resp.status_code == 200:
    print(f'  [PASS] Admin prayer status update')
    passed += 1
else:
    print(f'  [FAIL ({resp.status_code})] Admin prayer status update')
    failed += 1

# Admin notes update
resp = client.post(f'/admin/prayer-requests/{pr1_id}/notes',
                   data={'notes': 'Follow up with Jane next Sunday'}, follow_redirects=True)
if resp.status_code == 200:
    print(f'  [PASS] Admin prayer notes update')
    passed += 1
else:
    print(f'  [FAIL ({resp.status_code})] Admin prayer notes update')
    failed += 1

print()
print(f'Results: {passed} passed, {failed} failed out of {passed + failed} tests')
