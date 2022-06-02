from app import create_app, db
from app.password_change import bp
from app.password_change.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
from flask_login import current_user
from flask import redirect, url_for, flash, render_template
from app.models import Users

@bp.route('/change_password', methods=['GET','POST'])
def change_pwd():    
    if current_user.is_authenticated:
        return redirect(url_for('base.page_root'))
    form=ResetPasswordRequestForm()
    if form.validate_on_submit():
        email=form.email.data
        user = Users.query.filter_by(email=email).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
            return redirect(url_for('user.login'))
    return render_template('password_change.html', form=form, title='Reset Password')   

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('base.page_root'))
    user = Users.verify_reset_password(token)
    if not user:
        return redirect(url_for('base.page_root'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('user.login'))
    return render_template('reset_password.html', form=form)
