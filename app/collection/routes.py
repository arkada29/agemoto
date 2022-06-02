import imp
from flask import render_template, url_for, redirect, send_file, session, request, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from app import create_app, db
from app.collection.forms import UpcomingForm
from app.models import Upcomings, Users, Posts, Category
from app.collection import bp
from sqlalchemy.sql.expression import func
from werkzeug.utils import secure_filename
from PIL import Image

from datetime import datetime, date, timedelta
from sqlalchemy import cast, Date, and_, UniqueConstraint

import os
import uuid as uuid 

app = create_app()

@bp.route('/upcoming/games', methods=['GET','POST'])
def upcoming_games():
    page = request.args.get('page', 1, type=int)
    upcomings = Upcomings.query.filter_by(id_category=1).order_by(Upcomings.date_released.desc())\
                .paginate(page, app.config['POSTS_PER_PAGE_UPCOMINGS'], False)
    next_url = url_for('collection.upcoming_games', page=upcomings.next_num) \
        if upcomings.has_next else None
    prev_url = url_for('collection.upcoming_games', page=upcomings.prev_num) \
        if upcomings.has_prev else None
    count_upc_gm = db.session.query(func.count(Upcomings.id_upc)).first()
    # upcomings = Upcomings.query.filter_by(id_category=1).order_by(Upcomings.date_released.desc())
    cp = int(str(count_upc_gm).replace('(','').replace(')','').replace(',',''))    
    return render_template('upcoming_games.html', 
                            upcomings=upcomings.items,
                            next_url=next_url,
                            prev_url=prev_url,
                            page=page,
                            cp=cp)

@bp.route('/upcoming/animes')
def upcoming_animes():
    page = request.args.get('page', 1, type=int)
    upcomings = Upcomings.query.filter_by(id_category=2).order_by(Upcomings.date_released.desc())\
                .paginate(page, app.config['POSTS_PER_PAGE_UPCOMINGS'], False)
    next_url = url_for('collection.upcoming_animes', page=upcomings.next_num) \
        if upcomings.has_next else None
    prev_url = url_for('collection.upcoming_animes', page=upcomings.prev_num) \
        if upcomings.has_prev else None
    count_upc_gm = db.session.query(func.count(Upcomings.id_upc)).first()
    # upcomings = Upcomings.query.filter_by(id_category=1).order_by(Upcomings.date_released.desc())
    cp = int(str(count_upc_gm).replace('(','').replace(')','').replace(',',''))  
    return render_template('upcoming_animes.html', 
                            upcomings=upcomings.items,
                            next_url=next_url,
                            prev_url=prev_url,
                            page=page,
                            cp=cp)

@bp.route('/upcoming/movies')
def upcoming_movies():
    page = request.args.get('page', 1, type=int)
    upcomings = Upcomings.query.filter_by(id_category=6).order_by(Upcomings.date_released.desc())\
                .paginate(page, app.config['POSTS_PER_PAGE_UPCOMINGS'], False)
    next_url = url_for('collection.upcoming_movies', page=upcomings.next_num) \
        if upcomings.has_next else None
    prev_url = url_for('collection.upcoming_movies', page=upcomings.prev_num) \
        if upcomings.has_prev else None
    count_upc_gm = db.session.query(func.count(Upcomings.id_upc)).first()
    # upcomings = Upcomings.query.filter_by(id_category=1).order_by(Upcomings.date_released.desc())
    cp = int(str(count_upc_gm).replace('(','').replace(')','').replace(',','')) 
    return render_template('upcoming_movies.html',
                            upcomings=upcomings.items,
                            next_url=next_url,
                            prev_url=prev_url,
                            page=page,
                            cp=cp)

@bp.route('/upcoming/<int:id>')
def upcoming_detail(id):
    upcoming = Upcomings.query.get_or_404(id)
    post = Posts.query.order_by(Posts.upc_id)
    return render_template("upcoming_detail.html",upcoming=upcoming, post=post)

