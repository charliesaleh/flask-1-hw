from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# FORMS SECTION
class PokemonForm(FlaskForm):
    pokemon_names = StringField('Name:', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')