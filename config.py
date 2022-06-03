from datetime import timedelta
from pathlib import Path
import pathlib
import os
# from dotenv import load_dotenv

# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    
    basedir = Path(__file__).parent
    UPLOAD_FOLDER = 'app/static/images/'
    UPLOADED_PATH = basedir / 'app/static/uploads'

    ALLOWED_EXTENSION = set(['txt', 'pdf', 'jpg', 'png', 'jpeg', 'gif'])

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     "mysql+pymysql://root:rootpass@localhost/db_agemoto" 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')\
        or "mysql+pymysql://root:rootpass@localhost/db_agemoto"

    POSTS_PER_PAGE = 10
    POSTS_PER_PAGE_UPCOMINGS = 50

    #google stuff
    RECAPTCHA_PUBLIC_KEY = '6LfhAowfAAAAAHNUTYw61gzjtL7pWpJra_ckea6B'
    RECAPTCHA_PRIVATE_KEY = '6LfhAowfAAAAADQyn8kGHTD47Mz_umfyaEF5D5bV'
    
    GOOGLE_CLIENT_ID = "7506615127-pap2j83rb7q00ri0j03pcukl8l0rjqn4.apps.googleusercontent.com"
    CLIENT_SECRETS_FILE = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

    GOOGLEMAPS_KEY = "AIzaSyDsV20fqMaLCAyuqkMAoOejUNigYWTPnfk"

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or 1 #is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'aoazureflamegod@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'trismegistus' 
    ADMINS = ['aoazureflamegod@gmail.com']
    # SQLALCHEMY_dATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False