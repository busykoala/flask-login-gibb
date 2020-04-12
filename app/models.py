from app import db
from app import login
from dotenv import load_dotenv
from flask_login import UserMixin
from pathlib import Path
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import os

# load environment variables
env_path = Path.cwd() / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

PEPPER = os.getenv('PEPPER')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        peppered_pw = f'{PEPPER}{password}'
        self.password_hash = generate_password_hash(
            peppered_pw, method='pbkdf2:sha512', salt_length=10)

    def check_password(self, password):
        peppered_pw = f'{PEPPER}{password}'
        return check_password_hash(self.password_hash, peppered_pw)
