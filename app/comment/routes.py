from app.models import Comments, Users
from app import create_app, db, current_app, login_manager
from app.comment import bp
from flask import request, url_for, render_template, flash, redirect
from flask_login import login_required, current_user

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@bp.route("/comment_list")
@login_required
def comment_list():
    comment_list = Comments.query.order_by(Comments.id_comment).all()
    page = request.args.get('page', 1, type=int)
    comment = Comments.query.order_by(Comments.id_comment.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('upcomings', page=comment.next_num) \
        if comment.has_next else None
    prev_url = url_for('upcomings', page=comment.prev_num) \
        if comment.has_prev else None
    return render_template("comment_list.html", comment_list=comment_list,
                            comment=comment.items,
                            next_url=next_url,
                            prev_url=prev_url
                            )

@bp.route("/comment_delete/<int:id>")
@login_required
def comment_delete(id):
    if current_user.level == 'Admin':
        comment_delete = Comments.query.get_or_404(id)
        try:
            db.session.delete(comment_delete)
            db.session.commit()
            flash("Comment deleted bro . . .")
            # return render_template("login.html", form1 = form1,form2=form2, name=name, our_users=our_users)
            return redirect(url_for('comment_list'))
        except:
            db.session.rollback()
            flash("Deleting comment got a problem :(")
            return redirect(url_for('comment_list'))


@bp.route("/comment_flush")
@login_required
def comment_flush():
    if current_user.level == 'Admin':
        comment_delete = Comments.query.all()
        try:
            db.session.execute('''TRUNCATE TABLE comments''')
            db.session.delete(comment_delete)
            db.session.commit()
            flash("All comment deleted bro . . .")
            # return render_template("login.html", form1 = form1,form2=form2, name=name, our_users=our_users)
            return redirect(url_for('comment_list'))
        except:
            db.session.rollback()
            flash("Deleting comment got a problem :(")
            return redirect(url_for('comment_list'))
