from flask import render_template, current_app, redirect, url_for, request, session, flash, abort
from app.user.forms import LoginForm, UserForm
from app.user import bp
from app import create_app, db, login_manager
from app.models import Users, Posts, Upcomings, Comments
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from urllib.parse import urlparse, urljoin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from pip._vendor import cachecontrol
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from PIL import Image
from sqlalchemy.sql.expression import func
from sqlalchemy import cast, Date, and_, UniqueConstraint
from flask_babel import _

import google.auth.transport.requests
import requests
import uuid as uuid 
import os
import calendar

app = create_app()

flow = Flow.from_client_secrets_file(
        client_secrets_file=app.config['CLIENT_SECRETS_FILE'],
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri="https://agemoto.herokuapp.com/callback" )

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@bp.route('/login', methods=['GET','POST'])
def login():
    session.permanent = True
    name = None
    form1 = LoginForm()
    #validate Form
    if form1.validate_on_submit():
        user = Users.query.filter_by(username=form1.username.data).first()
        next = request.args.get('next')
        if user:
            #check the hash            
            if check_password_hash(user.password_hash, form1.password.data):
                login_user(user)
                user.last_seen = datetime.utcnow()
                session['user'] = user.username
                db.session.commit()
                # flash('Login successfully')
                app.logger.info('%s logged in successfully', user.username)
                if is_safe_url(next):
                    return redirect(next or url_for('user.dashboard'))                    
                else:
                    return redirect('/login')            
            else:
                flash(_("Wrong password - try again"))
        else:
            flash(_("User doesnt exist - try again"))   
    our_users = Users.query.order_by(Users.date_added)
    return render_template("/user/login.html", form1=form1, name=name, our_users=our_users)   

@bp.route('/register', methods=['POST','GET'])
# @login_required
def register():
    form = UserForm()
    if form.validate_on_submit():       
        user = Users.query.filter_by(username=form.username.data).first() 
        name = Users.query.filter_by(name=form.name.data).first() 
        email = Users.query.filter_by(email=form.email.data).first() 
        try:
            if user:
                flash("username exist try another")
            elif name:
                flash("name exist try another")
            elif email:
                flash("email exist try another")
            else:
                hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
                user = Users(name=form.name.data, 
                            email=form.email.data,
                            username=form.username.data, 
                            level= form.level.data,
                            password_hash=hashed_pw)
                db.session.add(user)
                db.session.commit()
                form.name.data = ''
                form.name.data = ''
                form.username.data = ''
                form.email.data = ''
                form.password_hash.data = ''
                form.level.data = ''
                flash(_("Users added Succesfully!"))
                app.logger.info('%s adding user', user)
                return redirect(url_for('user.register'))
        except:
            db.session.rollback()
            flash('Oops something wrong')
    return render_template('/user/register.html', form=form)


@bp.route('/login/google')
def login_google():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@bp.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500) # state doesnt match protect from cross site

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=app.config['GOOGLE_CLIENT_ID']
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")

    # try:
    next = request.args.get('next')
    name = Users.query.filter_by(name=session['name']).first()
    if name:
        login_user(name)
        if is_safe_url(next):
            return redirect(next or url_for('user.page_root'))                    
        else:
            return redirect('/login')   
    else:
        name = Users(name=session['name'], 
                    email=session['email'],
                    username=session['name'], 
                    level= 'VIP'
                    # password_hash=hashed_pw
                    )
        db.session.add(name)
        db.session.commit()
        # flash("Users added Succesfully!")
    login_user(name)
    return redirect(url_for('user.page_root'))

@bp.route('/logout', methods=['GET', 'POST'])
# @login_required
def logout():
    logout_user()
    session.clear()
    # session['user'] = None
    # if session.get('was_once_logged_in'):
    # #     # prevent flashing automatically logged out message
    # #     # del session['was_once_logged_in']
    #     session.pop('was_once_logged_in')
    # flash("You have logged out. Thanks for coming")
    return redirect(url_for('base.page_root'))

@bp.route("/delete/<int:id>")
@login_required
def delete(id):
    if 'Admin' == current_user.level:
    # if id == current_user.id:
        user_to_delete = Users.query.get_or_404(id)
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User deleted bro . . .")
            return redirect(url_for('user.user_list'))
        except:
            db.session.rollback()
            flash("Deleting user got a problem :(")
            return redirect(url_for('user.user_list'))
    else:
        flash("Sorry you can't delete that user")
        return redirect(url_for('user.dashboard', id=current_user.id))

