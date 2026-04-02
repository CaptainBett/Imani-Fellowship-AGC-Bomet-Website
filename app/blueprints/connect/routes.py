from flask import render_template, flash, redirect, url_for, request
from app.blueprints.connect import connect_bp
from app.blueprints.connect.forms import ConnectionCardForm, VolunteerForm
from app.extensions import db
from app.models.connection_card import ConnectionCard
from app.models.volunteer import VolunteerSignup
from app.models.ministry import Ministry
from app.models.page import Page


@connect_bp.route('/newcomers')
def newcomers():
    return render_template('connect/newcomers.html')


@connect_bp.route('/connect', methods=['GET', 'POST'])
def connection_card():
    form = ConnectionCardForm()

    if form.validate_on_submit():
        card = ConnectionCard(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            how_heard=form.how_heard.data or None,
            interests=form.interests.data,
            prayer_needs=form.prayer_needs.data,
            is_first_visit=form.is_first_visit.data,
        )
        db.session.add(card)
        db.session.commit()

        if request.headers.get('HX-Request'):
            return '<div class="alert alert-success"><i class="bi bi-check-circle"></i> Thank you! We\'re glad you\'re here. Someone from our team will reach out to you soon.</div>'

        flash('Thank you for connecting with us! We look forward to meeting you.', 'success')
        return redirect(url_for('connect.newcomers'))

    return render_template('connect/connection_card.html', form=form)


@connect_bp.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
    form = VolunteerForm()

    # Populate ministry choices dynamically
    ministries = Ministry.query.filter_by(is_active=True).order_by(Ministry.name).all()
    form.ministry_id.choices = [(0, 'Select a ministry')] + [(m.id, m.name) for m in ministries]

    if form.validate_on_submit():
        signup = VolunteerSignup(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            ministry_id=form.ministry_id.data if form.ministry_id.data != 0 else None,
            message=form.message.data,
        )
        db.session.add(signup)
        db.session.commit()

        if request.headers.get('HX-Request'):
            return '<div class="alert alert-success"><i class="bi bi-check-circle"></i> Thank you for signing up! Our team will be in touch with you soon.</div>'

        flash('Thank you for volunteering! We will contact you soon.', 'success')
        return redirect(url_for('connect.volunteer'))

    return render_template('connect/volunteer.html', form=form)


@connect_bp.route('/services')
def services():
    page = Page.get_by_slug('services')
    daycare_page = Page.get_by_slug('daycare')
    conference_page = Page.get_by_slug('conference-venue')
    return render_template(
        'connect/services.html',
        page=page,
        daycare_page=daycare_page,
        conference_page=conference_page,
    )
