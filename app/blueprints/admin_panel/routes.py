from datetime import datetime, timezone
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.blueprints.admin_panel import admin_bp
from app.blueprints.admin_panel.forms import (
    AnnouncementForm, EventForm, TeamMemberForm, PageForm, SiteSettingsForm,
)
from app.extensions import db
from app.models.announcement import Announcement
from app.models.event import Event
from app.models.team_member import TeamMember
from app.models.page import Page
from app.models.site_setting import SiteSetting
from app.services.uploads import save_image, delete_image


# ─── Dashboard ────────────────────────────────────────────────────────────────

@admin_bp.route('/')
@login_required
def dashboard():
    announcement_count = Announcement.query.filter_by(is_published=True).count()
    event_count = Event.query.filter(
        Event.is_published.is_(True),
        Event.start_datetime > datetime.now(timezone.utc),
    ).count()
    team_count = TeamMember.query.filter_by(is_active=True).count()
    return render_template(
        'admin/dashboard.html',
        announcement_count=announcement_count,
        event_count=event_count,
        team_count=team_count,
    )


# ─── Announcements ────────────────────────────────────────────────────────────

@admin_bp.route('/announcements')
@login_required
def announcements_list():
    page = request.args.get('page', 1, type=int)
    announcements = Announcement.query.order_by(
        Announcement.created_at.desc()
    ).paginate(page=page, per_page=15, error_out=False)
    return render_template('admin/announcements/list.html', announcements=announcements)


@admin_bp.route('/announcements/create', methods=['GET', 'POST'])
@login_required
def announcements_create():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data,
            body=form.body.data,
            excerpt=form.excerpt.data,
            author_id=current_user.id,
        )
        announcement.generate_slug()

        if form.image.data:
            announcement.image_url = save_image(form.image.data, 'announcements')

        if form.is_published.data:
            announcement.publish()

        db.session.add(announcement)
        db.session.commit()
        flash('Announcement created successfully.', 'success')
        return redirect(url_for('admin_panel.announcements_list'))

    return render_template('admin/announcements/form.html', form=form, editing=False)


@admin_bp.route('/announcements/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def announcements_edit(id):
    announcement = Announcement.query.get_or_404(id)
    form = AnnouncementForm(obj=announcement)

    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.body = form.body.data
        announcement.excerpt = form.excerpt.data

        if form.image.data:
            delete_image(announcement.image_url)
            announcement.image_url = save_image(form.image.data, 'announcements')

        if form.is_published.data and not announcement.is_published:
            announcement.publish()
        elif not form.is_published.data:
            announcement.unpublish()

        db.session.commit()
        flash('Announcement updated successfully.', 'success')
        return redirect(url_for('admin_panel.announcements_list'))

    form.is_published.data = announcement.is_published
    return render_template('admin/announcements/form.html', form=form, editing=True, item=announcement)


@admin_bp.route('/announcements/<int:id>/delete', methods=['POST'])
@login_required
def announcements_delete(id):
    announcement = Announcement.query.get_or_404(id)
    delete_image(announcement.image_url)
    db.session.delete(announcement)
    db.session.commit()
    flash('Announcement deleted.', 'success')
    return redirect(url_for('admin_panel.announcements_list'))


# ─── Events ───────────────────────────────────────────────────────────────────

@admin_bp.route('/events')
@login_required
def events_list():
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.start_datetime.desc()).paginate(
        page=page, per_page=15, error_out=False
    )
    return render_template('admin/events/list.html', events=events)


@admin_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def events_create():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data,
            start_datetime=form.start_datetime.data,
            end_datetime=form.end_datetime.data,
            is_recurring=form.is_recurring.data,
            recurrence_rule=form.recurrence_rule.data or None,
            is_published=form.is_published.data,
        )

        if form.image.data:
            event.image_url = save_image(form.image.data, 'events')

        db.session.add(event)
        db.session.commit()
        flash('Event created successfully.', 'success')
        return redirect(url_for('admin_panel.events_list'))

    return render_template('admin/events/form.html', form=form, editing=False)


@admin_bp.route('/events/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def events_edit(id):
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)

    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.location = form.location.data
        event.start_datetime = form.start_datetime.data
        event.end_datetime = form.end_datetime.data
        event.is_recurring = form.is_recurring.data
        event.recurrence_rule = form.recurrence_rule.data or None
        event.is_published = form.is_published.data

        if form.image.data:
            delete_image(event.image_url)
            event.image_url = save_image(form.image.data, 'events')

        db.session.commit()
        flash('Event updated successfully.', 'success')
        return redirect(url_for('admin_panel.events_list'))

    return render_template('admin/events/form.html', form=form, editing=True, item=event)


@admin_bp.route('/events/<int:id>/delete', methods=['POST'])
@login_required
def events_delete(id):
    event = Event.query.get_or_404(id)
    delete_image(event.image_url)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.', 'success')
    return redirect(url_for('admin_panel.events_list'))


# ─── Team Members ─────────────────────────────────────────────────────────────

@admin_bp.route('/team')
@login_required
def team_list():
    members = TeamMember.query.order_by(TeamMember.sort_order, TeamMember.name).all()
    return render_template('admin/team/list.html', members=members)


