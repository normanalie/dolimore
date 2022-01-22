from flask import redirect, render_template, url_for
from flask_login import current_user, login_user

from app import app
from app.forms import LoginForm
from app.models import User


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
    errors = []
    if current_user.is_authenticated:
        return redirect(url_for(''))

    form = LoginForm()
    if form.validate_on_submit():  # POST processing
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            errors.append("Pas d'utilisateurs avec cet email")
        elif not user.check_password(form.password.data):
            errors.append("Mot de passe incorrect")
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for(''))
    return render_template('login.html', form=form, errors=errors)