from wsgiref.validate import validator
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, DateField, TextAreaField
from wtforms.validators import DataRequired

class UpcomingForm(FlaskForm):
    name = StringField('Upcoming Name', validators = [DataRequired()])
    date_released = DateField('Release Date', validators = [DataRequired()])
    categories = StringField("Categories")
    platform = StringField("Platform/Type")
    cover_picture = FileField("Cover")
    thumbnail_picture = FileField("Thumbnail")
    publishers = StringField("Publisher")
    developers = StringField("Developer")
    genre = StringField("Genre")
    synopsis = TextAreaField("Synopsis")
    producer =  StringField("Director")
    studio =  StringField("Studios")
    series =  StringField("Series")
    engine =  StringField("Engine")
    mode =  StringField("Mode")
    episode =  StringField("Episodes")
    duration =  StringField("Duration")
    source =  StringField("Source")

    starring = StringField("Starring")
    boxoffice = StringField("Box Office")
    language = StringField("Language")
    budget = StringField("Budget")
    mpaa = StringField("MPAA")
    based = StringField("Based On")

    submit = SubmitField("Submit")
