from flask import current_app, redirect, render_template, request, url_for
from flask_login import login_required

from os import path

from app.contract import bp
from app import db
from app.models import User

from .forms import ContractForm
from .contract import Contract


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ContractForm()
    if not path.exists(current_app.root_path+"\\static\\files\\contract\\contrat.odt"):  # No contract file
        return redirect(url_for('contract.upload'))

    if form.validate_on_submit():  # POST    
        return render_template('contract.index.html')

    return render_template('contract/index.html', form=form)


@bp.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    return render_template('contract/upload.html')

@bp.route('/export/', methods=['GET', 'POST'])
@login_required
def export():
    return render_template('contract/export.html')