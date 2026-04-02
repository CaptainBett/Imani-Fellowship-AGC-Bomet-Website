from flask import Blueprint

ministries_bp = Blueprint('ministries', __name__, template_folder='../../templates/ministries')

from app.blueprints.ministries import routes  # noqa: E402, F401
