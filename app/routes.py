from flask import render_template, request, flash, redirect, url_for
import requests
from app.forms import PokemonForm, LoginForm, RegistrationForm
from app.models import User
from app import app
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user

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
        
        # Query from our db
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Successfully logged in! Welcome back, {queried_user.first_name}!', 'success')
            login_user(queried_user)
            return redirect(url_for('home'))
        else:
            error ='Invalid email or password'
            flash(error, 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user:
        logout_user()
        flash(f'Successfully logged out!', 'warning')
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Grabbimg our form data and store it into dict
        new_user_data = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': form.password.data
        }
        #Create instance of our user
        new_user = User()
        # Impletemening values from out form data for our instance
        new_user.from_dict(new_user_data)
        #Save to our database
        new_user.save_to_db()
        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

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
