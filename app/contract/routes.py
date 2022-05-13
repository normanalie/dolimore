from flask import render_template
from flask_login import login_required
from app.contract import bp
from app import db
from app.models import User


@bp.route('/')
@login_required
def index():

    return render_template('contract/index.html')