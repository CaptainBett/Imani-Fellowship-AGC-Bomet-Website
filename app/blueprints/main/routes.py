from flask import render_template
from app.blueprints.main import main_bp
from app.models.site_setting import SiteSetting


@main_bp.route('/')
def home():
    year_theme = SiteSetting.get('year_theme', 'Walking in Faith')
    year_theme_verse = SiteSetting.get('year_theme_verse', '')
    whatsapp_number = SiteSetting.get('whatsapp_number', '')
    return render_template(
        'main/home.html',
        year_theme=year_theme,
        year_theme_verse=year_theme_verse,
        whatsapp_number=whatsapp_number,
    )


@main_bp.route('/about')
def about():
    return render_template('main/about.html')
