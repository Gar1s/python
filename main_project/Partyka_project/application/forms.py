from email.message import EmailMessage
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import EmailField, FileField, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp
from flask_wtf.file import FileField, FileAllowed

from application.models import User

class LoginForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(message="This field is required."), Email(message="Invalid email.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[
        DataRequired(message="This field is required."),
        Length(min=4, max=14, message='Username must be between 4 and 14 characters.'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots, or underscores')
    ])
    email = EmailField('Email', validators=[
        DataRequired(message="This field is required."),
        Email(message="Invalid email.")
    ])
    password = PasswordField(label='Password', validators=[
        DataRequired(message="This field is required."),
        Length(min=6, message='Password must be more than 6 characters long')
    ])
    confirm_password = PasswordField(label='Confirm password', validators=[
        DataRequired(message="This field is required."),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Sign up')
    
    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Username already exists. Choose a different one.')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email already exists. Please use a different one.')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
        Length(min=4, max=14, message='Username must be between 4 and 14 characters.'), 
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots, or underscores')
    ])
    email = StringField('Email', validators=[Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=240)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class ChangePasswordForm(FlaskForm):
    # current_password = PasswordField('Current Password', validators=[DataRequired()])
    # new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=4, max=10)])
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    # submit = SubmitField('Change Password')
    current_password = PasswordField(label='Current Password', validators=[DataRequired(message="This field is required."), Length(min=6, message='Password must be more than 6 characters long')])
    new_password = PasswordField(label='New Password', validators=[DataRequired(message="This field is required."), Length(min=6, message='Password must be more than 6 characters long')])
    confirm_password = PasswordField(label='Confirm New Password', validators=[DataRequired(message="This field is required."), Length(min=6, message='Password must be more than 6 characters long')])
    submit = SubmitField("Change Password")

    def validate_current_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Incorrect current password. Please try again.')

class TodoForm(FlaskForm):
    title = StringField("Enter a task here", validators=[DataRequired(message="This field is required.")])
    description = StringField('Describe your task', validators=[DataRequired(message="This field is required.")])
    submit = SubmitField("Save")