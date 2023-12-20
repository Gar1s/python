from flask import Blueprint

phone_call_api_bp = Blueprint('phone_call', __name__, url_prefix='/api/phone_call')

from . import views