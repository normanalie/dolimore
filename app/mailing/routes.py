from datetime import datetime

from flask import redirect, render_template, request, send_from_directory, session, url_for, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.mailing import bp
from app import db
from .forms import MailingForm
from app.models import User

from .dolibarr import Dolibarr
from .export import Export




@bp.route('/', methods=["GET", "POST"])
@login_required
def index():
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
            emails_customer = Dolibarr.get(filters={
                "type": ["customer"], 
                "contacts": form.add_customer_contacts.data,
                "categories": form.categories_customer.data,
                "departements": form.departments_customer.data,
                "operator": form.operator_customer.data
                })
            emails_customer = emails_customer.values()  # Get return a dict, we only want emails. 
            #emails_customer = Dolibarr.emails(["customer"], form.categories_customer.data, form.operator_customer.data)
            extracted_emails.extend(emails_contact)
            extracted_emails.extend(emails_customer)

            emails.append(extracted_emails)
        else:  # Delete button -> Empty emails list
            emails = []

    form.categories_contact.data = ""  # Empty default value at each reload 
    form.categories_customer.data = ""

    emails = Dolibarr.delete_duplicates(emails)
    session["mailing_emails"] = emails  # Update session var
    return render_template('mailing/index.html', form=form, emails=emails)


@bp.route('/export/')
@login_required
def export():
    if "mailing_emails" in session:  # List of precedent emails selection
        emails = session["mailing_emails"]
    
        # Extract emails
        full_emails = []  # A single list of all the emails
        for sublist in emails:
            for email in sublist:
                if email not in full_emails:
                    full_emails.append(email)

        # Generate path
        export_dir = current_app.config["EXPORT_FOLDER"]
        ts = datetime.timestamp(datetime.now())
        ts = str(ts).split('.')[0]  # Remove miliseconds from timestamp
        username = current_user.username
        filename = f'mailing-{username}-{ts}.csv'
        path = Export.path([current_app.root_path, export_dir, filename])

        # Generate file
        Export.csv(full_emails, path)
        return send_from_directory(directory=export_dir, path=filename, as_attachment=True)
