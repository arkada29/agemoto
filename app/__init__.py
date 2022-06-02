import logging
import os
from flask import Flask, request, current_app, render_template, redirect, flash, url_for, abort, session, send_from_directory, make_response, jsonify
from config import Config
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_mail import Mail
from flask_share import Share
from flask_babel import Babel, lazy_gettext as _l
#sql_alchemy
from flask_sqlalchemy import SQLAlchemy

#utilities
from pathlib import Path


# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app,db)
db = SQLAlchemy()
migrate = Migrate()
share = Share()

login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message = _l('Please log in to access this page.')
babel = Babel()



mail = Mail()

basedir = Path(__file__).parent
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def create_app(config_class=Config):

    app = Flask(__name__)    

    db.init_app(app)
    migrate.init_app(app,db)    
    share.init_app(app)    
    login_manager.init_app(app)
    babel.init_app(app)

    app.config.from_object(config_class)
    
    mail.init_app(app)
    
    # login.init_app(app)
    from app.base import bp as main_bp
    app.register_blueprint(main_bp)

    from app.post import bp as post_bp
    app.register_blueprint(post_bp)

    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from app.search import bp as search_bp
    app.register_blueprint(search_bp)

    from app.comment import bp as comment_bp
    app.register_blueprint(comment_bp)

    from app.collection import bp as collection_bp
    app.register_blueprint(collection_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.password_change import bp as password_change_bp
    app.register_blueprint(password_change_bp)

    from app.about import bp as about_bp
    app.register_blueprint(about_bp)

    #handling email server
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject="Agemoto Failure",
                credentials=auth, 
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/agemoto.log',
                                            maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Agemoto startup')

    return app

# from app import models

