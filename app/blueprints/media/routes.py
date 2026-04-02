from flask import render_template, request
from app.blueprints.media import media_bp
from app.models.sermon import Sermon
from app.models.media import MediaItem
from app.models.team_member import TeamMember


# ─── Sermons Archive ─────────────────────────────────────────────────────────

@media_bp.route('/sermons')
def sermons_index():
    page = request.args.get('page', 1, type=int)
    content_type = request.args.get('type', '')
    series = request.args.get('series', '')

    query = Sermon.query.filter_by(is_published=True)
    if content_type in ('sermon', 'devotional', 'note'):
        query = query.filter_by(content_type=content_type)
    if series:
        query = query.filter_by(series=series)

    sermons = query.order_by(
        Sermon.sermon_date.desc().nullslast(), Sermon.created_at.desc()
    ).paginate(page=page, per_page=12, error_out=False)

    # Get featured sermon
    featured = Sermon.query.filter_by(is_published=True, is_featured=True).order_by(
        Sermon.sermon_date.desc().nullslast()
    ).first()

    # Get unique series for filter
    all_series = [s[0] for s in
                  Sermon.query.with_entities(Sermon.series).filter(
                      Sermon.series.isnot(None), Sermon.series != '', Sermon.is_published.is_(True)
                  ).distinct().order_by(Sermon.series).all()]

    return render_template(
        'sermons/index.html',
        sermons=sermons,
        featured=featured,
        all_series=all_series,
        current_type=content_type,
        current_series=series,
    )


@media_bp.route('/sermons/<slug>')
def sermon_detail(slug):
    sermon = Sermon.query.filter_by(slug=slug, is_published=True).first_or_404()

    # Get next/prev for navigation
    prev_sermon = Sermon.query.filter(
        Sermon.is_published.is_(True),
        Sermon.sermon_date < sermon.sermon_date if sermon.sermon_date else Sermon.id < sermon.id
    ).order_by(Sermon.sermon_date.desc().nullslast()).first()

    next_sermon = Sermon.query.filter(
        Sermon.is_published.is_(True),
        Sermon.sermon_date > sermon.sermon_date if sermon.sermon_date else Sermon.id > sermon.id
    ).order_by(Sermon.sermon_date.asc().nullslast()).first()

    return render_template(
        'sermons/detail.html',
        sermon=sermon,
        prev_sermon=prev_sermon,
        next_sermon=next_sermon,
    )


# ─── HTMX Load More for Sermons ──────────────────────────────────────────────

@media_bp.route('/sermons/load-more')
def sermons_load_more():
    page = request.args.get('page', 1, type=int)
    content_type = request.args.get('type', '')

    query = Sermon.query.filter_by(is_published=True)
    if content_type in ('sermon', 'devotional', 'note'):
        query = query.filter_by(content_type=content_type)

    sermons = query.order_by(
        Sermon.sermon_date.desc().nullslast(), Sermon.created_at.desc()
    ).paginate(page=page, per_page=12, error_out=False)

    return render_template('sermons/_cards.html', sermons=sermons)


# ─── Gallery ─────────────────────────────────────────────────────────────────

@media_bp.route('/gallery')
def gallery_index():
    category = request.args.get('category', '')
    query = MediaItem.query.filter_by(is_published=True)
    if category:
        query = query.filter_by(category=category)

    items = query.order_by(MediaItem.sort_order, MediaItem.created_at.desc()).all()

    return render_template(
        'gallery/index.html',
        items=items,
        current_category=category,
    )


# ─── Choir Page ──────────────────────────────────────────────────────────────

@media_bp.route('/choir')
def choir():
    # Choir media (photos + videos)
    choir_media = MediaItem.query.filter_by(
        category='choir', is_published=True
    ).order_by(MediaItem.sort_order, MediaItem.created_at.desc()).all()

    # Choir team members
    choir_members = TeamMember.query.filter_by(
        category='choir', is_active=True
    ).order_by(TeamMember.sort_order, TeamMember.name).all()

    return render_template(
        'gallery/choir.html',
        choir_media=choir_media,
        choir_members=choir_members,
    )
