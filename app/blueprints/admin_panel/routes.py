from datetime import datetime, timezone
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.blueprints.admin_panel import admin_bp
from app.blueprints.admin_panel.forms import (
    AnnouncementForm, EventForm, TeamMemberForm, PageForm, SiteSettingsForm,
    MinistryForm, MinistryContentForm, FellowshipForm, SermonForm, MediaItemForm,
    GivingCategoryForm,
)
from app.extensions import db
from app.models.announcement import Announcement
from app.models.event import Event
from app.models.team_member import TeamMember
from app.models.page import Page
from app.models.ministry import Ministry, MinistryContent
from app.models.fellowship import Fellowship
from app.models.connection_card import ConnectionCard
from app.models.volunteer import VolunteerSignup
from app.models.sermon import Sermon
from app.models.media import MediaItem
from app.models.giving import GivingCategory, Donation
from app.models.prayer_request import PrayerRequest
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
    sermon_count = Sermon.query.filter_by(is_published=True).count()
    media_count = MediaItem.query.filter_by(is_published=True).count()
    donation_count = Donation.query.filter_by(status='completed').count()
    return render_template(
        'admin/dashboard.html',
        announcement_count=announcement_count,
        event_count=event_count,
        team_count=team_count,
        sermon_count=sermon_count,
        media_count=media_count,
        donation_count=donation_count,
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


# ─── Ministries ───────────────────────────────────────────────────────────────

@admin_bp.route('/ministries')
@login_required
def ministries_list():
    ministries = Ministry.query.order_by(Ministry.sort_order, Ministry.name).all()
    return render_template('admin/ministries/list.html', ministries=ministries)


@admin_bp.route('/ministries/create', methods=['GET', 'POST'])
@login_required
def ministries_create():
    form = MinistryForm()
    if form.validate_on_submit():
        slug = form.slug.data or form.name.data.lower().replace(' ', '-').replace("'", '')
        if Ministry.query.filter_by(slug=slug).first():
            flash('A ministry with this slug already exists.', 'danger')
            return render_template('admin/ministries/form.html', form=form, editing=False)

        ministry = Ministry(
            name=form.name.data,
            slug=slug,
            description=form.description.data,
            icon=form.icon.data or 'bi-collection',
            sort_order=form.sort_order.data or 0,
            is_active=form.is_active.data,
        )

        if form.image.data:
            ministry.image_url = save_image(form.image.data, 'ministries')

        db.session.add(ministry)
        db.session.commit()
        flash('Ministry created successfully.', 'success')
        return redirect(url_for('admin_panel.ministries_list'))

    return render_template('admin/ministries/form.html', form=form, editing=False)


@admin_bp.route('/ministries/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def ministries_edit(id):
    ministry = Ministry.query.get_or_404(id)
    form = MinistryForm(obj=ministry)

    if form.validate_on_submit():
        ministry.name = form.name.data
        ministry.description = form.description.data
        ministry.icon = form.icon.data or 'bi-collection'
        ministry.sort_order = form.sort_order.data or 0
        ministry.is_active = form.is_active.data

        if form.image.data:
            delete_image(ministry.image_url)
            ministry.image_url = save_image(form.image.data, 'ministries')

        db.session.commit()
        flash('Ministry updated successfully.', 'success')
        return redirect(url_for('admin_panel.ministries_list'))

    return render_template('admin/ministries/form.html', form=form, editing=True, item=ministry)


@admin_bp.route('/ministries/<int:id>/delete', methods=['POST'])
@login_required
def ministries_delete(id):
    ministry = Ministry.query.get_or_404(id)
    delete_image(ministry.image_url)
    db.session.delete(ministry)
    db.session.commit()
    flash('Ministry deleted.', 'success')
    return redirect(url_for('admin_panel.ministries_list'))


@admin_bp.route('/ministries/<int:id>/content/add', methods=['GET', 'POST'])
@login_required
def ministry_content_add(id):
    ministry = Ministry.query.get_or_404(id)
    form = MinistryContentForm()

    if form.validate_on_submit():
        section = MinistryContent(
            ministry_id=ministry.id,
            title=form.title.data,
            body=form.body.data,
            sort_order=form.sort_order.data or 0,
        )
        if form.image.data:
            section.image_url = save_image(form.image.data, 'ministries')
        db.session.add(section)
        db.session.commit()
        flash('Content section added.', 'success')
        return redirect(url_for('admin_panel.ministries_edit', id=ministry.id))

    return render_template('admin/ministries/content_form.html', form=form, ministry=ministry, editing=False)


@admin_bp.route('/ministries/content/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def ministry_content_edit(id):
    section = MinistryContent.query.get_or_404(id)
    form = MinistryContentForm(obj=section)

    if form.validate_on_submit():
        section.title = form.title.data
        section.body = form.body.data
        section.sort_order = form.sort_order.data or 0
        if form.image.data:
            delete_image(section.image_url)
            section.image_url = save_image(form.image.data, 'ministries')
        db.session.commit()
        flash('Content section updated.', 'success')
        return redirect(url_for('admin_panel.ministries_edit', id=section.ministry_id))

    return render_template('admin/ministries/content_form.html', form=form,
                           ministry=section.ministry, editing=True, item=section)


@admin_bp.route('/ministries/content/<int:id>/delete', methods=['POST'])
@login_required
def ministry_content_delete(id):
    section = MinistryContent.query.get_or_404(id)
    ministry_id = section.ministry_id
    delete_image(section.image_url)
    db.session.delete(section)
    db.session.commit()
    flash('Content section removed.', 'success')
    return redirect(url_for('admin_panel.ministries_edit', id=ministry_id))


# ─── Fellowships ──────────────────────────────────────────────────────────────

@admin_bp.route('/fellowships')
@login_required
def fellowships_list():
    fellowships = Fellowship.query.order_by(Fellowship.name).all()
    return render_template('admin/fellowships/list.html', fellowships=fellowships)


@admin_bp.route('/fellowships/create', methods=['GET', 'POST'])
@login_required
def fellowships_create():
    form = FellowshipForm()
    if form.validate_on_submit():
        slug = form.slug.data or form.name.data.lower().replace(' ', '-')
        fellowship = Fellowship(
            name=form.name.data,
            slug=slug,
            description=form.description.data,
            meeting_day=form.meeting_day.data or None,
            meeting_time=form.meeting_time.data,
            location=form.location.data,
            contact_person=form.contact_person.data,
            contact_phone=form.contact_phone.data,
            is_active=form.is_active.data,
        )
        if form.image.data:
            fellowship.image_url = save_image(form.image.data, 'fellowships')
        db.session.add(fellowship)
        db.session.commit()
        flash('Fellowship created successfully.', 'success')
        return redirect(url_for('admin_panel.fellowships_list'))

    return render_template('admin/fellowships/form.html', form=form, editing=False)


@admin_bp.route('/fellowships/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def fellowships_edit(id):
    fellowship = Fellowship.query.get_or_404(id)
    form = FellowshipForm(obj=fellowship)

    if form.validate_on_submit():
        fellowship.name = form.name.data
        fellowship.description = form.description.data
        fellowship.meeting_day = form.meeting_day.data or None
        fellowship.meeting_time = form.meeting_time.data
        fellowship.location = form.location.data
        fellowship.contact_person = form.contact_person.data
        fellowship.contact_phone = form.contact_phone.data
        fellowship.is_active = form.is_active.data

        if form.image.data:
            delete_image(fellowship.image_url)
            fellowship.image_url = save_image(form.image.data, 'fellowships')

        db.session.commit()
        flash('Fellowship updated successfully.', 'success')
        return redirect(url_for('admin_panel.fellowships_list'))

    return render_template('admin/fellowships/form.html', form=form, editing=True, item=fellowship)


@admin_bp.route('/fellowships/<int:id>/delete', methods=['POST'])
@login_required
def fellowships_delete(id):
    fellowship = Fellowship.query.get_or_404(id)
    delete_image(fellowship.image_url)
    db.session.delete(fellowship)
    db.session.commit()
    flash('Fellowship deleted.', 'success')
    return redirect(url_for('admin_panel.fellowships_list'))


# ─── Connection Cards (view only) ────────────────────────────────────────────

@admin_bp.route('/connection-cards')
@login_required
def connection_cards_list():
    page = request.args.get('page', 1, type=int)
    cards = ConnectionCard.query.order_by(
        ConnectionCard.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/connection_cards/list.html', cards=cards)


@admin_bp.route('/connection-cards/<int:id>/delete', methods=['POST'])
@login_required
def connection_cards_delete(id):
    card = ConnectionCard.query.get_or_404(id)
    db.session.delete(card)
    db.session.commit()
    flash('Connection card removed.', 'success')
    return redirect(url_for('admin_panel.connection_cards_list'))


# ─── Volunteer Sign-ups (view only) ──────────────────────────────────────────

@admin_bp.route('/volunteers')
@login_required
def volunteers_list():
    page = request.args.get('page', 1, type=int)
    signups = VolunteerSignup.query.order_by(
        VolunteerSignup.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/volunteers/list.html', signups=signups)


@admin_bp.route('/volunteers/<int:id>/status', methods=['POST'])
@login_required
def volunteers_update_status(id):
    signup = VolunteerSignup.query.get_or_404(id)
    new_status = request.form.get('status', 'new')
    if new_status in ('new', 'contacted', 'active'):
        signup.status = new_status
        db.session.commit()
        flash(f'Status updated to {new_status}.', 'success')
    return redirect(url_for('admin_panel.volunteers_list'))


# ─── Sermons & Devotionals ───────────────────────────────────────────────────

@admin_bp.route('/sermons')
@login_required
def sermons_list():
    page = request.args.get('page', 1, type=int)
    content_type = request.args.get('type', '')
    query = Sermon.query
    if content_type in ('sermon', 'devotional', 'note'):
        query = query.filter_by(content_type=content_type)
    sermons = query.order_by(Sermon.sermon_date.desc().nullslast(), Sermon.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/sermons/list.html', sermons=sermons, current_type=content_type)


@admin_bp.route('/sermons/create', methods=['GET', 'POST'])
@login_required
def sermons_create():
    form = SermonForm()
    if form.validate_on_submit():
        sermon = Sermon(
            title=form.title.data,
            speaker=form.speaker.data,
            series=form.series.data,
            scripture_reference=form.scripture_reference.data,
            excerpt=form.excerpt.data,
            body=form.body.data,
            video_url=form.video_url.data or None,
            audio_url=form.audio_url.data or None,
            content_type=form.content_type.data,
            sermon_date=form.sermon_date.data,
            is_published=form.is_published.data,
            is_featured=form.is_featured.data,
        )
        sermon.generate_slug()

        if form.image.data:
            sermon.image_url = save_image(form.image.data, 'sermons')

        db.session.add(sermon)
        db.session.commit()
        flash('Sermon/devotional created successfully.', 'success')
        return redirect(url_for('admin_panel.sermons_list'))

    return render_template('admin/sermons/form.html', form=form, editing=False)


@admin_bp.route('/sermons/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def sermons_edit(id):
    sermon = Sermon.query.get_or_404(id)
    form = SermonForm(obj=sermon)

    if form.validate_on_submit():
        sermon.title = form.title.data
        sermon.speaker = form.speaker.data
        sermon.series = form.series.data
        sermon.scripture_reference = form.scripture_reference.data
        sermon.excerpt = form.excerpt.data
        sermon.body = form.body.data
        sermon.video_url = form.video_url.data or None
        sermon.audio_url = form.audio_url.data or None
        sermon.content_type = form.content_type.data
        sermon.sermon_date = form.sermon_date.data
        sermon.is_published = form.is_published.data
        sermon.is_featured = form.is_featured.data

        if form.image.data:
            delete_image(sermon.image_url)
            sermon.image_url = save_image(form.image.data, 'sermons')

        db.session.commit()
        flash('Sermon/devotional updated successfully.', 'success')
        return redirect(url_for('admin_panel.sermons_list'))

    return render_template('admin/sermons/form.html', form=form, editing=True, item=sermon)


@admin_bp.route('/sermons/<int:id>/delete', methods=['POST'])
@login_required
def sermons_delete(id):
    sermon = Sermon.query.get_or_404(id)
    delete_image(sermon.image_url)
    db.session.delete(sermon)
    db.session.commit()
    flash('Sermon/devotional deleted.', 'success')
    return redirect(url_for('admin_panel.sermons_list'))


# ─── Media Gallery ────────────────────────────────────────────────────────────

@admin_bp.route('/gallery')
@login_required
def gallery_list():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    query = MediaItem.query
    if category:
        query = query.filter_by(category=category)
    items = query.order_by(MediaItem.sort_order, MediaItem.created_at.desc()).paginate(
        page=page, per_page=24, error_out=False
    )
    return render_template('admin/gallery/list.html', items=items, current_category=category)


@admin_bp.route('/gallery/create', methods=['GET', 'POST'])
@login_required
def gallery_create():
    form = MediaItemForm()
    if form.validate_on_submit():
        item = MediaItem(
            title=form.title.data,
            description=form.description.data,
            media_type=form.media_type.data,
            category=form.category.data,
            sort_order=form.sort_order.data or 0,
            is_published=form.is_published.data,
        )

        if form.media_type.data == 'video':
            item.file_url = form.video_url.data
        elif form.image.data:
            item.file_url = save_image(form.image.data, 'gallery')
        else:
            flash('Please upload an image or provide a video URL.', 'danger')
            return render_template('admin/gallery/form.html', form=form, editing=False)

        db.session.add(item)
        db.session.commit()
        flash('Media item added.', 'success')
        return redirect(url_for('admin_panel.gallery_list'))

    return render_template('admin/gallery/form.html', form=form, editing=False)


@admin_bp.route('/gallery/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def gallery_edit(id):
    item = MediaItem.query.get_or_404(id)
    form = MediaItemForm(obj=item)
    if item.is_video:
        form.video_url.data = form.video_url.data or item.file_url

    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        item.media_type = form.media_type.data
        item.category = form.category.data
        item.sort_order = form.sort_order.data or 0
        item.is_published = form.is_published.data

        if form.media_type.data == 'video':
            item.file_url = form.video_url.data
        elif form.image.data:
            if item.is_image:
                delete_image(item.file_url)
            item.file_url = save_image(form.image.data, 'gallery')

        db.session.commit()
        flash('Media item updated.', 'success')
        return redirect(url_for('admin_panel.gallery_list'))

    return render_template('admin/gallery/form.html', form=form, editing=True, item=item)


@admin_bp.route('/gallery/<int:id>/delete', methods=['POST'])
@login_required
def gallery_delete(id):
    item = MediaItem.query.get_or_404(id)
    if item.is_image:
        delete_image(item.file_url)
    db.session.delete(item)
    db.session.commit()
    flash('Media item deleted.', 'success')
    return redirect(url_for('admin_panel.gallery_list'))


# ─── Giving Categories ────────────────────────────────────────────────────────

@admin_bp.route('/giving/categories')
@login_required
def giving_categories_list():
    categories = GivingCategory.query.order_by(GivingCategory.sort_order, GivingCategory.name).all()
    return render_template('admin/giving/categories.html', categories=categories)


@admin_bp.route('/giving/categories/create', methods=['GET', 'POST'])
@login_required
def giving_categories_create():
    form = GivingCategoryForm()
    if form.validate_on_submit():
        slug = form.slug.data or form.name.data.lower().replace(' ', '-')
        cat = GivingCategory(
            name=form.name.data,
            slug=slug,
            description=form.description.data,
            sort_order=form.sort_order.data or 0,
            is_active=form.is_active.data,
        )
        db.session.add(cat)
        db.session.commit()
        flash('Giving category created.', 'success')
        return redirect(url_for('admin_panel.giving_categories_list'))
    return render_template('admin/giving/category_form.html', form=form, editing=False)


@admin_bp.route('/giving/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def giving_categories_edit(id):
    cat = GivingCategory.query.get_or_404(id)
    form = GivingCategoryForm(obj=cat)
    if form.validate_on_submit():
        cat.name = form.name.data
        cat.description = form.description.data
        cat.sort_order = form.sort_order.data or 0
        cat.is_active = form.is_active.data
        db.session.commit()
        flash('Giving category updated.', 'success')
        return redirect(url_for('admin_panel.giving_categories_list'))
    return render_template('admin/giving/category_form.html', form=form, editing=True, item=cat)


@admin_bp.route('/giving/categories/<int:id>/delete', methods=['POST'])
@login_required
def giving_categories_delete(id):
    cat = GivingCategory.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    flash('Giving category deleted.', 'success')
    return redirect(url_for('admin_panel.giving_categories_list'))


# ─── Donations (view / reports) ──────────────────────────────────────────────

@admin_bp.route('/giving/donations')
@login_required
def donations_list():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    category_id = request.args.get('category', '', type=str)

    query = Donation.query
    if status in ('completed', 'pending', 'failed'):
        query = query.filter_by(status=status)
    if category_id:
        query = query.filter_by(category_id=int(category_id))

    donations = query.order_by(Donation.created_at.desc()).paginate(
        page=page, per_page=25, error_out=False
    )

    # Summary stats
    from sqlalchemy import func
    total_completed = db.session.query(func.sum(Donation.amount)).filter_by(status='completed').scalar() or 0
    total_count = Donation.query.filter_by(status='completed').count()

    categories = GivingCategory.query.order_by(GivingCategory.name).all()

    return render_template(
        'admin/giving/donations.html',
        donations=donations,
        current_status=status,
        current_category=category_id,
        categories=categories,
        total_completed=total_completed,
        total_count=total_count,
    )


# ─── Prayer Requests ─────────────────────────────────────────────────────────

@admin_bp.route('/prayer-requests')
@login_required
def prayer_requests_list():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    query = PrayerRequest.query
    if status in ('new', 'praying', 'answered'):
        query = query.filter_by(status=status)
    requests_list = query.order_by(PrayerRequest.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/prayer_requests/list.html',
                           requests=requests_list, current_status=status)


@admin_bp.route('/prayer-requests/<int:id>')
@login_required
def prayer_requests_detail(id):
    pr = PrayerRequest.query.get_or_404(id)
    return render_template('admin/prayer_requests/detail.html', pr=pr)


@admin_bp.route('/prayer-requests/<int:id>/status', methods=['POST'])
@login_required
def prayer_requests_update_status(id):
    pr = PrayerRequest.query.get_or_404(id)
    new_status = request.form.get('status', 'new')
    if new_status in ('new', 'praying', 'answered'):
        pr.status = new_status
        db.session.commit()
        flash(f'Status updated to {new_status}.', 'success')
    return redirect(url_for('admin_panel.prayer_requests_detail', id=id))


@admin_bp.route('/prayer-requests/<int:id>/notes', methods=['POST'])
@login_required
def prayer_requests_update_notes(id):
    pr = PrayerRequest.query.get_or_404(id)
    pr.notes = request.form.get('notes', '')
    db.session.commit()
    flash('Notes saved.', 'success')
    return redirect(url_for('admin_panel.prayer_requests_detail', id=id))


@admin_bp.route('/prayer-requests/<int:id>/delete', methods=['POST'])
@login_required
def prayer_requests_delete(id):
    pr = PrayerRequest.query.get_or_404(id)
    db.session.delete(pr)
    db.session.commit()
    flash('Prayer request removed.', 'success')
    return redirect(url_for('admin_panel.prayer_requests_list'))
