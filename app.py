from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])

def home():
    return render_template('home.html')

@app.route('/pokeapi', methods=['GET', 'POST'])
def pokeapi():
    print(request.method)
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name')
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
                "AttackBaseStat": pokemon["stats"][0]["base_stat"],
                "HPBaseStat": pokemon["stats"][0]["base_stat"],
                "DefenseBaseStat": pokemon["stats"][0]["base_stat"],
                }
            print(get_pokemon_info)
            return render_template('pokeapi.html', get_pokemon_info=get_pokemon_info)
        else:
            "This pokemon does not exist"
    return render_template('pokeapi.html')
