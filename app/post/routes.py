import json
from app import create_app, db, current_app
from flask import flash, render_template, request, session, redirect, url_for, jsonify, make_response, Response
from app.post import bp
from app.post.forms import PostForm
from app.comment.forms import CommentForm
from app.models import Posts, Upcomings, Comments, Users, Category
from sqlalchemy.sql.expression import func
from sqlalchemy import and_
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from PIL import Image
from werkzeug.utils import secure_filename
from config import Config
import uuid as uuid
import os

app = create_app()

# app.config.from_object(Config)

# @login_manager.user_loader
# def load_user(user_id):
#     return Users.query.get(int(user_id))
@bp.route('/imageuploader', methods=['POST'])
@login_required
def imageuploader():
    # check if the post request has the file part
    file = request.files.get('file')
    if file:
        filename = file.filename.lower()
        fn, ext = filename.split('.')
        # truncate filename (excluding extension) to 30 characters
        fn = fn[:30]
        filename = fn + '.' + ext
        if ext in ['jpg', 'gif', 'png', 'jpeg']:
            pic_filename = secure_filename(filename)
            # pic_name = str(uuid.uuid1()) + "_" + pic_filename
            try:
                # everything looks good, save file
                img_fullpath = os.path.join(app.config['UPLOADED_PATH'], pic_filename)
                file.save(img_fullpath)
            except:
                # fail, image did not upload
                output = make_response(404)
                output.headers['Error'] = 'Image failed to upload'
                return output
            return jsonify({'location' : pic_filename})
    os.abort(Response('404 - Image failed to upload'))

@bp.route('/post/add-post', methods=['GET', 'POST'])
@login_required
def blog_post():
    form = PostForm()
    group_cat = db.session.query(Category.category)
    upcoming = db.session.query(Upcomings.name)
    upc = request.form.get('query')
    if form.validate_on_submit():
        # try:
        #     language = detect(form.content.data)
        # except LangDetectException:
        #     language = ''
        poster = current_user.id
        filename = request.files['post_thumbnail']
        id_cat = db.session.query(Category.id_category).filter_by(category=form.category.data)
        upcoming_id = db.session.query(Upcomings.id_upc).filter_by(name=upc)
        if filename and allowed_file(filename.filename):
            # name_to_update.profile_pic = filename
            form.post_thumbnail.data = filename
            #Grab image name
            # in_mem_file = BytesIO(form.post_thumbnail.data.read())
            image = Image.open(form.post_thumbnail.data)
            image = image.resize((1280,570),Image.ANTIALIAS)
            pic_filename = secure_filename(form.post_thumbnail.data.filename)
            #set uuid
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            #save that image
            # saver = request.files['post_thumbnail']
            #change it to string to save to db
            
            form.post_thumbnail.data = pic_name

            post = Posts(title=form.title.data,
                        content=form.content.data,
                        post_id=poster,
                        category_id=id_cat,
                        slug=form.slug.data,
                        platfrom = form.platform.data,
                        description = form.description.data,
                        thumbnail=form.post_thumbnail.data,
                        upc_id=upcoming_id,
                        # language=language,
                        tags=form.tags.data,
                        news_type=form.news_type.data
                        )
            form.title.data = ""
            form.content.data = ""
            # form.author.data = ""
            form.slug.data = ""
            form.post_thumbnail.data = ""
            form.platform.data = ""
            form.description.data = ""
            form.tags.data = ""
            form.news_type.data = ""
            try:
                db.session.add(post)
                db.session.commit()
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name), optimize=True)
                app.logger.info('%s adding post', post.title)
                flash("Post submitted successfully !!!")
                return redirect(url_for('post.blog_post'))
            except:
                db.session.rollback()
                flash("Sorry there is something wrong we are looking to it !!!")
                return redirect(url_for('post.blog_post')) 
        else:    
            post = Posts(title=form.title.data,
                        content=form.content.data,
                        post_id=poster,
                        category_id=id_cat,
                        slug=form.slug.data,
                        platfrom = form.platform.data,
                        description = form.description.data,
                        upc_id=upcoming_id,
                        # language=language,
                        tags=form.tags.data,
                        news_type=form.news_type.data
                        )
            form.title.data = ""
            form.content.data = ""
            # form.author.data = ""
            form.slug.data = ""
            form.platform.data = ""
            form.description.data = ""
            form.tags.data = ""
            form.news_type.data = ""
            try:
                db.session.add(post)
                db.session.commit()
                app.logger.info('%s adding post', post.title)
                flash("Post submitted successfully !!!")
                return redirect(url_for('post.blog_post'))
            except:
                db.session.rollback()
                flash("Sorry there is something wrong we are looking to it !!!")
                return redirect(url_for('post.blog_post'))
        
    return render_template("add-post.html", form=form, group_cat=group_cat, upcoming=upcoming)

