from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired

# FORMS SECTION
class PokemonForm(FlaskForm):
    pokemon_names = StringField('Name:', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')
    
class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class SignUpForm(FlaskForm):
    email = EmailField('Enter Email:', validators=[DataRequired()])
    password = PasswordField('Enter Password:', validators=[DataRequired()])
    submit_btn = SubmitField('Sign Up')
    