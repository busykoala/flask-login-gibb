from pathlib import Path
import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.path.join('sqlite:///',
                                           Path('.') / 'application.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')

    # only allow for https
    # SESSION_COOKIE_SECURE = True
    # secure remember_me cookie from flask_login
    # REMEMBER_COOKIE_SECURE = True

    # XSS Protection (CSRF protection already because of wtf-forms)
    # SESSION_COOKIE_HTTPONLY = True
    # REMEMBER_COOKIE_HTTPONLY = True
