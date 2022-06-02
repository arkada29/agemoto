from wsgiref.validate import validator
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Change')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
                'Repeat Password', validators=[DataRequired(), EqualTo('password')]
                )
    submit = SubmitField('Request Password Reset')