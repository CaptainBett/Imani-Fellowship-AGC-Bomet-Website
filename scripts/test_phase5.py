"""Test all Phase 5 routes."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.giving import GivingCategory, Donation

app = create_app('testing')
client = app.test_client()

with app.app_context():
    db.create_all()

    user = User(email='admin@test.com', display_name='Admin', role='admin', is_active=True)
    user.set_password('admin1234')

    c1 = GivingCategory(name='Tithes', slug='tithes', description='10% giving', is_active=True, sort_order=1)
    c2 = GivingCategory(name='Offerings', slug='offerings', description='Free-will offering', is_active=True, sort_order=2)
    c3 = GivingCategory(name='Building Fund', slug='building-fund', description='Church construction', is_active=True, sort_order=3)

    d1 = Donation(category_id=1, amount=1000, phone_number='254712345678',
                  donor_name='Test Donor', status='completed', transaction_id='ABC123')
    d2 = Donation(category_id=2, amount=500, phone_number='254712345678',
                  status='pending', mpesa_checkout_id='ws_CO_test123')

    db.session.add_all([user, c1, c2, c3, d1, d2])
    db.session.commit()

passed = 0
failed = 0

# Public routes
routes = [
    ('GET', '/give', 'Public giving page'),
]

print('=== Public Routes ===')
for method, url, desc in routes:
    resp = client.get(url)
    if resp.status_code == 200:
        print(f'  [PASS] {desc}')
        passed += 1
    else:
        print(f'  [FAIL ({resp.status_code})] {desc}')
        failed += 1

# Check the giving page has categories
resp = client.get('/give')
html = resp.data.decode()
if 'Tithes' in html and 'Offerings' in html and 'Building Fund' in html:
    print(f'  [PASS] Giving page shows categories')
    passed += 1
else:
    print(f'  [FAIL] Giving page missing categories')
    failed += 1

# API routes
print()
print('=== API Routes ===')

# STK push without data should return 400
resp = client.post('/api/mpesa/stk-push', data={})
if resp.status_code == 400:
    print(f'  [PASS] STK push rejects empty data (400)')
    passed += 1
else:
    print(f'  [FAIL ({resp.status_code})] STK push should reject empty data')
    failed += 1

# STK push with bad phone
resp = client.post('/api/mpesa/stk-push', data={'phone': 'abc', 'amount': '100'})
if resp.status_code == 400:
    print(f'  [PASS] STK push rejects invalid phone (400)')
    passed += 1
else:
    print(f'  [FAIL ({resp.status_code})] STK push should reject invalid phone')
    failed += 1

# Status poll - existing pending donation
resp = client.get('/api/mpesa/status/ws_CO_test123')
if resp.status_code == 200 and 'Waiting for payment' in resp.data.decode():
    print(f'  [PASS] Status poll returns pending state')
    passed += 1
else:
    print(f'  [FAIL ({resp.status_code})] Status poll for pending donation')
    failed += 1

# Status poll - non-existent
resp = client.get('/api/mpesa/status/nonexistent')
if resp.status_code == 200 and 'not found' in resp.data.decode():
    print(f'  [PASS] Status poll returns not found for unknown ID')
    passed += 1
else:
    print(f'  [FAIL ({resp.status_code})] Status poll for nonexistent')
    failed += 1

# Admin routes
print()
resp = client.post('/auth/login', data={'email': 'admin@test.com', 'password': 'admin1234'}, follow_redirects=True)
print(f'Admin login: {resp.status_code}')

admin_routes = [
    ('GET', '/admin/giving/categories', 'Admin giving categories'),
    ('GET', '/admin/giving/categories/create', 'Admin category create form'),
    ('GET', '/admin/giving/donations', 'Admin donations list'),
    ('GET', '/admin/giving/donations?status=completed', 'Admin donations filtered'),
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

# Test mpesa service phone formatting
from app.services.mpesa import format_phone
phone_tests = [
    ('0712345678', '254712345678'),
    ('+254712345678', '254712345678'),
    ('254712345678', '254712345678'),
    ('712345678', '254712345678'),
    ('abc', None),
    ('', None),
]
print()
print('=== Phone Formatting ===')
for input_phone, expected in phone_tests:
    result = format_phone(input_phone)
    if result == expected:
        print(f'  [PASS] format_phone("{input_phone}") = {result}')
        passed += 1
    else:
        print(f'  [FAIL] format_phone("{input_phone}") = {result}, expected {expected}')
        failed += 1

print()
print(f'Results: {passed} passed, {failed} failed out of {passed + failed} tests')
