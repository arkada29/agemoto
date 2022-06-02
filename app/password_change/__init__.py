from flask import Blueprint

bp = Blueprint('password_change', __name__, template_folder='templates')

from app.password_change import routes