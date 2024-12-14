from flask import Blueprint

mainBP = Blueprint('main', __name__, template_folder='templates', static_folder='static', url_prefix="/picture-time")

from . import routes