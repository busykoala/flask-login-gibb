# 183_lb3_gruppe2

This project is a school training for creating a login route and basic
command execution using flask.

## Project Documentation

### Requirements Overview

| Requirement                                                  | implemented                                         | implemented in    |
| ------------------------------------------------------------ | --------------------------------------------------- | ----------------- |
| Login over HTTP-POST with user 'lb3' and password 'sml12345' | ✓                                                   | `app/routes.py`   |
| Session-Handling post-login for executing the sys command    | ✓                                                   | `app/routes.py`   |
| Sys command over HTTP-GET ('name="sysopt"')                  | ✓ (requires additional parameter `&submit=Execute`) | `app/routes.py`   |
| Logging over STDOUT/ERR or log file                          | ✓ (both possible)                                   | `app/helper.py`   |
| Secure and persistent password storage                       | ✓                                                   | `app/models.py`   |
| Encrypted communication over ssl                             | ✓ (via `gunicorn`)                                  | (see [Run](#run)) |
| (Optional) Seucure user creation over GUI                    | ✓                                                   | `app/routes.py`   |
| (Optional) Useful and appealing GUI / UX                     | ✓                                                   | (see [GUI](#gui)) |

### Models

The application currently requires uses a user model, used for authentication against the application.

```py
# app/models.py

id = db.Column(db.Integer, primary_key=True)
username = db.Column(db.String(64), index=True, unique=True)
email = db.Column(db.String(120), index=True, unique=True)
password_hash = db.Column(db.String(128))
```

### User Registration

New users can register via the sign-up form at `/register`. When registering new users the uniqueness of the username and email is ensured.

### User Authentication & persistent password storage

The dependency `werkzeug.security.generate_password_hash` implements storing individually salted passwords. As an additional security measure an application specific pepper is used, making brute-force, as well as rainbow table and dictionary attacks infeasible.

```py
# app/models.py

def set_password(self, password):
    peppered_pw = f'{PEPPER}{password}'
    self.password_hash = generate_password_hash(
        peppered_pw, method='pbkdf2:sha512', salt_length=10)

def check_password(self, password):
    peppered_pw = f'{PEPPER}{password}'
    return check_password_hash(self.password_hash, peppered_pw)
```

All routes with exception of the `/login` and `register` route require authentication.

### Session-Handling

The session handling mechanism is provided by the `flask-login` dependency. By using the decorator `@login_required` the according session cookie is checked for whether the user is logged in. Sessions are set using the `login_user()` and destroyed with `logout_user()`, implemented in `routes.py`.

### System command 'host'

The application implements the system command `host`. It enables logged in users to call `host` with the user which runs the application.

To prevent command injections the user input is matched against a regex containing all whitelisted command parameters:

```py
# app/helper.py

to_be_validated = ' '.join(parameter_list)
pattern = re.compile(r'^host(?:\s+-[aCdilrTvVw46]+)*(?:\s[^-][a-zA-Z\.\-0-9]+[^\s]){0,2}$')
return pattern.match(to_be_validated)
```

As an additional security measure, all user-supplied parameters are quoted prior to being executed.

Prior to rendering the response, the command output is escaped to avoid any kind of HTML injection:

```py
# app/routes.py

try:
    output = check_output(ex_command, stderr=STDOUT).decode()

# ...

ansi_escaped = ansi_escape(output)
htmlified = ansi_escaped.replace('\n', '<br>')
logger.debug('Route /index was called and returned htmlified data.')

return render_template('index.html', title='Command', form=form,
                        output=htmlified, user=username)
```

### Logging

Apart from the logs done by the libraries implemented we set a logger with INFO level using a log file, which is located at a user-defined path.

Additionally the DEBUG level is logged to the standard output.

### SSL/TLS

This is not part of the application. The installed production server `gunicorn` lets you start the application using a private-public key pair and choose the port. For more information on enabling SSL/TLS visit the [Run](#run) section.

### GUI

The Application uses a functional GUI with supportive UI styling. The command input/output simulates a shell environment by using a dark background with a blue-ish font.

The menu is a basic bootstrap menu utilizing familiar icons for login/register and for the logout. The home button is customized so that the users can see whether they are logged in.

Notifications are highlighted by using a different background color.

## Install

### Using docker (development only)

Currently a docker build can be used for local development.

```sh
# Clone the project
git clone git@gitlab.iet-gibb.ch:mos111952/183_lb3_gruppe2.git
cd 183_lb3_gruppe2

# Build the containers
docker build --tag 183_lb3_gruppe2:0.1 .

# Run the container and expose port 5000
docker run -p 5000:5000 183_lb3_gruppe2:0.1
```

### Manual Install

```sh
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

#### Migration

```sh
# migrate table users
flask db migrate -m "users table"

# upgrade
flask db upgrade

# add lb3 user to database
flask seed run
```

#### Run

```sh
# development server
flask run

# production server
gunicorn app:app -w <workers> --bind <host>:<port>

# production server with ssl
gunicorn --certfile=server.crt --keyfile=server.key --bind 0.0.0.0:443 app:app
```
