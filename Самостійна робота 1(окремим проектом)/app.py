from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    feedback = db.Column(db.Text, nullable=False)

class FeedbackForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    feedback = TextAreaField('Your Feedback', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        feedback_text = form.feedback.data
        feedback_entry = Feedback(name=name, feedback=feedback_text)
        db.session.add(feedback_entry)
        db.session.commit()
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('index'))
    feedback_entries = Feedback.query.all()
    return render_template('index.html', form=form, feedback_entries=feedback_entries)

if __name__ == '__main__':
    app.run()
    