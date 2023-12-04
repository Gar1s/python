from flask import Blueprint

todo_blueprint = Blueprint('todo', __name__, template_folder="templates")

from . import views