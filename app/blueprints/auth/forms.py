from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from app.models import User

# FORMS SECTION
class PokemonForm(FlaskForm):
    pokemon_names = StringField('Name:', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')
    catch = SubmitField('Catch')
    
class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')])
    submit_btn = SubmitField('Register')
    
class EditProfileForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = EmailField('Email:', validators=[DataRequired()])
    submit_btn = SubmitField('Update')
    
class PokemonCaughtForm(FlaskForm):
    pokemon_name = StringField('Pokemon Name', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')
    catch = SubmitField('Catch')
    
class PokemonTeamForm(FlaskForm):
    Name = StringField('Name', validators=[DataRequired()])
    Abilities = StringField('Abilities', validators=[DataRequired()])
    BaseExperience = StringField('Base Experience', validators=[DataRequired()])
    FrontShinyURL = StringField('Front Shiny URL', validators=[DataRequired()])
    AttackBaseStat = StringField('Attack Base Stat', validators=[DataRequired()])
    HPBaseStat = StringField('HP Base Stat', validators=[DataRequired()])
    DefenseBaseStat = StringField('Defense Base Stat', validators=[DataRequired()])
    submit_btn = SubmitField('Add Pokemon')
    
class PokemonBattleForm(FlaskForm):
    opponent_email = EmailField('Opponent Email:', validators=[DataRequired()])
    submit_btn = SubmitField('Battle Pokemon')
