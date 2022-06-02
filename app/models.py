from app import db, create_app
from sqlalchemy import UniqueConstraint
from datetime import datetime, date, timedelta
from flask_login import UserMixin, current_user
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from time import time
import jwt

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    name =  db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    about_author = db.Column(db.Text(255), nullable=True)
    fav_color = db.Column(db.String(120))
    profile_pic = db.Column(db.String(500), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime)
    level = db.Column(db.String(20), nullable=False)
    #adding last seen
    last_seen = db.Column(db.DateTime)
    #do some password
    password_hash = db.Column(db.String(128))

    # id_post = db.Column(db.Integer, db.ForeignKey('posts.id'))

    #user can have many post
    posts = db.relationship('Posts', backref='poster')#foreign_keys=['posts.id']

    comments = db.relationship('Comments', backref='comment_user')
    upcomings = db.relationship('Upcomings', backref='upcoming_user')

    likepost = db.relationship('Likepost',  backref='liked_user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not readable !')

    @password.setter
    def password(self, user_pwd):
        self.password_hash = generate_password_hash(user_pwd)

    def verify(self, user_pwd):
        return check_password_hash(self.password_hash, user_pwd)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)    

    def like_post(self, post):
        if not self.has_liked_post(post):
            # post_id = Posts.query.filter_by(id=post.id).first_or_404()
            like = Likepost(user_id=self.id, post_id=post.id)#    
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            # post_id = Users.query.filter_by(id=post.id).first_or_404()
            Likepost.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        # post_id = Users.query.filter_by(id=post.id).first_or_404()
        return Likepost.query.filter(
            Likepost.user_id == self.id,
            Likepost.post_id == post.id).count() > 0

    #encode-decode-token
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_pwd':self.id, 'exp':time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )
    
    @staticmethod
    def verify_reset_password(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY']
            ,algorithms=['HS256'])['reset_pwd']
        except:
            return
        return Users.query.get(id)

    #create string
    def __repr__(self):
        return '<Name %r>' % self.name

# #models for like post
class Likepost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))    

#create blog post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.now)
    slug = db.Column(db.String(255))
    description = db.Column(db.String(255))
    thumbnail = db.Column(db.String(500), nullable=True)
    platfrom = db.Column(db.String(255), nullable=True)
    language = db.Column(db.String(5))
    tags = db.Column(db.String(255), nullable=True)
    news_type = db.Column(db.String(50), nullable=True)
    #foreign key to link Users
    post_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id_category'))
    upc_id = db.Column(db.Integer, db.ForeignKey('upcomings.id_upc'))

    updated = db.Column(db.String(20))

    comments = db.relationship('Comments', backref='comment_post')
    
    likepost = db.relationship('Likepost', backref='post_like', lazy='dynamic')

    # users = db.relationship('Users', backref='user_post') #, foreign_keys='post_id'

    # def allowed_file(filename):
    #     return '.' in filename and filename.rsplit('.',1)[1].lower() in ['ALLOWED_EXTENSION']

    def list_breaker(value):
        for j in value:
            if j.description != None:
                desc = j.description.split(',')
                return desc

     #Like post
    # def like_post(self, user):
    #     if not self.has_liked_post(user):
    #         user_id = Users.query.filter_by(id=user).first_or_404()
    #         like = Likepost(user_id=user_id.id, post_id=self.id)#    
    #         db.session.add(like)

    # def unlike_post(self, user):
    #     if self.has_liked_post(user):
    #         user_id = Users.query.filter_by(id=user).first_or_404()
    #         Likepost.query.filter_by(
    #             user_id=user_id.id,
    #             post_id=self.id).delete()

    # def has_liked_post(self, user):
    #     user_id = Users.query.filter_by(id=user.id).first_or_404()
    #     return Likepost.query.filter(
    #         Likepost.user_id == user_id.id,
    #         Likepost.post_id == self.id).count() > 0

    def __repr__(self):
        return '<Name %r>' % self.name

#create comment model
class Comments(db.Model):
    id_comment = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    date_comment = db.Column(db.DateTime, default=datetime.now)
    #foreign key
    id_post = db.Column(db.Integer, db.ForeignKey('posts.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))

#create upcoming model
class Upcomings(db.Model):
    id_upc = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_released = db.Column(db.Date)
    date_created = db.Column(db.DateTime, default=datetime.now)
    cover_picture = db.Column(db.String(255))
    thumbnail_picture = db.Column(db.String(255))
    platform = db.Column(db.String(255))
    developer = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    synopsis = db.Column(db.Text(500))
    producer = db.Column(db.String(255))
    studio = db.Column(db.String(255))
    series = db.Column(db.String(255))
    engine = db.Column(db.String(255))
    mode = db.Column(db.String(255))
    episode = db.Column(db.String(255))
    duration = db.Column(db.String(255))
    source = db.Column(db.String(255))

    starring = db.Column(db.String(255))
    boxoffice = db.Column(db.String(255))
    language = db.Column(db.String(255))
    budget = db.Column(db.String(255))
    mpaa = db.Column(db.String(255))
    based = db.Column(db.String(255))

    updated = db.Column(db.String(20))

    #foreign key
    id_category = db.Column(db.Integer, db.ForeignKey('category.id_category'))
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    #relationship
    posts = db.relationship('Posts', backref='upcoming_post')

    # def allowed_file(filename):
    #     return '.' in filename and filename.rsplit('.',1)[1].lower() in ['ALLOWED_EXTENSION']

#create Category
class Category(db.Model):
    id_category = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=datetime.now())
    posts = db.relationship('Posts', backref = 'category_post')
    upcomings = db.relationship('Upcomings', backref='category_upcoming') 

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    subject = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(20))
    message = db.Column(db.Text)

# class UnionSearch(db.Model):
#     id_search = db.Column(db.Integer, primary_key=True)
#     name_post = db.Column(db.String(255))
#     slug_post = db.Column