@bp.route('/post/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
def edit_post(id):
    edit = Posts.query.get_or_404(id)
    form = PostForm()
    group_cat = db.session.query(Category.category)
    upcoming = db.session.query(Upcomings.name)
    upc = request.form.get('query')
    if form.validate_on_submit():
        # form.category.data = db.session.query(Category.category)
        upcoming_id = db.session.query(Upcomings.id_upc).filter_by(name=upc)
        category_id = db.session.query(Category.id_category).filter_by(category=form.category.data)
        edit.title = form.title.data
        edit.slug = form.slug.data
        edit.content = form.content.data
        edit.category_id = category_id
        edit.description = form.description.data
        edit.platfrom = form.platform.data
        edit.upc_id = upcoming_id
        edit.tags = form.tags.data
        edit.news_type = form.news_type.data
        filename = request.files['post_thumbnail']
        edit.updated = 'updated'
        if filename and allowed_file(filename.filename):
            edit.thumbnail = filename
            #Grab image name
            image = Image.open(edit.thumbnail)
            image = image.resize((1280,570),Image.ANTIALIAS)
            pic_filename = secure_filename(edit.thumbnail.filename)
            #set uuid
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            #save that image
            # saver = request.files['post_thumbnail']
            #change it to string to save to db
            form.post_thumbnail.data = pic_name
            edit.thumbnail = pic_name

            try:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name), optimize=True)
                app.logger.info('%s logged in successfully', edit.title)
            except Exception as e:
                app.logger.info('%s logged in successfully', edit.title)
        #update to db
            # try:
            #     # db.session.add(edit)
            #     # db.session.commit()
            #     image.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name), optimize=True)
            #     flash("Post has been updated !")
            #     app.logger.info('%s logged in successfully', edit.title)
            #     return redirect(url_for('post.post', year=edit.date_posted.year, id=edit.id, category=edit.category_post.category, name=edit.title))
            #     # return redirect(url_for('post', id=edit.id))
            # except:
            #     # db.session.rollback()
            #     flash("Failed to update post !")
            #     return redirect(url_for('post.post', year=edit.date_posted.year, id=edit.id, category=edit.category_post.category, name=edit.title))
        
        try:
            # db.session.add(edit)
            db.session.commit()
            flash("Post has been updated !")
            return redirect(url_for('post.post', year=edit.date_posted.year, id=edit.id, category=edit.category_post.category, name=edit.title))
        except:
            db.session.rollback()
            flash("Failed to update post !")
            return redirect(url_for('post.post', year=edit.date_posted.year, id=edit.id, category=edit.category_post.category, name=edit.title))
    
    if current_user.id == edit.poster.id:
        form.title.data = edit.title
        form.slug.data = edit.slug
        form.content.data = edit.content
        form.category.data = ""
        form.description.data = edit.description
        form.post_thumbnail.data = edit.thumbnail
        form.platform.data = edit.platfrom
        form.post_upcoming.data = ""
        form.tags.data = ""
        form.news_type.data = ""
        return render_template('edit_post.html', form=form, edit=edit, group_cat=group_cat, upcoming=upcoming)
    else:
        flash("You don't authorized to edit the post !")
        post = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", post=post)

@bp.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    # if id == post_to_delete.poster.id:
    # request.method == 'POST':
    # if request.method == 'POST':
    if current_user.level == 'Admin':
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            # Return a message
            flash("Blog Post Was Deleted!")
            # Grab all the posts from the database
            posts = Posts.query.order_by(Posts.date_posted)
            return redirect(url_for("post.post_list"))
        except:
            # Return an error message
            flash("Whoops! There was a problem deleting post, try again...")
            # Grab all the posts from the database
            # posts = Posts.query.order_by(Posts.date_posted)
            # return render_template("posts.html", posts=posts)
            return redirect(url_for("post.post_list"))
    else:
            # Return a message
        flash("You Aren't Authorized To Delete That Post!")
        # Grab all the posts from the database
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

