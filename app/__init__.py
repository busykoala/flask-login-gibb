from config import Config
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path


# load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


# init application
app = Flask(__name__)

# init login manager and set redirect for unauthorized
login = LoginManager(app)
login.login_view = "login"
# set to logged out if session has different originating IP
login.session_protection = "strong"

# load config variables
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes  # noqa
from app import models  # noqa
