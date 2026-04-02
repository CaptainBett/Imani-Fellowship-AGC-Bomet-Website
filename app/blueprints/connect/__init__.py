from flask import Blueprint

connect_bp = Blueprint('connect', __name__, template_folder='../../templates/connect')

from app.blueprints.connect import routes  # noqa: E402, F401
