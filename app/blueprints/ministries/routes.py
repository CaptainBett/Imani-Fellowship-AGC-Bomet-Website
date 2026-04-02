from flask import render_template, abort
from app.blueprints.ministries import ministries_bp
from app.models.ministry import Ministry
from app.models.fellowship import Fellowship


@ministries_bp.route('/ministries')
def index():
    ministries = Ministry.query.filter_by(is_active=True).order_by(
        Ministry.sort_order, Ministry.name
    ).all()
    return render_template('ministries/index.html', ministries=ministries)


@ministries_bp.route('/ministries/<slug>')
def detail(slug):
    ministry = Ministry.query.filter_by(slug=slug, is_active=True).first_or_404()
    sections = ministry.content_sections.all()
    team = ministry.team_members.filter_by(is_active=True).order_by('sort_order').all()
    return render_template(
        'ministries/detail.html',
        ministry=ministry,
        sections=sections,
        team=team,
    )


@ministries_bp.route('/fellowships')
def fellowships():
    fellowships = Fellowship.query.filter_by(is_active=True).order_by(Fellowship.name).all()
    return render_template('fellowships/index.html', fellowships=fellowships)
