from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm, ContractForm, MailingForm
from app.models import User

from .dolibarr import Dolibarr
from . import dolibarr_config

Dolibarr.config(dolibarr_config.API_KEY, dolibarr_config.BASE_URL)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/contract', methods=['GET', 'POST'])
@login_required
def contract():
    form = ContractForm()
    tiers = ["mairie saint-denis", "salle des fetes"]
    return render_template('contract.html', form=form, tiers=tiers)


@app.route('/mailing', methods=["GET", "POST"])
@login_required
def mailing():
    form = MailingForm()
    emails = []

    categories_contact = Dolibarr.categories(types=["contact"])
    form.categories_contact.choices = categories_contact
    categories_customer = Dolibarr.categories(types=["customer"])
    form.categories_customer.choices = categories_customer

    if form.validate_on_submit():
        cat_id_contact = form.categories_contact.data
        cat_operator_contact = form.operator_contact.data
        cat_id_customer = form.categories_customer.data
        cat_operator_customer = form.operator_customer.data
        emails_contact = Dolibarr.emails(["contact"], cat_id_contact, cat_operator_contact)
        emails_customer = Dolibarr.emails(["customer"], cat_id_customer, cat_operator_customer)
        emails.extend(emails_contact)
        emails.extend(emails_customer)

    return render_template('mailing.html', form=form, emails=emails)


@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = []
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login.html', form=form, errors=errors)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))