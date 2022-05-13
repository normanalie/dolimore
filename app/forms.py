from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo
from wtforms import (
    StringField, TextAreaField, 
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
    remember_me = BooleanField("Rester connecté")
    submit = SubmitField("Se connecter")

class SignupForm(FlaskForm):  # Create a admin user the first time the app is launched
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirmation = PasswordField("Repeat password", validators=[EqualTo('password')])
    is_admin = BooleanField("Administrateur", default=False)
    submit = SubmitField("Créer")
