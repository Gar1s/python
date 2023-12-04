from flask import Blueprint

info_blueprint = Blueprint('info', __name__, template_folder="templates")

from . import views