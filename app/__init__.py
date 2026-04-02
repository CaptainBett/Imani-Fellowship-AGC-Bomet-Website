import os
from flask import Flask
from config import config
from app.extensions import db, migrate, login_manager, csrf, mail


def create_app(config_name=None):
    """Application factory."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register blueprints
    from app.blueprints.main import main_bp
    app.register_blueprint(main_bp)

    from app.blueprints.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.blueprints.admin_panel import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.blueprints.ministries import ministries_bp
    app.register_blueprint(ministries_bp)

    from app.blueprints.connect import connect_bp
    app.register_blueprint(connect_bp)

    # Import models so Flask-Migrate can detect them
    from app import models  # noqa: F401

    # Context processor for templates — injects site settings globally
    @app.context_processor
    def inject_globals():
        from datetime import datetime
        from app.models.site_setting import SiteSetting
        return {
            'now': datetime.now,
            'site': {
                'whatsapp_number': SiteSetting.get('whatsapp_number', ''),
                'church_phone': SiteSetting.get('church_phone', '+254 XXX XXX XXX'),
                'church_email': SiteSetting.get('church_email', 'info@imanifellowship.co.ke'),
                'facebook_url': SiteSetting.get('facebook_url', ''),
                'youtube_url': SiteSetting.get('youtube_url', ''),
                'instagram_url': SiteSetting.get('instagram_url', ''),
                'twitter_url': SiteSetting.get('twitter_url', ''),
            },
        }

    return app
