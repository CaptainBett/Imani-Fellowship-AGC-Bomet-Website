from flask import Blueprint

prayer_bp = Blueprint('prayer', __name__)

from app.blueprints.prayer import routes  # noqa: E402, F401