@bp.route('/posts')
def posts():
    top_post = Posts.query.order_by(Posts.date_posted.desc()).limit(2).all()
    top_post_id = [t.id for t in top_post]
    middle_post = Posts.query.order_by(Posts.id.desc()).filter(Posts.id.not_in(top_post_id)).limit(4).all()
    middle_post_id = min([m.id for m in middle_post])
    page = request.args.get('page', 1, type=int)
    post = Posts.query.order_by(Posts.date_posted.desc()).paginate\
            (page, app.config['POSTS_PER_PAGE'], False)
    favPost = Posts.query.filter(Posts.news_type=='favourite').order_by\
            (Posts.id.desc()).limit(5).all()
    next_url = url_for('post.posts', page=post.next_num) \
        if post.has_next else None
    prev_url = url_for('post.posts', page=post.prev_num) \
        if post.has_prev else None
    count_post = db.session.query(func.count(Posts.id)).first()
    cp = int(str(count_post).replace('(','').replace(')','').replace(',',''))
    minus = db.session.query(Posts.date_posted)
    now = datetime.now()
    rdelta = relativedelta
    count_query = db.session.query(func.count(Comments.id_post), Posts.id, Comments.id_post).\
                    join(Comments, Comments.id_post == Posts.id, isouter=True).group_by(Posts.id)
    
    return render_template("posts.html",
                            post=post.items,
                            now=now,
                            rdelta=rdelta,
                            minus=minus,
                            count_query=count_query,
                            next_url=next_url,
                            prev_url=prev_url,
                            cp = cp,
                            page=page,
                            top_post=top_post,
                            top_post_id=top_post_id,
                            middle_post_id=middle_post_id,
                            middle_post=middle_post,
                            favPost=favPost)