@bp.route("/user_list")
@login_required
def user_list():
    count = Users.query.order_by(Users.id).all()
    count_data = db.session.query(Users.id).count()
    page = request.args.get('page', 1, type=int)
    user = Users.query.order_by(Users.id.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('collection.user_list', page=user.next_num) \
        if user.has_next else None
    prev_url = url_for('collection.user_list', page=user.prev_num) \
        if user.has_prev else None
    return render_template("/user/user_list.html", count=count, 
                            count_data=count_data,
                            user=user.items,
                            next_url=next_url,
                            prev_url=prev_url
                            )

@bp.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    form = UserForm()
    id=current_user.id
    name_to_update = Users.query.get_or_404(id)
    count_post = Posts.query.all()
    count_user = Users.query.all()
    count_comment = Comments.query.all()
    count_upc = Upcomings.query.all()
    count_user_comment = db.session.query(func.count(Comments.id_user), Comments.id_user).group_by(Comments.id_user)
    
    countPost = len(Posts.query.all())
    countUser = len(Users.query.all())
    countUpc = len(Upcomings.query.all())
    totalDivider = countPost+countUser+countUpc

    pieLabel = ['Post', 'User', 'Upcoming']

    avgPost = round(countPost/totalDivider * 100, 2)
    avgUser = round(countUser/totalDivider * 100,2)
    avgUpc = round(countUpc/totalDivider * 100, 2)

    pieData = [avgPost, avgUser, avgUpc]   
    
    if name_to_update.profile_pic:
        del_img = os.path.join(app.config['UPLOAD_FOLDER'],name_to_update.profile_pic)
    if request.method == 'POST':
        # hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.about_author = request.form['about_author']
        name_to_update.level = request.form['level']
        # name_to_update.password_hash = hashed_pw
        filename = request.files['profile_pic']
        name_to_update.date_modified = datetime.now()
        if filename and allowed_file(filename.filename):
            name_to_update.profile_pic = filename
            image = Image.open(name_to_update.profile_pic)
            image = image.resize((500,700),Image.ANTIALIAS)
            #Grab image name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            #set uuid
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            #save that image
            # saver = request.files['profile_pic']
            #change it to string to save to db
            name_to_update.profile_pic = pic_name
            try:
                db.session.commit()
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name), optimize=True)
                if del_img:
                    os.remove(del_img)
                flash(_("User updated!"))
                app.logger.info('%s user updated', name_to_update.name)
                # return render_template("dashboard.html", form=form, name_to_update=name_to_update)
                return redirect(url_for("user.dashboard"))
            except:
                db.session.rollback()
                flash(_("Error updated!, try again bro ..."))
                app.logger.info('%s error on upate', name_to_update.name)
                # return render_template("dashboard.html", form=form, name_to_update=name_to_update)
                return redirect(url_for("user.dashboard"))
        else:
            try:
                db.session.commit()
                flash(_("User updated!"))
                app.logger.info('%s user updated', name_to_update.name)
                # return render_template("dashboard.html", form=form, name_to_update=name_to_update)
                return redirect(url_for("user.dashboard"))
            except:
                db.session.rollback()
                flash(_("Error updated!, try again bro ..."))
                app.logger.info('%s error on update', name_to_update.name)
                # return render_template("dashboard.html", form=form, name_to_update=name_to_update)
                return redirect(url_for("user.dashboard"))
    # else:
    form.name.data = name_to_update.name,
    form.username.data = name_to_update.username,
    form.email.data = name_to_update.email,
    form.about_author.data = name_to_update.about_author,
    form.level.data = name_to_update.level
    return render_template("/user/dashboard.html"
    , form=form
    , name_to_update=name_to_update
    , id=id
    , count_user=count_user
    , count_post=count_post
    ,count_comment=count_comment
    , count_upc=count_upc
    ,count_user_comment=count_user_comment
    ,pieLabel=pieLabel
    ,pieData = pieData
    )

def customGraphSearch():
    generalYear = db.session.query(func.count(Posts.id), func.year(Posts.date_posted))\
                    .group_by(func.year(Posts.date_posted)).all()

    generalMonth = db.session.query(func.count(Posts.id), cast(func.year(Posts.date_posted)+'-'+func.month(Posts.date_posted)+'-'+'01', Date))\
                    .group_by(cast(func.year(Posts.date_posted)+'-'+func.month(Posts.date_posted)+'-'+'01', Date)).all() 

    generalDay = db.session.query(func.count(Posts.id), func.Date(Posts.date_posted))\
                    .group_by(func.Date(Posts.date_posted)).all() 

    generalUpcYear = db.session.query(func.count(Upcomings.id_upc), func.year(Upcomings.date_created))\
                    .group_by(func.year(Upcomings.date_created)).all()

    generalUpcMonth = db.session.query(func.count(Upcomings.id_upc), cast(func.year(Upcomings.date_created)+'-'+func.month(Upcomings.date_created)+'-'+'01', Date))\
                    .group_by(cast(func.year(Upcomings.date_created)+'-'+func.month(Upcomings.date_created)+'-'+'01', Date)).all() 

    generalUpcDay = db.session.query(func.count(Upcomings.id_upc), func.Date(Upcomings.date_created))\
                    .group_by(func.Date(Upcomings.date_created)).all() 

    return (generalYear, generalMonth, generalDay
            , generalUpcYear, generalUpcMonth, generalUpcDay)

