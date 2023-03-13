from app import db, login
from flask_login import UserMixin # Only use on your User CLass
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

pokemon_team = db.Table(
    'pokemon_team',
    db.Column('owner_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon_caught.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    pokemon_catch = db.relationship('PokemonCaught', secondary=pokemon_team, lazy='dynamic', backref=db.backref('owners', lazy='dynamic'))
    

    # hashes our password
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # check password hash
    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)

    # Use this method to register our user atributes
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    def update_from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']

    # save to our database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    
    def catch_a_pokemon(self, pokemon):
        self.pokemon_catch.append(pokemon)
        db.session.commit()
        
    def remove_a_pokemon(self, pokemon):
        self.pokemon_catch.remove(pokemon)
        db.session.commit()
    
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#New
class PokemonCaught(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String, nullable=False)
    Abilities = db.Column(db.String, nullable=False)
    BaseExperience = db.Column(db.Integer, nullable=False)
    FrontShinyURL = db.Column(db.String, nullable=False)
    AttackBaseStat = db.Column(db.Integer, nullable=False)
    HPBaseStat = db.Column(db.Integer, nullable=False)
    DefenseBaseStat = db.Column(db.Integer, nullable=False)

    def from_dict(self, data):
        self.Name = data['Name']
        self.Abilities = data['Abilities']
        self.BaseExperience = data['BaseExperience']       
        self.FrontShinyURL = data['FrontShinyURL']
        self.AttackBaseStat = data['AttackBaseStat']
        self.HPBaseStat = data['HPBaseStat']
        self.DefenseBaseStat = data['DefenseBaseStat']

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self):
        db.session.commit(self)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()