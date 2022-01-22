from flask import redirect, render_template

from app import app
from app.forms import LoginForm


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contract')
def base():
    return render_template('contract.html')

@app.route('/mailing')
def mailing():
    return render_template('mailing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('login.html', form=form)