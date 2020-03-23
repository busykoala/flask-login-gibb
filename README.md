# 183_lb3_gruppe2

This project is a school training for creating a login route and basic
command execution using flask.

## Project Documentation

### Login using HTTP-Post

There is a login implemented.
`werkzeug.security.generate_password_hash` implements storing individually
salted passwords. Also as an additional security step a pepper is implemented.
Both are implemented on the `User` model (`app.models.User`).

With our implementation of the registering form it is possible to create
a new user e.g. with username `lb3` and password `sml12345`.

###  Session-Handling

Thanks to the package `flask-login` we can implement session handling easily.
By using the decorator `@login_required` the session cookie is checked
for whether the user is logged in. Sessions are set using the `login_user()`
and destroyed with `logout_user()`.

### System command 'host'

The application implements the system command `host`. It enables logged in
users to call `host` with the user which runs the application.

### Logging

Apart from the logs done by the libraries implemented we set a logger with
INFO level using a filehandler plus we are logging the DEBUG level into
standardout.

### Persistent and save password storage.

We use individual salts (implemented by `werkzeug.security.generate_password_hash`)
and a global pepper. The passwords are then stored in a sqlite3 database.

Using individual salts we make rainbow table attacks very inefficient.
Additionally the pepper will prevent dictionary attacks in case of a
database exploit.

### SSL/TLS

This is not part of the application. The installed production server
`gunicorn` lets you start the application using a private-public key pair
and choose the port.
The command is documented in the section `Run`.

### GUI

The Application has a very nice GUI. We implemented the command input/output
as it was in a shell environment with dark background and a prompt.

The menu is a basic bootstrap menu having the familiar icons for login/register
and for the logout.

Also the home button is customized so that the user can see that he is logged
in.

### Registering new User

There is a registering view for registering new users. When registering new
users the uniqueness of the username and email is ensured.

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

# add .env file holding the flask secret (csrf), the password pepper and the path to the log file.
# SECRET_KEY="very-secret"
# PEPPER="very-secret"
# LOG_PATH="/var/log/flask-login-gibb.log"
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
# development server
flask run

# production server
gunicorn app:app -w <workers> --bind <host>:<port>

# production server with ssl
gunicorn --certfile=server.crt --keyfile=server.key --bind 0.0.0.0:443 app:app
```
