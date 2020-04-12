from app.helper import setup_logger
from app.helper import LOGGER_NAME
from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_sqlalchemy import SQLAlchemy
import logging



# init logging
setup_logger()

logger = logging.getLogger(LOGGER_NAME)
logger.debug('Logger was setup successfully.')

# init application
app = Flask(__name__)
logger.debug('App was setup successfully.')

# init login manager and set redirect for unauthorized
login = LoginManager(app)
login.login_view = "login"
# set to logged out if session has different originating IP
login.session_protection = "strong"

# load config variables
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

seeder = FlaskSeeder()
seeder.init_app(app, db)

logger.debug('App config was setup successfully.')

from app import routes  # noqa
from app import models  # noqa
