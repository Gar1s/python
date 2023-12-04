from flask import render_template

from application.auth.models import User
from . import users_blueprint

@users_blueprint.route('/users')
def users():
    users = User.query.all()
    total_users = len(users)
    return render_template('users.html', users=users, total_users=total_users)
