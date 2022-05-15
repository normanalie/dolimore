from flask import current_app, redirect, render_template, request, send_file, url_for
from flask_login import login_required
from wtforms import DateField

from os import path
from app import contract

from app.contract import bp
from app import db
from app.models import User

from .forms import ContractForm, UploadForm
from .contract import Contract


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ContractForm()
    contract_path = current_app.root_path+"\\static\\files\\contract\\contract.odt"
    if not path.exists(contract_path):  # No contract file
        return redirect(url_for('contract.upload'))

    if form.validate_on_submit():  # POST    
        if form.submit.data:  # Submit button
            datas = dict()
            for field in form:
                if field.name != "csrf_tocken" and field.name != "submit":
                    if isinstance(field, DateField):
                        datas["#"+field.name] = field.data.strftime('%d/%m/%Y')
                    else: 
                        datas["#"+field.name] = str(field.data)
            file_path = Contract.generate(contract_path, datas)
            print(file_path)
        return send_file(file_path, as_attachment=True)

    return render_template('contract/index.html', form=form)


@bp.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    
    print(form.errors)
    print(form.validate())
    if form.validate_on_submit():
        f = request.files['file']
        f.save(f"{current_app.root_path}\\static\\files\\contract\\contract.odt")
        return redirect(url_for('contract.index'))
    return render_template('contract/upload.html', form=form)

@bp.route('/export/', methods=['GET', 'POST'])
@login_required
def export():
    return render_template('contract/export.html')