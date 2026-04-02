from flask import Blueprint

giving_bp = Blueprint('giving', __name__)

from app.blueprints.giving import routes  # noqa: E402, F401
