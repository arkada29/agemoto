from flask import Blueprint

bp = Blueprint('search',__name__, template_folder='templates')

from app.search import routes