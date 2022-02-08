from flask_wtf import FlaskForm
from wtforms import (
    RadioField, SelectMultipleField,
    BooleanField, 
    SubmitField, 
    )
class MailingForm(FlaskForm):
    categories_customer = SelectMultipleField("Catégories Tiers")
    categories_contact = SelectMultipleField("Catégories Contact")
    operator_customer = RadioField("Filtre Tiers", choices=[("and", "ET"), ("or", "OU")], default='and')
    operator_contact = RadioField("Filtre Contact", choices=[("and", "ET"), ("or", "OU")], default='and')
    add_customer_contacts = BooleanField("Ajouter les contacts des tiers ?")
    submit = SubmitField("Ajouter")
    delete = SubmitField("Vider")