def graphDataSet():
    yearNow = datetime.now().year
    yearPrev = (datetime.now().year-1)

    dataYear = db.session.query(func.count(Posts.id), func.year(Posts.date_posted))\
                .filter(and_(func.year(Posts.date_posted)>=yearPrev,func.year(Posts.date_posted)<=yearNow))\
                .group_by(func.year(Posts.date_posted)).all()

    dataMonth = db.session.query(func.count(Posts.id), func.month(Posts.date_posted))\
                .filter(func.year(Posts.date_posted)==yearNow)\
                .group_by(func.month(Posts.date_posted)).all()

    dataDay = db.session.query(func.count(Posts.id), func.Date(Posts.date_posted))\
                .filter(and_(func.year(Posts.date_posted)==2022), func.month(Posts.date_posted)==2)\
                .group_by(func.Date(Posts.date_posted)).all()

    dataYearUpc = db.session.query(func.count(Upcomings.id_upc), func.year(Upcomings.date_created))\
                .filter(and_(func.year(Upcomings.date_created)>=yearPrev,func.year(Upcomings.date_created)<=yearNow))\
                .group_by(func.year(Upcomings.date_created)).all()

    dataMonthUpc = db.session.query(func.count(Upcomings.id_upc), func.month(Upcomings.date_created))\
                .filter(func.year(Upcomings.date_created)==yearNow)\
                .group_by(func.month(Upcomings.date_created)).all()

    dataDayUpc = db.session.query(func.count(Upcomings.id_upc), func.Date(Upcomings.date_created))\
                .filter(and_(func.year(Upcomings.date_created)==2022), func.month(Upcomings.date_created)==2)\
                .group_by(func.Date(Upcomings.date_created)).all()

    reverseDayPost = []
    reverseDayUpc = []

    yearLabel = []
    yearData = []
    monthLabel = []
    monthData = []
    dayLabel = []
    dayData = []

    yearLabelUpc = []
    yearDataUpc = []
    monthLabelUpc = []
    monthDataUpc = []
    dayLabelUpc = []
    dayDataUpc = []

    for i, j in enumerate(reversed(dataDay)):
        if i < 7: 
            reverseDayPost.append(j)

    for i, j in enumerate(reversed(dataDayUpc)):
        if i < 7: 
            reverseDayUpc.append(j)           

    for count, year in dataYear:
        yearLabel.append(year)
        yearData.append(count)

    for count, month in dataMonth:
        month_num = str(month)
        datetime_object = datetime.strptime(month_num, "%m")
        month_name = datetime_object.strftime("%b")
        monthLabel.append(month_name)
        monthData.append(count)

    for count, day in reverseDayPost:
        dayLabel.append(calendar.day_name[day.weekday()])
        dayData.append(count)

    for count, year in dataYearUpc:
        yearLabelUpc.append(year)
        yearDataUpc.append(count)

    for count, month in dataMonthUpc:
        month_num = str(month)
        datetime_object = datetime.strptime(month_num, "%m")
        month_name = datetime_object.strftime("%b")
        monthLabelUpc.append(month_name)
        monthDataUpc.append(count)

    for count, day in reverseDayUpc:
        dayLabelUpc.append(calendar.day_name[day.weekday()])
        dayDataUpc.append(count)

    return (yearLabel, yearData, monthLabel, monthData, dayLabel, dayData,
            yearLabelUpc, yearDataUpc, monthLabelUpc, monthDataUpc, dayLabelUpc, dayDataUpc)

@bp.route('/statistic_detail', methods=['POST', 'GET'])
def statisticDetail():
    searchList = ['Year', 'Month', 'Day']    

    customGraphData = customGraphSearch()   

    yearLabel = graphDataSet()[0] 
    yearData = graphDataSet()[1]
    monthLabel = graphDataSet()[2]
    monthData = graphDataSet()[3]
    dayLabel = graphDataSet()[4]
    dayData = graphDataSet()[5]

    yearLabelUpc = graphDataSet()[6]
    yearDataUpc = graphDataSet()[7]
    monthLabelUpc = graphDataSet()[8]
    monthDataUpc = graphDataSet()[9]

    dayLabelUpc = graphDataSet()[10]
    dayDataUpc = graphDataSet()[11]

    return render_template('/user/statistic_detail.html'

                            ,yearLabel=yearLabel
                            ,yearData=yearData
                            ,monthLabel=monthLabel
                            ,monthData=monthData
                            ,dayData=dayData
                            ,dayLabel=dayLabel
                            ,yearLabelUpc=yearLabelUpc
                            ,yearDataUpc=yearDataUpc
                            ,monthLabelUpc=monthLabelUpc
                            ,monthDataUpc=monthDataUpc
                            ,dayLabelUpc=dayLabelUpc
                            ,dayDataUpc=dayDataUpc
                            ,customGraphData=customGraphData
 
                            )

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSION']
    

