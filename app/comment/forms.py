from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    comment = StringField("Comment")
    submit = SubmitField("Submit")