@bp.route('/upcoming_upload', methods=['GET', 'POST'])
@login_required
def upcoming():
    form = UpcomingForm()
    group_cat = db.session.query(Category.category)
    id_user = current_user.id
    if form.validate_on_submit():
        filename = request.files['cover_picture']
        filename2 = request.files['thumbnail_picture']
        if current_user.is_authenticated:
            category_id = form.categories.data
            id_cat = db.session.query(Category.id_category).filter_by(category=category_id)  
            if (filename and allowed_file(filename.filename)) or (filename2 and allowed_file(filename2.filename)):
                form.cover_picture.data = filename
                form.thumbnail_picture.data = filename2

                #Grab image name
                image = Image.open(form.cover_picture.data)
                image = image.resize((500,700),Image.ANTIALIAS)
                image2 = Image.open(form.thumbnail_picture.data)
                image2 = image2.resize((1280,570),Image.ANTIALIAS)

                pic_filename = secure_filename(form.cover_picture.data.filename)
                pic_filename2 = secure_filename(form.thumbnail_picture.data.filename)
                #set uuid
                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                pic_name2 = str(uuid.uuid1()) + "_" + pic_filename2

                #save that image
                #change it to string to save to db
                form.cover_picture.data = pic_name 
                form.thumbnail_picture.data = pic_name2 
                # form.
                upcoming = Upcomings(
                            name = form.name.data,
                            date_released = form.date_released.data,
                            # id_category = form.
                            id_category = id_cat,
                            platform = form.platform.data,
                            cover_picture = form.cover_picture.data,
                            thumbnail_picture = form.thumbnail_picture.data,
                            developer = form.developers.data,
                            publisher = form.publishers.data,
                            genre = form.genre.data,
                            synopsis = form.synopsis.data,
                            producer = form.producer.data,
                            studio = form.studio.data,
                            series = form.series.data,
                            engine = form.engine.data,
                            mode = form.mode.data,
                            episode = form.episode.data,
                            duration = form.duration.data,
                            source = form.source.data,

                            starring = form.starring.data,
                            boxoffice = form.boxoffice.data,
                            language = form.language.data,
                            budget = form.budget.data,
                            mpaa = form.mpaa.data,
                            based = form.based.data,

                            id_user = id_user
                            )
                form.name.data = ""
                form.date_released.data = ""
                form.categories.data = ""
                form.platform.data = ""
                form.developers.data = ""
                form.publishers.data = ""
                form.genre.data = ""
                form.synopsis.data = ""
                form.producer.data = ""
                form.studio.data = ""
                form.series.data = ""
                form.engine.data = ""
                form.mode.data = ""
                form.episode.data = ""
                form.duration.data = ""
                form.source.data = ""

                form.starring.data = ""
                form.boxoffice.data = ""
                form.language.data = ""
                form.budget.data = ""
                form.mpaa.data = ""
                form.based.data = ""

                try:
                    db.session.add(upcoming)
                    db.session.commit()
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                    image2.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name2))
                    flash('Succesfully added')
                    return redirect(url_for('collection.upcoming'))
                except Exception as e:
                    flash('Sorry there is an error occured')
                    return redirect(url_for('collection.upcoming'))
            else:
                upcoming = Upcomings(
                            name = form.name.data,
                            date_released = form.date_released.data,
                            id_category = id_cat,
                            platform = form.platform.data,
                            developer = form.developers.data,
                            publisher = form.publishers.data,
                            genre = form.genre.data,
                            synopsis = form.synopsis.data,
                            producer = form.producer.data,
                            studio = form.studio.data,
                            series = form.series.data,
                            engine = form.engine.data,
                            mode = form.mode.data,
                            episode = form.episode.data,
                            duration = form.duration.data,
                            source = form.source.data,

                            starring = form.starring.data,
                            boxoffice = form.boxoffice.data,
                            language = form.language.data,
                            budget = form.budget.data,
                            mpaa = form.mpaa.data,
                            based = form.based.data,

                            id_user = id_user
                            )
                form.name.data = ""
                form.date_released.data = ""
                form.categories.data = ""
                form.platform.data = ""
                form.developers.data = ""
                form.publishers.data = ""
                form.genre.data = ""
                form.synopsis.data = ""
                form.producer.data = ""
                form.studio.data = ""
                form.series.data = ""
                form.engine.data = ""
                form.mode.data = ""
                form.episode.data = ""
                form.duration.data = ""
                form.source.data = ""

                form.starring.data = ""
                form.boxoffice.data = ""
                form.language.data = ""
                form.budget.data = ""
                form.mpaa.data = ""
                form.based.data = ""

                db.session.add(upcoming)
                db.session.commit()
                flash('Succesfully added')
                return redirect(url_for('collection.upcoming'))
        else:
            flash("You're not authorized to access this page")
            # return redirect(url_for('upcoming'))        
        # return render_template('upcoming.html', form=form, categories=categories)
    return render_template('upcoming.html', form=form, group_cat=group_cat)

