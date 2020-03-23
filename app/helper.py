from dotenv import load_dotenv
from pathlib import Path
import logging
import os
import re

# load environment variables
env_path = Path.cwd() / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

LOG_PATH = os.getenv('LOG_PATH')
LOGGER_NAME='flask-login-gibb'


def ansi_escape(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def validate_input(parameter_list):
    to_be_validated = ' '.join(parameter_list)
    pattern = re.compile(r'^host(?:\s+-[aCdilrTvVw46]+)*(?:\s[^-][a-zA-Z\.\-0-9]+[^\s]){1,2}$')
    return pattern.match(to_be_validated)


def setup_logger(path=LOG_PATH, name=LOGGER_NAME):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(path)
    fh.setLevel(logging.INFO)

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)

    return
