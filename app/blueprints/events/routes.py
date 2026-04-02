import calendar
from datetime import datetime, timezone
from flask import render_template, request
from app.blueprints.events import events_bp
from app.models.event import Event


@events_bp.route('/events')
def events_index():
    """Public events page with calendar and upcoming list."""
    # Determine which month to display
    today = datetime.now(timezone.utc)
    try:
        year = int(request.args.get('year', today.year))
        month = int(request.args.get('month', today.month))
    except (ValueError, TypeError):
        year, month = today.year, today.month

    # Clamp month to valid range
    if month < 1:
        month, year = 12, year - 1
    elif month > 12:
        month, year = 1, year + 1

    # Get events for this month
    first_day = datetime(year, month, 1)
    last_day_num = calendar.monthrange(year, month)[1]
    last_day = datetime(year, month, last_day_num, 23, 59, 59)

    month_events = Event.query.filter(
        Event.is_published.is_(True),
        Event.start_datetime >= first_day,
        Event.start_datetime <= last_day,
    ).order_by(Event.start_datetime).all()

    # Build calendar grid
    cal = calendar.Calendar(firstweekday=0)  # Monday first
    month_days = cal.monthdayscalendar(year, month)

    # Map events to days
    events_by_day = {}
    for ev in month_events:
        day = ev.start_datetime.day
        events_by_day.setdefault(day, []).append(ev)

    # Navigation
    prev_month = month - 1
    prev_year = year
    if prev_month < 1:
        prev_month, prev_year = 12, year - 1

    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_month, next_year = 1, year + 1

    # Upcoming events (next 10)
    upcoming = Event.query.filter(
        Event.is_published.is_(True),
        Event.start_datetime >= datetime.now(timezone.utc),
    ).order_by(Event.start_datetime).limit(10).all()

    is_htmx = request.headers.get('HX-Request')

    template = 'events/_calendar.html' if is_htmx else 'events/index.html'

    return render_template(
        template,
        month_days=month_days,
        events_by_day=events_by_day,
        year=year,
        month=month,
        month_name=calendar.month_name[month],
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
        today=today,
        upcoming=upcoming,
    )


@events_bp.route('/events/<int:id>')
def event_detail(id):
    event = Event.query.filter_by(id=id, is_published=True).first_or_404()
    return render_template('events/detail.html', event=event)
