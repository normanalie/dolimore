from flask_wtf import FlaskForm
from wtforms import (
    RadioField, SelectMultipleField,
    BooleanField, 
    SubmitField, 
    )

from .department import Department

class MailingForm(FlaskForm):
    categories_customer = SelectMultipleField("Catégories Tiers")
    categories_contact = SelectMultipleField("Catégories Contact")
    operator_customer = RadioField("Filtre Tiers", choices=[("and", "ET"), ("or", "OU")], default='and')
    operator_contact = RadioField("Filtre Contact", choices=[("and", "ET"), ("or", "OU")], default='and')
    departments_customer = SelectMultipleField("Departements Tiers", choices=Department.tuple("#n (#i)"))
    departments_contact = SelectMultipleField("Departements Contacts", choices=Department.tuple("#n (#i)"))
    add_customer_contacts = BooleanField("Ajouter les contacts des tiers ?")
    submit = SubmitField("Ajouter")
    delete = SubmitField("Vider")