@bp.route('/upcomings')
@login_required
def upcomings():
    upcoming = Upcomings.query.order_by(Upcomings.date_created).all()
    count_data =  db.session.query(Upcomings.id_upc).count()
    page = request.args.get('page', 1, type=int)
    upc = Upcomings.query.order_by(Upcomings.id_upc.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('collection.upcomings', page=upc.next_num) \
        if upc.has_next else None
    prev_url = url_for('collection.upcomings', page=upc.prev_num) \
        if upc.has_prev else None
    return render_template("upcomings.html", upcoming=upcoming, 
                            # count_data=count_data,
                            upc=upc.items,
                            next_url=next_url,
                            prev_url=prev_url,
                            count_data=count_data
                            )

@bp.route('/upcomings/upcoming_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def upcoming_edit(id):
    form = UpcomingForm()
    upc_id = Upcomings.query.get_or_404(id)
    category_id = form.categories.data
    group_cat = db.session.query(Category.category)
    id_cat = db.session.query(Category.id_category).filter_by(category=category_id)  
    upcoming = Upcomings.query.order_by(Upcomings.date_created)
    # if current_user.is_authenticated:
    if form.validate_on_submit():
        filename = request.files['cover_picture']
        filename2 = request.files['thumbnail_picture']
        upc_id.name = form.name.data
        upc_id.date_released = form.date_released.data
        upc_id.platform = form.platform.data
        upc_id.id_category = id_cat
        upc_id.publisher = form.publishers.data
        upc_id.developer = form.developers.data
        upc_id.genre = form.genre.data
        upc_id.synopsis = form.synopsis.data
        upc_id.producer = form.producer.data
        upc_id.studio = form.studio.data
        upc_id.series = form.series.data
        upc_id.engine = form.engine.data
        upc_id.mode = form.mode.data
        upc_id.episode = form.episode.data
        upc_id.duration = form.duration.data
        upc_id.source = form.source.data

        upc_id.starring = form.starring.data
        upc_id.boxoffice = form.boxoffice.data
        upc_id.language = form.language.data
        upc_id.budget = form.budget.data
        upc_id.mpaa = form.mpaa.data  
        upc_id.based = form.based.data      

        upc_id.updated = 'updated'

        if filename and allowed_file(filename.filename):
            if upc_id.cover_picture:
                del_cover = os.path.join(app.config['UPLOAD_FOLDER'],upc_id.cover_picture)

            upc_id.cover_picture = filename
            #Grab image name         

            image = Image.open(upc_id.cover_picture)
            image = image.resize((500,700),Image.ANTIALIAS)

            pic_filename = secure_filename(upc_id.cover_picture.filename)

            #set uuid
            pic_name = str(uuid.uuid1()) + "_" + pic_filename

            #save that image
            # saver = request.files['post_thumbnail']            
            #change it to string to save to db

            form.cover_picture.data = pic_name
            upc_id.cover_picture = pic_name

            image.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name), optimize=True)
            if os.path.exists(del_cover):
                os.remove(del_cover)

            # try:
            #     # db.session.add(upc_id)
            #     db.session.commit()
            #     image.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name), optimize=True)
            #     if del_cover:
            #         os.remove(del_cover)
            #     flash("Data has been updated")
            #     return redirect(url_for('collection.upcoming_edit', id=upc_id.id_upc))
            # except:        
            #     db.session.rollback()
            #     flash("Sorry something wrong with the data")
            #     return redirect(url_for('collection.upcoming_edit', id=upc_id.id_upc))

        if filename2 and allowed_file(filename2.filename):
            if upc_id.thumbnail_picture:
                del_thumb = os.path.join(app.config['UPLOAD_FOLDER'],upc_id.thumbnail_picture)
            upc_id.thumbnail_picture = filename2
            #Grab image name         

            image2 = Image.open(upc_id.thumbnail_picture)
            image2 = image2.resize((1280,720),Image.ANTIALIAS)

            pic_filename2 = secure_filename(upc_id.thumbnail_picture.filename)

            #set uuid
            pic_name2 = str(uuid.uuid1()) + "_" + pic_filename2

            #save that image
            # saver = request.files['post_thumbnail']            
            #change it to string to save to db
            form.thumbnail_picture.data = pic_name2            
            upc_id.thumbnail_picture = pic_name2

            image2.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name2), optimize=True)
            if os.path.exists(del_thumb):
                os.remove(del_thumb)
            # try:
            #     # db.session.add(upc_id)
            #     db.session.commit()
            #     image2.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name2), optimize=True)
            #     if del_thumb:
            #         os.remove(del_thumb)
            #     flash("Data has been updated")
            #     return redirect(url_for('collection.upcoming_edit', id=upc_id.id_upc))
            # except:        
            #     db.session.rollback()
            #     flash("Sorry something wrong with the data")
            #     return redirect(url_for('collection.upcoming_edit', id=upc_id.id_upc))
        try:
            # db.session.add(upc_id)
            db.session.commit()
            flash("It's been updated")
            return redirect(url_for('collection.upcoming_edit', id=upc_id.id_upc))
        except:        
            db.session.rollback()
            flash("Sorry it's not submitted")
            return redirect(url_for('collection.upcoming_edit', id=upc_id.id_upc))

        # else:
        #     try:
        #         # db.session.add(upc_id)
        #         db.session.commit()
        #         flash("It's been updated")
        #         return redirect(url_for('collection.upcoming_edit', id=upc_id.id_upc))
        #     except:        
        #         db.session.rollback()
        #         flash("Sorry it's not submitted")
        #         return redirect(url_for('collection.upcoming_edit', id=upc_id.id_upc))

    form.name.data = upc_id.name
    form.date_released.data = upc_id.date_released
    form.platform.data = upc_id.platform
    form.publishers.data = upc_id.publisher
    form.developers.data = upc_id.developer
    form.genre.data = upc_id.genre
    form.synopsis.data = upc_id.synopsis
    form.producer.data = upc_id.producer
    form.studio.data = upc_id.studio
    form.series.data = upc_id.series
    form.engine.data = upc_id.engine
    form.mode.data = upc_id.mode
    form.episode.data = upc_id.episode
    form.duration.data = upc_id.duration
    form.source.data = upc_id.source

    form.starring.data = upc_id.starring
    form.boxoffice.data = upc_id.boxoffice
    form.language.data = upc_id.language
    form.budget.data = upc_id.budget
    form.mpaa.data = upc_id.mpaa
    form.based.data = upc_id.based

    return render_template('upcoming_update.html', 
                            upc_id=upc_id, 
                            form=form, 
                            upcoming=upcoming,
                            group_cat=group_cat)

@bp.route("/upcomings/upcoming_delete/<int:id>")
@login_required
def upcoming_delete(id):
    upc_to_delete = Upcomings.query.get_or_404(id)
    try:
        db.session.delete(upc_to_delete)
        db.session.commit()
        flash('Delete successfully')
        upcoming = Upcomings.query.order_by(Upcomings.date_created)
        return redirect(url_for("collection.upcomings"))
    except:
        db.session.rollback()
        flash("Somethings wrong, please try again")
        upcoming = Upcomings.query.order_by(Upcomings.date_created)
        return render_template("upcomings.html", upcoming=upcoming)

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSION']
