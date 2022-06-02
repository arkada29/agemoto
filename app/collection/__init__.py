from flask import Blueprint

bp = Blueprint('collection', __name__, template_folder='templates')

from app.collection import routes