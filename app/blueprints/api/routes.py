"""
API endpoints for M-Pesa STK Push integration.

Endpoints:
  POST /api/mpesa/stk-push   — Initiate STK push to user's phone
  POST /api/mpesa/callback    — Safaricom callback (receives payment result)
  GET  /api/mpesa/status/<id> — Poll payment status (HTMX polling)
"""
import json
import logging
from datetime import datetime, timezone

from flask import request, jsonify, render_template_string
from app.blueprints.api import api_bp
from app.extensions import db, csrf
from app.models.giving import Donation, GivingCategory
from app.services.mpesa import initiate_stk_push, process_callback, format_phone

logger = logging.getLogger(__name__)


@api_bp.route('/mpesa/stk-push', methods=['POST'])
def mpesa_stk_push():
    """Initiate M-Pesa STK Push payment."""
    phone = request.form.get('phone', '').strip()
    amount = request.form.get('amount', '').strip()
    category_id = request.form.get('category_id', '').strip()
    donor_name = request.form.get('donor_name', '').strip()

    # Validate
    if not phone or not amount:
        return jsonify({'success': False, 'error': 'Phone number and amount are required'}), 400

    formatted_phone = format_phone(phone)
    if not formatted_phone:
        return jsonify({'success': False, 'error': 'Invalid phone number. Use format 0712345678 or 254712345678'}), 400

    try:
        amount_int = int(float(amount))
        if amount_int < 1:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid amount'}), 400

    # Determine account reference from category
    account_ref = 'Church Giving'
    if category_id:
        cat = GivingCategory.query.get(int(category_id))
        if cat:
            account_ref = cat.name[:12]

    # Initiate STK Push
    result = initiate_stk_push(
        phone_number=formatted_phone,
        amount=amount_int,
        account_reference=account_ref,
        transaction_desc='Imani Giving',
    )

    if result['success']:
        # Save donation record as pending
        donation = Donation(
            category_id=int(category_id) if category_id else None,
            amount=amount_int,
            phone_number=formatted_phone,
            donor_name=donor_name or None,
            status='pending',
            mpesa_checkout_id=result['checkout_request_id'],
        )
        db.session.add(donation)
        db.session.commit()

        return jsonify({
            'success': True,
            'checkout_request_id': result['checkout_request_id'],
            'message': 'Check your phone for the M-Pesa prompt. Enter your PIN to complete.',
        })
    else:
        return jsonify({'success': False, 'error': result.get('error', 'Unknown error')}), 500


@api_bp.route('/mpesa/callback', methods=['POST'])
@csrf.exempt
def mpesa_callback():
    """
    Safaricom M-Pesa callback endpoint.
    This is called by Safaricom servers after the user completes (or cancels) the STK push.
    Must always return {"ResultCode": 0, "ResultDesc": "Accepted"}.
    """
    try:
        callback_data = request.get_json(force=True)
        logger.info(f'M-Pesa callback received: {json.dumps(callback_data)}')

        result = process_callback(callback_data)
        if not result:
            logger.error('Failed to parse M-Pesa callback')
            return jsonify({'ResultCode': 0, 'ResultDesc': 'Accepted'})

        # Find the pending donation
        donation = Donation.query.filter_by(
            mpesa_checkout_id=result['checkout_request_id']
        ).first()

        if donation:
            if result['result_code'] == 0:
                donation.status = 'completed'
                donation.transaction_id = result['receipt_number']
                donation.completed_at = datetime.now(timezone.utc)
                if result['phone']:
                    donation.phone_number = result['phone']
            else:
                donation.status = 'failed'

            donation.callback_data = json.dumps(callback_data)
            db.session.commit()
            logger.info(f'Donation {donation.id} updated to {donation.status}')
        else:
            logger.warning(f'No donation found for checkout ID: {result["checkout_request_id"]}')

    except Exception as e:
        logger.error(f'Error processing M-Pesa callback: {e}')

    # Always return success to Safaricom
    return jsonify({'ResultCode': 0, 'ResultDesc': 'Accepted'})


@api_bp.route('/mpesa/status/<checkout_id>')
def mpesa_status(checkout_id):
    """
    Poll payment status — used by HTMX to update the UI.
    Returns an HTML fragment with the current status.
    """
    donation = Donation.query.filter_by(mpesa_checkout_id=checkout_id).first()

    if not donation:
        return '<div class="alert alert-danger">Payment not found.</div>'

    if donation.status == 'completed':
        return f'''
        <div class="alert alert-success">
            <h5 class="alert-heading"><i class="bi bi-check-circle-fill"></i> Payment Successful!</h5>
            <p class="mb-1">Amount: <strong>KES {donation.amount:,.0f}</strong></p>
            <p class="mb-1">Receipt: <strong>{donation.transaction_id or "Processing..."}</strong></p>
            <p class="mb-0">Thank you for your generous giving. God bless you!</p>
        </div>
        '''
    elif donation.status == 'failed':
        return '''
        <div class="alert alert-danger">
            <h5 class="alert-heading"><i class="bi bi-x-circle-fill"></i> Payment Failed</h5>
            <p class="mb-0">The transaction was not completed. Please try again.</p>
        </div>
        '''
    else:
        # Still pending — tell HTMX to keep polling
        return f'''
        <div class="alert alert-info" hx-get="/api/mpesa/status/{checkout_id}"
             hx-trigger="every 3s" hx-swap="outerHTML">
            <div class="d-flex align-items-center">
                <div class="spinner-border spinner-border-sm me-3" role="status"></div>
                <div>
                    <strong>Waiting for payment...</strong><br>
                    <small>Check your phone for the M-Pesa prompt and enter your PIN.</small>
                </div>
            </div>
        </div>
        '''
