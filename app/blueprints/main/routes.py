from flask import render_template, request
import requests
from app.blueprints.main import main
from flask_login import login_required
from app.blueprints.auth.forms import PokemonForm

# ROUTES SECTION
@main.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@main.route('/pokeapi', methods=['GET', 'POST'])
@login_required
def pokeapi():
    form = PokemonForm()
    print(request.method)
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_name = form.pokemon_names.data
        print(pokemon_name)
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        if response.ok:
            pokemon = response.json()
            get_pokemon_info = {
                "Name": pokemon["name"],
                "Abilities": pokemon["abilities"][0]['ability']['name'],
                "BaseExperience": pokemon["base_experience"],
                "FrontShinyURL": pokemon["sprites"]["front_shiny"],
                "AttackBaseStat": pokemon["stats"][1]["base_stat"],
                "HPBaseStat": pokemon["stats"][0]["base_stat"],
                "DefenseBaseStat": pokemon["stats"][2]["base_stat"],
                }
            print(get_pokemon_info)
            return render_template('pokeapi.html', get_pokemon_info=get_pokemon_info, form=form)
        else:
            error = "This pokemon does not exist"
            return render_template('pokeapi.html', form=form, error=error)
    return render_template('pokeapi.html', form=form)

