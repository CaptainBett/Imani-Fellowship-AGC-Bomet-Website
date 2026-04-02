"""Test all Phase 4 routes."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.sermon import Sermon
from app.models.media import MediaItem
from app.models.team_member import TeamMember

app = create_app('testing')
client = app.test_client()

with app.app_context():
    db.create_all()

    # Seed data
    user = User(email='admin@test.com', display_name='Admin', role='admin', is_active=True)
    user.set_password('admin1234')
    db.session.add(user)

    s1 = Sermon(title='Walking in Faith', slug='walking-in-faith', speaker='Pastor James',
                series='Faith Series', scripture_reference='Hebrews 11:1',
                body='<p>Notes on walking in faith...</p>', excerpt='A powerful sermon on faith.',
                content_type='sermon', sermon_date=date(2026, 3, 29),
                is_published=True, is_featured=True)
    s2 = Sermon(title='Morning Devotion', slug='morning-devotion', speaker='Elder Mary',
                body='<p>Start your day with God...</p>', content_type='devotional',
                sermon_date=date(2026, 3, 28), is_published=True)
    s3 = Sermon(title='Draft Sermon', slug='draft-sermon', content_type='sermon', is_published=False)
    db.session.add_all([s1, s2, s3])

    m1 = MediaItem(title='Sunday Service', file_url='uploads/gallery/test.jpg',
                   media_type='image', category='church', is_published=True)
    m2 = MediaItem(title='Choir Performance', file_url='https://youtube.com/watch?v=test',
                   media_type='video', category='choir', is_published=True)

    choir_member = TeamMember(name='John Singer', title='Tenor', category='choir',
                              is_active=True, sort_order=1)
    db.session.add_all([m1, m2, choir_member])
    db.session.commit()

# Test public routes
routes = [
    ('GET', '/sermons', 'Sermons listing'),
    ('GET', '/sermons/walking-in-faith', 'Sermon detail'),
    ('GET', '/sermons?type=devotional', 'Devotionals filter'),
    ('GET', '/sermons/load-more?page=1', 'HTMX load more'),
    ('GET', '/gallery', 'Gallery page'),
    ('GET', '/gallery?category=choir', 'Gallery choir filter'),
    ('GET', '/choir', 'Choir page'),
]

passed = 0
failed = 0

print('=== Public Routes ===')
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

# Draft should not be visible publicly
resp = client.get('/sermons/draft-sermon')
if resp.status_code == 404:
    print(f'  [PASS] Draft sermon returns 404')
    passed += 1
else:
    print(f'  [FAIL ({resp.status_code})] Draft sermon should be 404')
    failed += 1

# Admin login
print()
resp = client.post('/auth/login', data={'email': 'admin@test.com', 'password': 'admin1234'}, follow_redirects=True)
print(f'Admin login: {resp.status_code}')

admin_routes = [
    ('GET', '/admin/sermons', 'Admin sermons list'),
    ('GET', '/admin/sermons/create', 'Admin sermon create form'),
    ('GET', '/admin/sermons?type=devotional', 'Admin devotional filter'),
    ('GET', '/admin/gallery', 'Admin gallery list'),
    ('GET', '/admin/gallery/create', 'Admin gallery create form'),
    ('GET', '/admin/gallery?category=choir', 'Admin gallery choir filter'),
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

print()
print(f'Results: {passed} passed, {failed} failed out of {passed + failed} tests')
