from datetime import datetime
import os
from flask import get_flashed_messages, request, render_template, redirect, url_for, make_response, session, flash
from application import app
from application import credentials
from application.forms import LoginForm


my_skills = [
    {'id': 1, 'name': 'Python'},
    {'id': 2, 'name': 'Flask'},
    {'id': 3, 'name': 'HTML'},
    {'id': 4, 'name': 'CSS'},
]

@app.route('/')
def home():    
    return render_template('home.html', title='Main', os_info=os.name, 
		user_agent=request.headers.get('User-Agent'), current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/page1')
def page1():
    return render_template('page1.html', title='About Me', os_info=os.name, 
		user_agent=request.headers.get('User-Agent'), current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/skills')
def skills():
    return render_template('skills.html', my_skills=my_skills)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if "username" in session:
        flash('Login successful!', 'success')
        return redirect(url_for('info'))

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = credentials.get_user_credentials(username)

        if user is not None:
            username_match = user.get("username") == username
            password_match = user.get("password") == password

            if username_match and password_match:
                if form.remember.data:
                    session["username"] = username
                    flash('Login successful!', 'success')
                    return redirect(url_for('info'))
                return redirect('/')
            else:
                flash('Invalid password', 'danger')
        else:
            flash('User not found', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    response = redirect(url_for("login"))
    if "username" in session:
        session.pop("username")
    return response

@app.route('/info', methods=['GET', 'POST'])
def info():
    print(get_flashed_messages(True))
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))
    return render_template("info.html")

@app.route('/change-password', methods=["POST"])
def change_password():
    response = redirect(url_for("info"))

    current_password = request.form.get("current-password", "")
    new_password = request.form.get("new-password", "")
    confirm_password = request.form.get("confirm-password", "")

    if new_password != confirm_password:
        flash("New and confirm passwords do not match", "danger")
        return response

    if not new_password:
        flash("A new password must be provided", "danger")
        return response

    username = session["username"]
    user = credentials.get_user_credentials(username)
    if user is None:
        flash(f"User \"{username}\" doesn't exist anymore", "danger")
        return response

    if current_password == user["password"]:
        status = credentials.change_user_password(user, new_password)
        if status == 0:
            flash("Successfully changed password", "success")
            return response
        else:
            flash("Failed to change password", "danger")
            return response
    else:
        flash("Incorrect password was provided", "danger")
        return response

@app.route('/setcookie', methods=["POST"])
def setcookie():
    response = redirect(url_for("info"))
    if request.form.get("key", ""):
        key = request.form.get("key")
        value = request.form.get("value", "")
        max_age = request.form.get("max_age", 0, type=int)
        response.set_cookie(key, value, max_age)
        flash(f"Set cookie \"{key}\" to \"{value}\" with max-age \"{max_age}\"", "success")
    else:
        flash("Cookie key must be provided", "danger")
    return response

@app.route('/deletecookie', methods=["POST"])
def deletecookie():
    response = redirect(url_for("info"))
    if request.form.get("key", ""):
        key = request.form.get("key")
        response.delete_cookie(key)
        flash(f"Deleted cookie \"{key}\"", "success")
    else:
        flash("Cookie key must be provided", "danger")
    return response

@app.route('/clearcookies', methods=["POST"])
def clearcookies():
    response = redirect(url_for("info"))
    for cookie in request.cookies:
        response.delete_cookie(cookie)
    flash("Deleted all cookies", "success")
    return response