from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField

class ContactForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    subject = StringField("Subject")
    telephone = StringField("Telphone")
    message = TextAreaField("Message")
    submit = SubmitField("Submit")