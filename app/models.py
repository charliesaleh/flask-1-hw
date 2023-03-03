from app import db, login
from flask_login import UserMixin # Only use on your User CLass
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    # hashes our password
    def hash_password(self, original_password):
        return generate_password_hash(original_password)


    # check password hash
    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)

    # Use this method to register our user aatributes
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    # save to our database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)