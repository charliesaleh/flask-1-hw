from flask import render_template, request, redirect, url_for, flash
import requests, random
from app.blueprints.main import main
from flask_login import login_required, current_user
from app.blueprints.auth.forms import PokemonForm, PokemonBattleForm
from ...models import PokemonCaught, User

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



@main.route("/pokemon_catch/<pokemon_name>")
@login_required
def pokemon_catch(pokemon_name):
    pokemon_catch = PokemonCaught.query.filter_by(Name=pokemon_name).first()
    if pokemon_catch:
        if current_user.pokemon_catch.count() < 5:

            current_user.catch_a_pokemon(pokemon_catch)
            flash(f'You caught {pokemon_name} and has now been added to your team!', 'success')
            return redirect(url_for('main.pokeapi'))
        else:
            flash(f'Team is full! You cannot add {pokemon_name} because your team is full!', 'danger')
            return redirect(url_for('main.pokeapi'))
    else:
        if current_user:
            pokemon_name = pokemon_name
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
                    "DefenseBaseStat": pokemon["stats"][2]["base_stat"]
                    }
                pokemon = PokemonCaught()
                pokemon.from_dict(get_pokemon_info)
                pokemon.save_to_db()
                current_user.catch_a_pokemon(pokemon)
                flash(f'You caught {pokemon_name} and has now been added to your team!', 'success')
                return redirect(url_for('main.pokeapi'))
            else:
                flash(f'Team is full! You cannot add {pokemon_name} because your team is full!', 'danger')
        return redirect(url_for('main.pokeapi'))



@main.route("/pokemon_team")
@login_required
def pokemon_team():
    pokemons = current_user.pokemon_catch.all()
    return render_template("pokemon_team.html", pokemons=pokemons)

@main.route('/remove_pokemon/<int:pokemon_id>', methods=['GET'])
@login_required
def remove_pokemon(pokemon_id):
    pokemon = PokemonCaught.query.get(pokemon_id)
    if pokemon is not None:
        current_user.remove_a_pokemon(pokemon)
        pokemon.delete_from_db()
        flash(f'{pokemon.Name} has been removed from your team.', 'success')
    else:
        flash(f'Pokemon not found.', 'danger')
    return redirect(url_for('main.pokemon_team'))




@main.route('/pokemon_battle', methods=['GET', 'POST'])
@login_required
def pokemon_battle():
    form = PokemonBattleForm()
    opponent = None
    if request.method == 'POST' and form.validate_on_submit():
        opponent = User.query.filter_by(email=form.opponent_email.data).first()
        if opponent is not None:
            current_user_pokemon = current_user.pokemon_catch.first()
            opponent_pokemon = opponent.pokemon_catch.first()
            winner = calculate_winner(current_user_pokemon, opponent_pokemon)
            if winner == current_user_pokemon:
                flash(f'You won the battle against {opponent.first_name}!', 'success')
            elif winner == opponent_pokemon:
                flash(f'You lost the battle against {opponent.first_name}!', 'danger')
            else:
                flash(f'The battle between you and {opponent.first_name} resulted in a draw!', 'info')
            return redirect(url_for('main.pokemon_team'))
        else:
            flash(f'Opponent with email {form.opponent_email.data} not found!', 'danger')
            return redirect(url_for('main.pokemon_battle'))
    return render_template('pokemon_battle.html', form=form, opponent=opponent)


def calculate_winner(pokemon1, pokemon2):
    total_stats1 = pokemon1.HPBaseStat + pokemon1.AttackBaseStat + pokemon1.DefenseBaseStat
    total_stats2 = pokemon2.HPBaseStat + pokemon2.AttackBaseStat + pokemon2.DefenseBaseStat
    if total_stats1 > total_stats2:
        return pokemon1
    elif total_stats1 < total_stats2:
        return pokemon2
    else:
        return None

