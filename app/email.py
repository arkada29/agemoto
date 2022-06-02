from app.models import Users
from flask_mail import Message
from flask import current_app
from app import create_app, render_template, mail
from threading import Thread

app = create_app()

def send_async_email(application, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, 
            args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user):
    token = Users.get_reset_password_token(user)
    send_email(
        '[Agemoto] Reset Your Password',
        sender=app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('reset_password.txt', user=user, token=token),
        html_body=render_template('reset_password.html', user=user, token=token)
    )