@admin_bp.route('/team/create', methods=['GET', 'POST'])
@login_required
def team_create():
    form = TeamMemberForm()
    if form.validate_on_submit():
        member = TeamMember(
            name=form.name.data,
            title=form.title.data,
            bio=form.bio.data,
            category=form.category.data,
            sort_order=form.sort_order.data or 0,
            is_active=form.is_active.data,
        )

        if form.photo.data:
            member.photo_url = save_image(form.photo.data, 'team')

        db.session.add(member)
        db.session.commit()
        flash('Team member added successfully.', 'success')
        return redirect(url_for('admin_panel.team_list'))

    return render_template('admin/team/form.html', form=form, editing=False)


@admin_bp.route('/team/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def team_edit(id):
    member = TeamMember.query.get_or_404(id)
    form = TeamMemberForm(obj=member)

    if form.validate_on_submit():
        member.name = form.name.data
        member.title = form.title.data
        member.bio = form.bio.data
        member.category = form.category.data
        member.sort_order = form.sort_order.data or 0
        member.is_active = form.is_active.data

        if form.photo.data:
            delete_image(member.photo_url)
            member.photo_url = save_image(form.photo.data, 'team')

        db.session.commit()
        flash('Team member updated successfully.', 'success')
        return redirect(url_for('admin_panel.team_list'))

    return render_template('admin/team/form.html', form=form, editing=True, item=member)


@admin_bp.route('/team/<int:id>/delete', methods=['POST'])
@login_required
def team_delete(id):
    member = TeamMember.query.get_or_404(id)
    delete_image(member.photo_url)
    db.session.delete(member)
    db.session.commit()
    flash('Team member removed.', 'success')
    return redirect(url_for('admin_panel.team_list'))


# ─── Pages ────────────────────────────────────────────────────────────────────

@admin_bp.route('/pages')
@login_required
def pages_list():
    pages = Page.query.order_by(Page.slug).all()
    return render_template('admin/pages/list.html', pages=pages)


@admin_bp.route('/pages/create', methods=['GET', 'POST'])
@login_required
def pages_create():
    form = PageForm()
    if form.validate_on_submit():
        slug = form.title.data.lower().replace(' ', '-')
        if Page.query.filter_by(slug=slug).first():
            flash('A page with this title already exists.', 'danger')
            return render_template('admin/pages/form.html', form=form, editing=False)

        page = Page(
            slug=slug,
            title=form.title.data,
            content=form.content.data,
            meta_description=form.meta_description.data,
            updated_by=current_user.id,
        )
        db.session.add(page)
        db.session.commit()
        flash('Page created successfully.', 'success')
        return redirect(url_for('admin_panel.pages_list'))

    return render_template('admin/pages/form.html', form=form, editing=False)


@admin_bp.route('/pages/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def pages_edit(id):
    page = Page.query.get_or_404(id)
    form = PageForm(obj=page)

    if form.validate_on_submit():
        page.title = form.title.data
        page.content = form.content.data
        page.meta_description = form.meta_description.data
        page.updated_by = current_user.id
        db.session.commit()
        flash('Page updated successfully.', 'success')
        return redirect(url_for('admin_panel.pages_list'))

    return render_template('admin/pages/form.html', form=form, editing=True, item=page)


@admin_bp.route('/pages/<int:id>/delete', methods=['POST'])
@login_required
def pages_delete(id):
    page = Page.query.get_or_404(id)
    db.session.delete(page)
    db.session.commit()
    flash('Page deleted.', 'success')
    return redirect(url_for('admin_panel.pages_list'))


# ─── Site Settings ────────────────────────────────────────────────────────────

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SiteSettingsForm()

    if form.validate_on_submit():
        settings_map = {
            'year_theme': form.year_theme.data,
            'year_theme_verse': form.year_theme_verse.data,
            'whatsapp_number': form.whatsapp_number.data,
            'church_phone': form.church_phone.data,
            'church_email': form.church_email.data,
            'facebook_url': form.facebook_url.data,
            'youtube_url': form.youtube_url.data,
            'instagram_url': form.instagram_url.data,
            'twitter_url': form.twitter_url.data,
        }
        for key, value in settings_map.items():
            SiteSetting.set(key, value or '')
        flash('Settings saved successfully.', 'success')
        return redirect(url_for('admin_panel.settings'))

    # Pre-fill form with current values
    form.year_theme.data = SiteSetting.get('year_theme')
    form.year_theme_verse.data = SiteSetting.get('year_theme_verse')
    form.whatsapp_number.data = SiteSetting.get('whatsapp_number')
    form.church_phone.data = SiteSetting.get('church_phone')
    form.church_email.data = SiteSetting.get('church_email')
    form.facebook_url.data = SiteSetting.get('facebook_url')
    form.youtube_url.data = SiteSetting.get('youtube_url')
    form.instagram_url.data = SiteSetting.get('instagram_url')
    form.twitter_url.data = SiteSetting.get('twitter_url')

    return render_template('admin/settings.html', form=form)
