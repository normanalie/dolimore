from flask_wtf import FlaskForm

from datetime import date

from wtforms.validators import DataRequired
from wtforms import (
    StringField, TextAreaField,
    DateField,
    DecimalField, 
    SubmitField, 
    )


class ContractForm(FlaskForm):
    object_number = StringField('N° Objet')
    quote_number = StringField('N° Devis')
    show_name = StringField('Nom spectacle')
    show_conditions = TextAreaField('Conditions accueil')
    show_date = DateField('Date spectacle', format='%Y-%m-%d', validators=[DataRequired()])
    residence_place = StringField('Lieu herbergement')
    technical_contact = StringField('Notre contact technique')
    price_excl = DecimalField('Prix HT', places=2, rounding=None, use_locale=None, validators=[DataRequired()])
    taxes = DecimalField('TVA 5,5%', places=2, rounding=None, use_locale=None, validators=[DataRequired()])
    price_incl = DecimalField('Prix TTC', places=2, rounding=None, use_locale=None, validators=[DataRequired()])
    price_letter = StringField('Prix lettres')
    contract_date = DateField('Date', format='%Y-%m-%d', default=date.today(), validators=[DataRequired()])
    submit = SubmitField("Générer")