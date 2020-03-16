from pathlib import Path
import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.path.join('sqlite:///',
                                           Path('.') / 'application.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