@bp.route('/posts/post_games/<category>/<sub_cat>')
def posts_games(category, sub_cat):
    sub_category = sub_cat
    upcoming = Upcomings.query.filter(Upcomings.date_released>=datetime.now())\
                .order_by(Upcomings.date_released).limit(10)
    page = request.args.get('page', 1, type=int)
    post = Posts.query.filter(Posts.platfrom.like('%'+sub_category+'%'))\
            .order_by(Posts.date_posted.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('post.posts_games', page=post.next_num) \
        if post.has_next else None
    prev_url = url_for('post.posts_games', page=post.prev_num) \
        if post.has_prev else None
    count_post = db.session.query(func.count(Posts.id)).first()
    cp = int(str(count_post).replace('(','').replace(')','').replace(',',''))
    minus = db.session.query(Posts.date_posted)
    now = datetime.now()
    rdelta = relativedelta
    count_query = db.session.query(func.count(Comments.id_post), Posts.id, Comments.id_post).\
                    join(Comments, Comments.id_post == Posts.id, isouter=True).group_by(Posts.id)
    top_post = Posts.query.filter(Posts.platfrom.like('%'+sub_category+'%')).order_by(Posts.date_posted.desc())\
                .limit(2).all()
    top_post_id = [t.id for t in top_post]
    middle_post =   Posts.query.filter(and_(Posts.platfrom.like('%'+sub_category+'%'),\
                    Posts.id.not_in(top_post_id))).order_by(Posts.id.desc())\
                    .limit(4).all()
    middle_post_id = []
    if len(middle_post) != 0:
        for m in middle_post:
            middle_post_id.append(m.id)
    # middle_post_id = min([m.id for m in middle_post])
    return render_template('posts_games.html',
                            upcoming=upcoming,
                            post=post.items,
                            now=now,
                            rdelta=rdelta,
                            minus=minus,
                            count_query=count_query,
                            next_url=next_url,
                            prev_url=prev_url,
                            cp = cp,
                            page=page,
                            top_post=top_post,
                            top_post_id=top_post_id,
                            sub_category=sub_category,
                            middle_post=middle_post,
                            middle_post_id=middle_post_id,
                            category=category
            )

@bp.route('/posts/post_animes/<category>')
def posts_anime(category):
    upcoming = Upcomings.query.filter(Upcomings.date_released>=datetime.now()).order_by(Upcomings.date_released).limit(10)
    page = request.args.get('page', 1, type=int)
    post = Posts.query.filter(Posts.category_id==2).order_by(Posts.date_posted.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('post.posts_anime', page=post.next_num) \
        if post.has_next else None
    prev_url = url_for('post.posts_anime', page=post.prev_num) \
        if post.has_prev else None
    count_post = db.session.query(func.count(Posts.id)).filter(Posts.category_id==2).first()
    cp = int(str(count_post).replace('(','').replace(')','').replace(',',''))
    minus = db.session.query(Posts.date_posted)
    now = datetime.now()
    rdelta = relativedelta
    count_query = db.session.query(func.count(Comments.id_post), Posts.id, \
                    Comments.id_post).join(Comments, Comments.id_post == Posts.id, \
                    isouter=True).group_by(Posts.id)
    top_post =  Posts.query.filter(Posts.category_id==2).\
                order_by(Posts.date_posted.desc()).limit(2).all()
    top_post_id = [t.id for t in top_post]
    middle_post =   Posts.query.filter(and_(Posts.category_id==2,\
                    Posts.id.not_in(top_post_id))).order_by(Posts.id.desc())\
                    .limit(4).all()
    
    middle_post_id = min([m.id for m in middle_post ])
    return render_template('posts_anime.html',
                            upcoming=upcoming,
                            post=post.items,
                            now=now,
                            rdelta=rdelta,
                            minus=minus,
                            count_query=count_query,
                            next_url=next_url,
                            prev_url=prev_url,
                            cp = cp,
                            page=page,
                            top_post=top_post,
                            top_post_id=top_post_id,
                            middle_post_id=middle_post_id,
                            middle_post=middle_post,
                            # sub_category=sub_category,
                            category=category)

@bp.route('/posts/post_movies/<category>')
def posts_movies(category):
    upcoming = Upcomings.query.filter(Posts.category_id==6).filter(Upcomings.date_released>=datetime.now()).order_by(Upcomings.date_released).limit(10)
    page = request.args.get('page', 1, type=int)
    post = Posts.query.filter(Posts.category_id==6).filter(Posts.category_id==6).order_by(Posts.date_posted.desc())\
            .paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('post.posts_movies', page=post.next_num) \
        if post.has_next else None
    prev_url = url_for('post.posts_movies', page=post.prev_num) \
        if post.has_prev else None
    count_post = db.session.query(func.count(Posts.id)).filter(Posts.category_id==6).first()
    cp = int(str(count_post).replace('(','').replace(')','').replace(',',''))
    minus = db.session.query(Posts.date_posted)
    now = datetime.now()
    rdelta = relativedelta
    count_query = db.session.query(func.count(Comments.id_post), Posts.id, \
                    Comments.id_post).join(Comments, Comments.id_post == Posts.id, \
                    isouter=True).group_by(Posts.id)
    top_post =  Posts.query.filter(Posts.category_id==6).\
                order_by(Posts.date_posted.desc()).limit(2).all()
    top_post_id = [t.id for t in top_post]
    middle_post =   Posts.query.filter(and_(Posts.category_id==6,\
                    Posts.id.not_in(top_post_id))).order_by(Posts.id.desc())\
                    .limit(4).all()
    
    middle_post_id = []
    if len(middle_post) != 0:
        for m in middle_post:
            middle_post_id.append(m.id)
    return render_template('posts_movies.html',
                            upcoming=upcoming,
                            post=post.items,
                            now=now,
                            rdelta=rdelta,
                            minus=minus,
                            count_query=count_query,
                            next_url=next_url,
                            prev_url=prev_url,
                            cp = cp,
                            page=page,
                            top_post=top_post,
                            top_post_id=top_post_id,
                            middle_post_id=middle_post_id,
                            middle_post=middle_post,
                            # sub_category=sub_category,
                            category=category)

@bp.route('/posts/post_techno/<category>')
def post_techno(category):
    top_post = Posts.query.filter(Posts.category_id==5).order_by(Posts.date_posted.desc()).limit(2).all()
    top_post_id = [t.id for t in top_post]
    middle_post = Posts.query.filter(Posts.category_id==5).order_by(Posts.id.desc()).filter(Posts.id.not_in(top_post_id)).limit(4).all()
    # middle_post_id = min([m.id for m in middle_post])
    middle_post_id = []
    if len(middle_post) != 0:
        for m in middle_post:
            middle_post_id.append(m.id)
    page = request.args.get('page', 1, type=int)
    post = Posts.query.filter(Posts.category_id==5).order_by(Posts.date_posted.desc()).paginate\
            (page, app.config['POSTS_PER_PAGE'], False)
    favPost = Posts.query.filter(and_(Posts.news_type=='favourite'),\
             (Posts.category_id==5)).order_by(Posts.id.desc()).limit(5).all()
    next_url = url_for('post.post_techno', page=post.next_num) \
        if post.has_next else None
    prev_url = url_for('post.post_techno', page=post.prev_num) \
        if post.has_prev else None
    count_post = db.session.query(func.count(Posts.id)).filter(Posts.category_id==5).first()
    cp = int(str(count_post).replace('(','').replace(')','').replace(',',''))
    minus = db.session.query(Posts.date_posted)
    now = datetime.now()
    rdelta = relativedelta
    count_query = db.session.query(func.count(Comments.id_post), Posts.id, Comments.id_post).\
                    join(Comments, Comments.id_post == Posts.id, isouter=True).group_by(Posts.id)

    return render_template('posts_techno.html',
                            post=post.items,
                            now=now,
                            rdelta=rdelta,
                            minus=minus,
                            count_query=count_query,
                            next_url=next_url,
                            prev_url=prev_url,
                            cp = cp,
                            page=page,
                            top_post=top_post,
                            top_post_id=top_post_id,
                            middle_post_id=middle_post_id,
                            middle_post=middle_post,
                            favPost=favPost)

@bp.route('/posts/post_others/<category>')
def post_others(category):
    top_post = Posts.query.filter(Posts.category_id==4).order_by(Posts.date_posted.desc()).limit(2).all()
    top_post_id = [t.id for t in top_post]
    middle_post = Posts.query.filter(Posts.category_id==4).order_by(Posts.id.desc()).filter(Posts.id.not_in(top_post_id)).limit(4).all()
    # middle_post_id = min([m.id for m in middle_post])
    middle_post_id = []
    if len(middle_post) != 0:
        for m in middle_post:
            middle_post_id.append(m.id)
    page = request.args.get('page', 1, type=int)
    post = Posts.query.filter(Posts.category_id==4).order_by(Posts.date_posted.desc()).paginate\
            (page, app.config['POSTS_PER_PAGE'], False)
    favPost = Posts.query.filter(and_(Posts.news_type=='favourite'),\
             (Posts.category_id==4)).order_by(Posts.id.desc()).limit(5).all()
    next_url = url_for('post.post_others', page=post.next_num) \
        if post.has_next else None
    prev_url = url_for('post.post_others', page=post.prev_num) \
        if post.has_prev else None
    count_post = db.session.query(func.count(Posts.id)).filter(Posts.category_id==4).first()
    cp = int(str(count_post).replace('(','').replace(')','').replace(',',''))
    minus = db.session.query(Posts.date_posted)
    now = datetime.now()
    rdelta = relativedelta
    count_query = db.session.query(func.count(Comments.id_post), Posts.id, Comments.id_post).\
                    join(Comments, Comments.id_post == Posts.id, isouter=True).group_by(Posts.id)
    return render_template('posts_others.html',
                            post=post.items,
                            now=now,
                            rdelta=rdelta,
                            minus=minus,
                            count_query=count_query,
                            next_url=next_url,
                            prev_url=prev_url,
                            cp = cp,
                            page=page,
                            top_post=top_post,
                            top_post_id=top_post_id,
                            middle_post_id=middle_post_id,
                            middle_post=middle_post,
                            favPost=favPost)

@bp.route('/posts/post_compilation/<category>')
def posts_compilation(category):
    top_post = Posts.query.filter(Posts.category_id==3).order_by(Posts.date_posted.desc()).limit(2).all()
    top_post_id = [t.id for t in top_post]
    middle_post = Posts.query.filter(Posts.category_id==3).order_by(Posts.id.desc()).filter(Posts.id.not_in(top_post_id)).limit(4).all()
    # middle_post_id = min([m.id for m in middle_post])
    middle_post_id = []
    if len(middle_post) != 0:
        for m in middle_post:
            middle_post_id.append(m.id)
    page = request.args.get('page', 1, type=int)
    post = Posts.query.filter(Posts.category_id==3).order_by(Posts.date_posted.desc()).paginate\
            (page, app.config['POSTS_PER_PAGE'], False)
    favPost = Posts.query.filter(and_(Posts.news_type=='favourite'),\
             (Posts.category_id==3)).order_by(Posts.id.desc()).limit(5).all()
    next_url = url_for('post.posts_compilation', page=post.next_num) \
        if post.has_next else None
    prev_url = url_for('post.posts_compilation', page=post.prev_num) \
        if post.has_prev else None
    count_post = db.session.query(func.count(Posts.id)).filter(Posts.category_id==3).first()
    cp = int(str(count_post).replace('(','').replace(')','').replace(',',''))
    minus = db.session.query(Posts.date_posted)
    now = datetime.now()
    rdelta = relativedelta
    count_query = db.session.query(func.count(Comments.id_post), Posts.id, Comments.id_post).\
                    join(Comments, Comments.id_post == Posts.id, isouter=True).group_by(Posts.id)
    return render_template('posts_compilation.html',
                            post=post.items,
                            now=now,
                            rdelta=rdelta,
                            minus=minus,
                            count_query=count_query,
                            next_url=next_url,
                            prev_url=prev_url,
                            cp = cp,
                            page=page,
                            top_post=top_post,
                            top_post_id=top_post_id,
                            middle_post_id=middle_post_id,
                            middle_post=middle_post,
                            favPost=favPost)

@bp.route('/post/<int:year>/<int:id>/<category>/<name>', methods=['GET', 'POST'])
def post(year, id, category, name):
    comment_form = CommentForm()
    now = datetime.now()
    utc =  datetime.utcnow()
    rdelta = relativedelta
    diff = now - utc
    diff_hours = diff.total_seconds()/3600
    post = Posts.query.get_or_404(id)
    prev_id = Posts.query.filter(Posts.id<post.id).order_by(Posts.id.desc()).limit(1).all()
    next_id = Posts.query.filter(Posts.id>post.id).order_by(Posts.id.asc()).limit(1).all()
    title = post.title
    user = Users.query.order_by(Users.id)
    posts = Posts.query.order_by(func.rand()).limit(4)
    pos = Posts.query.order_by(Posts.id)
    comments = Comments.query.order_by(Comments.id_comment)
    upcoming = Upcomings.query.order_by(Upcomings.date_created)
    return render_template('post.html'
                            , post=post
                            , prev_id=prev_id
                            , next_id=next_id
                            , posts=posts
                            , pos=pos
                            , comment_form=comment_form
                            , comments=comments
                            , now = now
                            , rdelta=rdelta
                            , upcoming=upcoming
                            , diff_hours=str(int(diff_hours))+ ' hours ago'
                            , user=user
                            , title = title
                            )

@bp.route("/post/post_list")
@login_required
def post_list():
    count = Posts.query.order_by(Posts.id).all()
    page = request.args.get('page', 1, type=int)
    post = Posts.query.order_by(Posts.id.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('post.post_list', page=post.next_num) \
        if post.has_next else None
    prev_url = url_for('post.post_list', page=post.prev_num) \
        if post.has_prev else None
    return render_template("post_list.html",
                        count=count,
                        post=post.items,
                        next_url=next_url,
                        prev_url=prev_url
                        )

@bp.route("/posts/top_ten.html")
def top_ten():
    page = request.args.get('page', 1, type=int)
    post = Posts.query.filter_by(category_id=3).order_by(Posts.date_posted.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('post.posts', page=post.next_num) \
        if post.has_next else None
    prev_url = url_for('post.posts', page=post.prev_num) \
        if post.has_prev else None
    count_post = db.session.query(func.count(Posts.id)).first()
    cp = int(str(count_post).replace('(','').replace(')','').replace(',',''))
    minus = db.session.query(Posts.date_posted)
    now = datetime.now()
    count_query = db.session.query(func.count(Comments.id_post), Posts.id, Comments.id_post).\
    join(Comments, Comments.id_post == Posts.id, isouter=True).group_by(Posts.id)
    top_post = Posts.query.filter_by(category_id=3).order_by(Posts.date_posted.desc()).limit(2)
    return render_template("top_ten.html",
                            post=post.items,
                            now=now,
                            minus=minus,
                            count_query=count_query,
                            next_url=next_url,
                            prev_url=prev_url,
                            cp = cp,
                            page=page, top_post=top_post)

@bp.route("/searchcollection",methods=["POST","GET"])
def searchcollection():
    if request.method == 'POST':

        search_word = request.get_json()
        if search_word == '':
            collection = ()
            collect = Upcomings.query.filter(Upcomings.name).limit(20).all()
            for a in collect:
                collection = list(collection)
                row_dict = {column: str(getattr(a, column)) for column in a.__table__.c.keys()}
                collection.append(row_dict)
                collection = tuple(collection)
        else:
            collection = ()
            collect = Upcomings.query.filter(Upcomings.name.like('%'+str(search_word[0]['query'])+'%')).limit(20).all()
            for a in collect:
                collection = list(collection)
                row_dict = {column: str(getattr(a, column)) for column in a.__table__.c.keys()}
                collection.append(row_dict)
                collection = tuple(collection)
            numrows = len(collection)
    return jsonify({'htmlresponse': render_template('collectionResponse.html',

                search_word= search_word[0]['query'],
                collection=collection,
                numrows=numrows
                    )})




def allowed_file(filename):
        return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSION']