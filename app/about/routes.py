from flask import render_template, redirect, url_for, flash
from app.about import bp
from app import current_app, db
from app.about.forms import ContactForm
from app.models import Contact
from flask_babel import _

@bp.route('/about-contact', methods=['POST', 'GET'])
def about_contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        name=''
        try:
            contact = Contact(
                name=contact_form.name.data,
                email=contact_form.email.data,
                subject=contact_form.subject.data,
                telephone=contact_form.telephone.data,
                message=contact_form.message.data
                )
            db.session.add(contact)
            db.session.commit()
            contact_form.name.data=""
            contact_form.email.data=""
            contact_form.subject.data=""
            contact_form.telephone.data=""
            contact_form.message.data=""
            flash(_("You're message has been submitted"))
            current_app.logger.info('%s adding user', name)
            return redirect(url_for("about.about_contact"))
        except Exception as e:
            db.session.rollback()
            flash(_('Sorry, somethings wrong we sorry for this'))
    return render_template('about_contact.html',
                            contact_form=contact_form)