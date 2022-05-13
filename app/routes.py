from flask import redirect, render_template, request, session, url_for, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.forms import LoginForm, SignupForm
from app.models import User


bp = Blueprint('main', __name__, url_prefix="")


@bp.route('/')
@bp.route('/index/')
def index():
    return render_template('index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    errors = []
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():  # POST processing
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            errors.append("Pas d'utilisateurs avec cet email")
        elif not user.check_password(form.password.data):
            errors.append("Mot de passe incorrect")
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':  # Check if there is a next_page and if the next_page is a relative path
                next_page = url_for('main.index')
            return redirect(next_page)
    return render_template('login.html', form=form, errors=errors)


@bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.before_app_request
def firstconnection():
    if len(User.query.all()) == 0:  # No user in db
        form = SignupForm()
        errors = []

        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            u = User(username=username, email=email, is_admin=True)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('main.login'))
        
        if request.method == 'POST' and not form.validate():
            errors.append(form.errors)

        return render_template('firstconnection.html', form=form, errors=errors)
    
