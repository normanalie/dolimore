from flask import Blueprint

bp = Blueprint('mailing', __name__)

from app.mailing import routes