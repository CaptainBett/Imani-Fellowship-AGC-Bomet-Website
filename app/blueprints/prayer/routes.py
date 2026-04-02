from flask import render_template, request, flash, redirect, url_for
from app.blueprints.prayer import prayer_bp
from app.blueprints.prayer.forms import PrayerRequestForm
from app.extensions import db
from app.models.prayer_request import PrayerRequest


@prayer_bp.route('/prayer', methods=['GET', 'POST'])
def prayer_request():
    form = PrayerRequestForm()

    if form.validate_on_submit():
        pr = PrayerRequest(
            name=form.name.data if not form.is_anonymous.data else None,
            email=form.email.data,
            phone=form.phone.data,
            request=form.request.data,
            is_anonymous=form.is_anonymous.data,
            is_public=form.is_public.data,
            status='new',
        )
        db.session.add(pr)
        db.session.commit()

        # HTMX response
        if request.headers.get('HX-Request'):
            return '''
            <div class="alert alert-success">
                <h5 class="alert-heading"><i class="bi bi-check-circle-fill"></i> Prayer Request Submitted</h5>
                <p class="mb-0">Thank you for sharing your prayer request. Our prayer team will be praying for you.</p>
            </div>
            '''

        flash('Your prayer request has been submitted. We are praying for you.', 'success')
        return redirect(url_for('prayer.prayer_request'))

    # Get public prayer requests for the prayer wall
    public_requests = PrayerRequest.query.filter_by(
        is_public=True
    ).order_by(PrayerRequest.created_at.desc()).limit(20).all()

    return render_template('prayer/index.html', form=form, public_requests=public_requests)
