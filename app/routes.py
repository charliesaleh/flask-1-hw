from flask import render_template, request
import requests
from app.forms import PokemonForm, LoginForm, SignUpForm
from app import app

# ROUTES SECTION

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if email in app.config.get('REGISTERED_USERS') and password == app.config.get('REGISTERED_USERS').get(email).get('password'):
            return f'Successfully logged in! Hello, {app.config.get("REGISTERED_USERS").get(email).get("name")}'
        else:
            error = 'Invalid email or password'
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if email in app.config.get('UNREGISTERED_USERS') and password == app.config.get('UNREGISTERED_USERS').get(email).get('password'):
            return f'Successfully signed up! Hello, {app.config.get("UNREGISTERED_USERS").get(email).get("name")}'
        else:
            return render_template('sign_up.html', form=form)
    return render_template('sign_up.html', form=form)

@app.route('/pokeapi', methods=['GET', 'POST'])
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
