from datetime import datetime
import os
from flask import get_flashed_messages, request, render_template, redirect, url_for, make_response, session, flash
from application import app, db
from application import credentials
from application.forms import ChangePasswordForm, LoginForm, RegistrationForm, TodoForm

from application.models import Todo


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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account successfully created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # if "username" in session:
    #     flash('Login successful!', 'success')
    #     return redirect(url_for('info'))

    if form.validate_on_submit():
        if form.email.data == "test@gmail.com" and form.password.data == '123456':
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful!', 'danger')

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

@app.route('/change-password', methods=["GET","POST"])
def change_password():
    username = session.get("username")

    if not username:
        flash("User not logged in", "danger")
        return redirect(url_for("login"))

    user = credentials.get_user_credentials(username)

    if user is None:
        flash(f"User \"{username}\" doesn't exist anymore", "danger")
        return redirect(url_for("info"))

    current_password = request.form.get("current-password", "")
    new_password = request.form.get("new-password", "")
    confirm_password = request.form.get("confirm-password", "")

    if not current_password or not new_password or not confirm_password:
        flash("All fields must be filled", "danger")
        return redirect(url_for("info"))

    if current_password != user["password"]:
        flash("Incorrect current password", "danger")
    elif new_password != confirm_password:
        flash("New and confirm passwords do not match", "danger")
    elif len(new_password) < 4 or len(new_password) > 10:
        flash("New password must be between 4 and 10 characters", "danger")
    else:
        if current_password == user["password"]:
            status = credentials.change_user_password(user, new_password)
            if status == 0:
                flash("Successfully changed password", "success")
            else:
                flash("Failed to change password", "danger")
        else:
            flash("Incorrect password was provided", "danger")

    return redirect(url_for("info"))

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