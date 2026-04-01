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

    # Import models so Flask-Migrate can detect them
    from app import models  # noqa: F401

    # Context processor for templates
    @app.context_processor
    def inject_globals():
        from datetime import datetime
        return {'now': datetime.now}

    return app
