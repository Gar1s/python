from flask import get_flashed_messages, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from . import info_blueprint

@info_blueprint.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    print(get_flashed_messages(True))
    username = current_user.username
    return render_template("info.html", username=username)

@info_blueprint.route('/clearcookies', methods=["POST"])
def clearcookies():
    response = redirect(url_for("info.info"))
    for cookie in request.cookies:
        response.delete_cookie(cookie)
    flash("Deleted all cookies", "danger")
    return response

@info_blueprint.route('/setcookie', methods=["POST"])
def setcookie():
    response = redirect(url_for("info.info"))
    if request.form.get("key", ""):
        key = request.form.get("key")
        value = request.form.get("value", "")
        max_age = request.form.get("max_age", 0, type=int)
        response.set_cookie(key, value, max_age)
        flash(f"Set cookie \"{key}\" to \"{value}\" with max-age \"{max_age}\"", "success")
    else:
        flash("Cookie key must be provided", "danger")
    return response

@info_blueprint.route('/deletecookie', methods=["POST"])
def deletecookie():
    response = redirect(url_for("info.info"))
    if request.form.get("key", ""):
        key = request.form.get("key")
        response.delete_cookie(key)
        flash(f"Deleted cookie \"{key}\"", "danger")
    else:
        flash("Cookie key must be provided", "danger")
    return response