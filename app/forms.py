from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Regexp, Email
from wtforms import (
    StringField, TextAreaField, 
    SelectField, RadioField, SelectMultipleField,
    IntegerField, FloatField,
    EmailField, TelField, 
    DateField, 
    PasswordField, 
    BooleanField, 
    SubmitField, 
    )

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Rester connecté", validators=[DataRequired()])
    submit = SubmitField("Se connecter")

class MailingForm(FlaskForm):
    categories_customer = SelectMultipleField("Catégories Tiers")
    categories_contact = SelectMultipleField("Catégories Contact")
    operator_customer = RadioField("Filtre Tiers", choices=[("and", "ET"), ("or", "OU")])
    operator_contact = RadioField("Filtre Contact", choices=[("and", "ET"), ("or", "OU")])
    submit = SubmitField("Ajouter")

class ContractForm(FlaskForm):
    object_number = IntegerField("Numéro objet", validators=[DataRequired(), Length(4, 4, "Longueur: 4 chiffres")])
    quote_number = StringField("Numéro devis", validators=[DataRequired(), Length(-1, 60, "Le numéro est trop long")])

    producer_name = StringField("Nom", validators=[DataRequired(), Length(-1, 60, "Le nom est trop long")])
    producer_address = StringField("Addresse", validators=[DataRequired(), Length(-1, 120, "L'addresse est trop longue")])
    producer_zip = IntegerField("Code postal", validators=[DataRequired(), Length(2, 5, "Longueur: 2 à 5 chiffres")])
    producer_tel = TelField("Numéro de telephone", validators=[Regexp("\d{1,}", message="Ne doit contenir que des chiffres"), Length(-1, 60, "Le numéro est trop long")])
    producer_email = EmailField("Email", validators=[Email("Email invalide")])
    producer_siret = IntegerField("Siret/Siren", validators=[DataRequired(), Length(9, 14, "Longueur: 9 à 14 chiffres")])
    producer_licence = StringField("Licence", validators=[])
    producer_ape = StringField("Code APE", validators=[DataRequired(), Regexp("\d{4}[a-zA-Z]", message="4 chiffres et 1 lettre")])
    producer_tva = StringField("Numéro de TVA", validators=[Length(1, 60, "Le numéro est trop long")])

    producer_representative = StringField("Représentant", validators=[DataRequired(), Length(1, 60, "Le nom est trop long")])
    representative_role = StringField("Qualité du représentant", validators=[DataRequired(), Length(1, 60, "Le texte est trop long")])

    show_name = StringField("Nom", validators=[DataRequired(), Length(-1, 60, "Le nom est trop long")])
    show_date = DateField("Date", validators=[DataRequired()])
    show_conditions = TextAreaField("Conditions d'accueil", validators=[Length(-1, 500, "Doit faire moins de 500 caractères")])
    show_contact = StringField("Contact technique", validators=[DataRequired(), Length(-1, 120, "Le contact est trop long")])

    price_exclVAT = FloatField("Montant HT", validators=[DataRequired(), Length(-1, 60, "Le montant est trop long")])

    submit = SubmitField("Générer")