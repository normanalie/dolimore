from datetime import datetime

from flask import redirect, render_template, request, send_from_directory, session, url_for, Blueprint, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.forms import LoginForm, ContractForm, MailingForm, CreateAdminForm
from app.models import User

from .dolibarr import Dolibarr
from .export import Export

bp = Blueprint('main', __name__, url_prefix="")


@bp.route('/')
@bp.route('/index/')
def index():
    if len(User.query.all()) == 0:  # No user in db
        return redirect(url_for('main.firstconnection'))

    return render_template('index.html')


@bp.route('/contract/', methods=['GET', 'POST'])
@login_required
def contract():
    form = ContractForm()
    tiers = ["mairie saint-denis", "salle des fetes"]
    return render_template('contract.html', form=form, tiers=tiers)


@bp.route('/mailing/', methods=["GET", "POST"])
@login_required
def mailing():
    if len(User.query.all()) == 0:  # No user in db
        return redirect(url_for('main.firstconnection'))

    form = MailingForm()
    if "mailing_emails" in session:  # List of precedent emails selection
        # A list of lists with all the precedent append: [ ['callA@gmail.com', 'callA@gmail.com'], ['callB@gmail.com', 'callB@gmail.com'] ]
        emails = session["mailing_emails"]
    else:
        emails = []

    form.categories_contact.choices = Dolibarr.categories(types=["contact"])
    form.categories_customer.choices = Dolibarr.categories(types=["customer"])

    if form.validate_on_submit():
        if form.submit.data:  # Submit button
            extracted_emails = []  # A local list of all emails from selected categories, added to session emails at the end
            emails_contact = Dolibarr.emails(["contact"], form.categories_contact.data, form.operator_contact.data)
            emails_customer = Dolibarr.emails(["customer"], form.categories_customer.data, form.operator_customer.data)
            extracted_emails.extend(emails_contact)
            extracted_emails.extend(emails_customer)
            if form.add_customer_contacts.data:
                emails_customer_contacts = Dolibarr.customer_contacts_from_cat(form.categories_customer.data, form.operator_customer.data)
                extracted_emails.extend(emails_customer_contacts)
            emails.append(extracted_emails)
        else:  # Delete button -> Empty emails list
            emails = []

    form.categories_contact.data = ""  # Empty default value at each reload 
    form.categories_customer.data = ""

    emails = Dolibarr.delete_duplicates(emails)
    session["mailing_emails"] = emails  # Update session var
    return render_template('mailing.html', form=form, emails=emails)


@bp.route('/mailing/export/')
@login_required
def mailing_export():
    if "mailing_emails" in session:  # List of precedent emails selection
        emails = session["mailing_emails"]
    
        # Extract emails
        full_emails = []  # A single list of all the emails
        for sublist in emails:
            for email in sublist:
                if email not in full_emails:
                    full_emails.append(email)

        # Generate path
        basedir = current_app.config["EXPORT_FOLDER"]
        ts = datetime.timestamp(datetime.now())
        ts = str(ts).split('.')[0]  # Remove miliseconds from timestamp
        username = current_user.username
        filename = f'mailing-{username}-{ts}.csv'
        path = Export.path([basedir, filename])

        # Generate file
        Export.csv(full_emails, path)
        return send_from_directory(directory=basedir, path=filename, as_attachment=True)





@bp.route('/login', methods=['GET', 'POST'])
def login():
    if len(User.query.all()) == 0:  # No user in db
        return redirect(url_for('main.firstconnection'))

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


@bp.route('/firstconnection', methods=["GET", "POST"])
def firstconnection():
    if len(User.query.all()) == 0:  # No user in db
        form = CreateAdminForm()
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
    return redirect(url_for('main.index'))
