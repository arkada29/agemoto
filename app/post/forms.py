from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=10, max=80, 
                        message='Cannot more than 80 characters')])
    # content = CKEditorField('Content')#, validators=[DataRequired()] 
    content = TextAreaField('Content')
    slug = StringField("Slug", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    description = StringField("Genre")
    platform = StringField('Platform')
    post_thumbnail = FileField("Thumbnail")
    post_upcoming = StringField("Collection Name")
    tags = StringField('Tags')
    news_type = StringField('News Type')
    submit = SubmitField("Submit")