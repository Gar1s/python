from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed
from wtforms.widgets import CheckboxInput, ListWidget

type_choices = [("news", "News"), ("publication", "Publication"), ("other", "Other")]
enabled_choices = [(True, "True")]

class PostForm(FlaskForm):
    title = StringField(
        label="Title", validators=[DataRequired(message="This field is required.")]
    )
    text = TextAreaField(
        label="Write your post here",
        validators=[DataRequired(message="This field is required.")],
    )
    image = FileField(
        "Post Picture",
        validators=[FileAllowed(["jpg", "png"], message="This file is not allowed")],
    )
    type = SelectField(
        "Type",
        choices=type_choices,
        validators=[DataRequired(message="Please select a type.")],
    )
    category = SelectField('Category', validators=[DataRequired(message="This field is required.")])
    tags = SelectMultipleField('Tags', validators=[DataRequired(message="This field is required.")], coerce=int, option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    submit = SubmitField("Submit")


class EditPostForm(FlaskForm):
    title = StringField(
        label="Title", validators=[DataRequired(message="This field is required.")]
    )
    text = TextAreaField(
        label="Write your post here",
        validators=[DataRequired(message="This field is required.")],
    )
    image = FileField(
        "Post Picture",
        validators=[FileAllowed(["jpg", "png"], message="This file is not allowed")],
    )
    type = SelectField(
        "Type",
        choices=type_choices,
        validators=[DataRequired(message="Please select a type.")],
    )
    enabled = SelectField("Enabled", choices=enabled_choices)
    category = SelectField('Category', validators=[DataRequired(message="This field is required.")])
    tags = SelectMultipleField('Tags', validators=[DataRequired(message="This field is required.")], coerce=int, option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    submit = SubmitField("Submit")
    
class CategoryForm(FlaskForm):
    name = StringField("Category name",
                       validators=[DataRequired(message="This field is required."),])
    submit = SubmitField("Submit")
    
class EditCategoryForm(FlaskForm):
    name = StringField("Category name",
                       validators=[DataRequired(message="This field is required."),])
    submit = SubmitField("Submit")
