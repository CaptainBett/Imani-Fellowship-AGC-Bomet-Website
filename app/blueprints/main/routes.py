from datetime import datetime, timezone
from flask import render_template
from app.blueprints.main import main_bp
from app.models.site_setting import SiteSetting
from app.models.announcement import Announcement
from app.models.event import Event
from app.models.team_member import TeamMember
from app.models.ministry import Ministry
from app.models.construction import ConstructionUpdate, FundraisingGroup


@main_bp.route('/')
def home():
    year_theme = SiteSetting.get('year_theme', 'Walking in Faith')
    year_theme_verse = SiteSetting.get('year_theme_verse', '')

    # Latest 3 published announcements
    announcements = Announcement.query.filter_by(is_published=True).order_by(
        Announcement.published_at.desc()
    ).limit(3).all()

    # Next 3 upcoming events
    upcoming_events = Event.query.filter(
        Event.is_published.is_(True),
        Event.start_datetime > datetime.now(timezone.utc),
    ).order_by(Event.start_datetime).limit(3).all()

    # Active ministries for homepage cards
    ministries = Ministry.query.filter_by(is_active=True).order_by(
        Ministry.sort_order, Ministry.name
    ).limit(8).all()

    return render_template(
        'main/home.html',
        year_theme=year_theme,
        year_theme_verse=year_theme_verse,
        announcements=announcements,
        upcoming_events=upcoming_events,
        ministries=ministries,
    )


@main_bp.route('/about')
def about():
    pastoral_team = TeamMember.query.filter_by(
        category='pastoral', is_active=True
    ).order_by(TeamMember.sort_order).all()

    elders = TeamMember.query.filter_by(
        category='elder', is_active=True
    ).order_by(TeamMember.sort_order).all()

    return render_template(
        'main/about.html',
        pastoral_team=pastoral_team,
        elders=elders,
    )


@main_bp.route('/construction')
def construction():
    updates = ConstructionUpdate.query.order_by(
        ConstructionUpdate.sort_order, ConstructionUpdate.created_at.desc()
    ).all()
    groups = FundraisingGroup.query.filter_by(is_active=True).order_by(
        FundraisingGroup.sort_order, FundraisingGroup.name
    ).all()
    total_target = sum(g.target_amount or 0 for g in groups)
    total_raised = sum(g.raised_amount or 0 for g in groups)
    return render_template(
        'main/construction.html',
        updates=updates, groups=groups,
        total_target=total_target, total_raised=total_raised,
    )
