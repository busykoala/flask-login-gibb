# 183_lb3_gruppe2

This project is a school training for creating a login route and basic
command execution using flask.

## Install

```
# clone and install dependencies in a virtual environment
git clone git@gitlab.iet-gibb.ch:mos111952/183_lb3_gruppe2.git
cd 183_lb3_gruppe2
python3 -m venv venv
source venv/bin/activate
python setup.py install

# initialize the database
flask db init

# add .env file holding the flask secret (csrf)
echo "SECRET_KEY=very-secret" > .env
```

## Migrate

```
# migrate table users
flask db migrate -m "users table"

# upgrade
flask db upgrade
```

## Run

```
flask run
```
