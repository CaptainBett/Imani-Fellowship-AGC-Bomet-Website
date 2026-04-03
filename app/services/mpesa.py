"""
M-Pesa Daraja API integration for STK Push payments.

Flow:
1. Get OAuth token from Safaricom
2. Generate password = base64(ShortCode + Passkey + Timestamp)
3. POST STK Push request → user receives prompt on phone
4. Safaricom POSTs callback with result → we update donation status
"""
import base64
import json
import logging
from datetime import datetime, timezone

import requests
from flask import current_app, request as flask_request

logger = logging.getLogger(__name__)

# API base URLs
SANDBOX_BASE = 'https://sandbox.safaricom.co.ke'
PRODUCTION_BASE = 'https://api.safaricom.co.ke'


def _get_base_url():
    env = current_app.config.get('MPESA_ENV', 'sandbox')
    return PRODUCTION_BASE if env == 'production' else SANDBOX_BASE


def _get_oauth_token():
    """Get OAuth access token from Safaricom Daraja API."""
    base_url = _get_base_url()
    consumer_key = current_app.config['MPESA_CONSUMER_KEY']
    consumer_secret = current_app.config['MPESA_CONSUMER_SECRET']

    url = f'{base_url}/oauth/v1/generate?grant_type=client_credentials'

    try:
        response = requests.get(url, auth=(consumer_key, consumer_secret), timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('access_token')
    except requests.RequestException as e:
        logger.error(f'M-Pesa OAuth error: {e}')
        return None


def _generate_password(shortcode, passkey, timestamp):
    """Generate the base64-encoded password for STK Push."""
    raw = f'{shortcode}{passkey}{timestamp}'
    return base64.b64encode(raw.encode()).decode()


def initiate_stk_push(phone_number, amount, account_reference='Giving', transaction_desc='Church Giving'):
    """
    Initiate an M-Pesa STK Push request.

    Args:
        phone_number: Phone in format 254XXXXXXXXX
        amount: Integer amount in KES
        account_reference: Short label (max 12 chars)
        transaction_desc: Description (max 13 chars)

    Returns:
        dict with keys: success (bool), checkout_request_id, merchant_request_id, error
    """
    token = _get_oauth_token()
    if not token:
        return {'success': False, 'error': 'Failed to get M-Pesa access token'}

    base_url = _get_base_url()
    shortcode = current_app.config['MPESA_SHORTCODE']
    passkey = current_app.config['MPESA_PASSKEY']
    # Use configured callback URL, or auto-construct from current domain
    callback_url = current_app.config.get('MPESA_CALLBACK_URL') or ''
    if not callback_url or 'yourdomain' in callback_url:
        callback_url = flask_request.url_root.rstrip('/') + '/api/mpesa/callback'

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = _generate_password(shortcode, passkey, timestamp)

    url = f'{base_url}/mpesa/stkpush/v1/processrequest'

    payload = {
        'BusinessShortCode': shortcode,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': int(amount),
        'PartyA': phone_number,
        'PartyB': shortcode,
        'PhoneNumber': phone_number,
        'CallBackURL': callback_url,
        'AccountReference': account_reference[:12],
        'TransactionDesc': transaction_desc[:13],
    }

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        data = response.json()

        logger.info(f'STK Push response: {json.dumps(data)}')

        if data.get('ResponseCode') == '0':
            return {
                'success': True,
                'checkout_request_id': data.get('CheckoutRequestID'),
                'merchant_request_id': data.get('MerchantRequestID'),
            }
        else:
            error_msg = data.get('errorMessage') or data.get('ResponseDescription', 'Unknown error')
            return {'success': False, 'error': error_msg}

    except requests.RequestException as e:
        logger.error(f'M-Pesa STK Push error: {e}')
        return {'success': False, 'error': 'Network error contacting M-Pesa'}


def process_callback(callback_data):
    """
    Process M-Pesa STK Push callback.

    Args:
        callback_data: The full JSON body from Safaricom callback

    Returns:
        dict with: checkout_request_id, result_code, result_desc, receipt_number, amount, phone
    """
    try:
        stk_callback = callback_data.get('Body', {}).get('stkCallback', {})

        result = {
            'merchant_request_id': stk_callback.get('MerchantRequestID'),
            'checkout_request_id': stk_callback.get('CheckoutRequestID'),
            'result_code': stk_callback.get('ResultCode'),
            'result_desc': stk_callback.get('ResultDesc', ''),
            'receipt_number': None,
            'amount': None,
            'phone': None,
        }

        # If successful (ResultCode == 0), extract metadata
        if result['result_code'] == 0:
            metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
            for item in metadata:
                name = item.get('Name')
                value = item.get('Value')
                if name == 'MpesaReceiptNumber':
                    result['receipt_number'] = value
                elif name == 'Amount':
                    result['amount'] = value
                elif name == 'PhoneNumber':
                    result['phone'] = str(value)

        return result

    except (KeyError, TypeError) as e:
        logger.error(f'Error processing M-Pesa callback: {e}')
        return None


def format_phone(phone):
    """
    Normalize a Kenyan phone number to 254XXXXXXXXX format.

    Accepts: 0712345678, +254712345678, 254712345678, 712345678
    Returns: 254712345678 or None if invalid
    """
    if not phone:
        return None

    phone = phone.strip().replace(' ', '').replace('-', '')

    if phone.startswith('+'):
        phone = phone[1:]

    if phone.startswith('0') and len(phone) == 10:
        phone = '254' + phone[1:]
    elif phone.startswith('7') and len(phone) == 9:
        phone = '254' + phone
    elif phone.startswith('1') and len(phone) == 9:
        phone = '254' + phone

    if phone.startswith('254') and len(phone) == 12 and phone.isdigit():
        return phone

    return None
