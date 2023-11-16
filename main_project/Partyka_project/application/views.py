from datetime import datetime
import os
from sqlite3 import IntegrityError
from flask import get_flashed_messages, request, render_template, redirect, url_for, make_response, session, flash
from flask_login import current_user, login_required, login_user, logout_user
from application import app, db
from application import credentials
from application.forms import ChangePasswordForm, LoginForm, RegistrationForm, TodoForm, UpdateAccountForm

from application.models import Todo, User
from application.utility_for_saving_imgs import save_picture


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

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You already have an account!', 'success')
        return redirect(url_for('info'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account successfully created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash(f'Something went wrong', 'danger')
    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You already logged in!', 'success')
        return redirect(url_for('info'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in successfully to Info Page!', 'success')
            return redirect(url_for('info'))
        else:
            flash('Invalid username or password', 'warning')

    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    print(get_flashed_messages(True))
    update_account_form = UpdateAccountForm()
    change_password_form = ChangePasswordForm()

    if update_account_form.validate_on_submit():
        if update_account_form.picture.data:
            current_user.image_file = save_picture(update_account_form.picture.data)
        try:
            current_user.username = update_account_form.username.data
            current_user.email = update_account_form.email.data
            current_user.about_me = update_account_form.about_me.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
        except:
            db.session.rollback()
            flash("Failed to update!", category="danger") 
        return redirect(url_for('account'))

    elif request.method == 'GET':
        update_account_form.username.data = current_user.username
        update_account_form.email.data = current_user.email
        update_account_form.about_me.data =  current_user.about_me

    return render_template('account.html', update_account_form=update_account_form, change_password_form=change_password_form)

@app.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    print(get_flashed_messages(True))
    username = current_user.username
    return render_template("info.html", username=username)

@app.route('/change-password', methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        new_password = form.new_password.data
        try:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash("Failed to update!", category="danger")

        return redirect(url_for('account'))

    return render_template('account.html', change_password_form=form, update_account_form=UpdateAccountForm())

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
        flash(f"Deleted cookie \"{key}\"", "danger")
    else:
        flash("Cookie key must be provided", "danger")
    return response

@app.route('/clearcookies', methods=["POST"])
def clearcookies():
    response = redirect(url_for("info"))
    for cookie in request.cookies:
        response.delete_cookie(cookie)
    flash("Deleted all cookies", "danger")
    return response

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    form = TodoForm()
    todo_list = Todo.query.all()
    return render_template("todo.html", form=form, todo_list=todo_list)

@app.route('/add', methods=["POST"])
def add():
    form = TodoForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        new_todo = Todo(title=title, description=description, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo added successfully', 'success')
    else:
        flash('Invalid input. Please try again.', 'danger')

    return redirect(url_for("todo"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    flash('Todo updated successfully', 'success')
    return redirect(url_for('todo'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully', 'success')
    return redirect(url_for('todo'))

@app.route('/users')
def users():
    users = User.query.all()
    total_users = len(users)
    return render_template('users.html', users=users, total_users=total_users)

@app.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response