from datetime import datetime
from sqlite3 import IntegrityError
from flask import get_flashed_messages, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user

from application import db
from .forms import ChangePasswordForm, LoginForm, RegistrationForm, UpdateAccountForm

from application.auth.models import User
from application.auth.utility_for_saving_imgs import save_picture
from . import auth_blueprint

@auth_blueprint.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response


@auth_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You already have an account!', 'success')
        return redirect(url_for('auth.info'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account successfully created for {form.username.data}!', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash(f'Something went wrong', 'danger')
    return render_template('register.html', form=form, title='Register')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You already logged in!', 'success')
        return redirect(url_for('info.info'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in successfully to Account Page!', 'success')
            return redirect(url_for('auth.account'))
        else:
            flash('Invalid username or password', 'warning')

    return render_template('login.html', form=form)

@auth_blueprint.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('auth.account'))

    elif request.method == 'GET':
        update_account_form.username.data = current_user.username
        update_account_form.email.data = current_user.email
        update_account_form.about_me.data =  current_user.about_me

    return render_template('account.html', update_account_form=update_account_form, change_password_form=change_password_form)

@auth_blueprint.route('/change-password', methods=["GET", "POST"])
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

        return redirect(url_for('auth.account'))

    return render_template('account.html', change_password_form=form, update_account_form=UpdateAccountForm())

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('auth.login'))