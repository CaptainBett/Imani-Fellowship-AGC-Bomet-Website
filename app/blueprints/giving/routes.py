from flask import render_template
from app.blueprints.giving import giving_bp
from app.models.giving import GivingCategory


@giving_bp.route('/give')
def give():
    categories = GivingCategory.query.filter_by(is_active=True).order_by(
        GivingCategory.sort_order, GivingCategory.name
    ).all()
    return render_template('giving/index.html', categories=categories)
