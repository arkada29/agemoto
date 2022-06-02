from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, InputRequired, ValidationError
from flask_wtf.file import FileField

USER_LEVEL = ('Admin', 'Reguler', 'VIP')

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")

#register form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    # fav_color = StringField("Fav_Color")
    about_author = TextAreaField("About Author")
    password_hash = PasswordField('Password', validators=[DataRequired(), 
                    EqualTo('password_hash_match', message='Password Must Match!'),
                    Length(min=8, max=16)])
    password_hash_match = PasswordField('Confirm Password', validators=[DataRequired()])
    profile_pic = FileField("Profile Picture")
    # level = StringField('User Level', default='Reguler')
    level = SelectField(label='Level', choices=[u for u in USER_LEVEL])
    submit = SubmitField("Submit")

    def validate_username(self,username):
        excluded_char = "*?!'^+%&/()=}][{$#"
        for char in self.username.data:
            if char in excluded_char:
                raise ValidationError(f'Character {char} is not allowed on username')

    def validate_email(self, email):
        included_char = "@"
        # for char in self.email.data:
        #     if '@' != char:
        if included_char not in self.email.data:
            raise ValidationError(f"Must include proper {included_char} character")