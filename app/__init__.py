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

    from app.blueprints.media import media_bp
    app.register_blueprint(media_bp)

    from app.blueprints.giving import giving_bp
    app.register_blueprint(giving_bp)

    from app.blueprints.api import api_bp
    app.register_blueprint(api_bp)

    from app.blueprints.prayer import prayer_bp
    app.register_blueprint(prayer_bp)

    from app.blueprints.events import events_bp
    app.register_blueprint(events_bp)

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

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        from flask import render_template
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden(e):
        from flask import render_template
        return render_template('errors/403.html'), 403

    # CLI command to seed default admin
    @app.cli.command('seed-admin')
    def seed_admin():
        """Create default admin user if none exists."""
        from app.models.user import User
        if User.query.first():
            print('Admin user already exists. Skipping.')
            return
        admin = User(
            email='admin@gmail.com',
            display_name='Admin',
            role='admin',
        )
        admin.set_password('admin001')
        db.session.add(admin)
        db.session.commit()
        print('Default admin created: admin@gmail.com / admin001')

    return app
