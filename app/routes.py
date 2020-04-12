from app import app
from app import db
from app.forms import CommandForm
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.helper import ansi_escape
from app.helper import LOGGER_NAME
from app.helper import validate_input
from app.models import User
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from shlex import quote
from subprocess import STDOUT
from subprocess import check_output
import logging

logger = logging.getLogger(LOGGER_NAME)


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': current_user.username.capitalize()}
    username = user['username']
    form = CommandForm(request.args, meta={'csrf': False})
    if request.args.get('submit', False):
        command = form.name.data
        if not command:
            logger.debug('Route /index was called without a command.')
            return render_template('index.html', title='Command', form=form,
                                   errors=['This field is required.'],
                                   user=username)
        ex_command = ['host']
        ex_command.extend([quote(x) for x in command.split()])
        if not validate_input(ex_command):
            flash(f'Invalid input.')
            logger.error(f'Regex did not match at /index call.')
            return render_template('index.html', title='Command', form=form,
                                   errors=['Invalid input.'], user=username)
        try:
            output = check_output(ex_command, stderr=STDOUT).decode()
        except Exception as e:
            flash(f'Invalid input.')
            logger.error(f'Route /index was called with error {e}')
            return render_template('index.html', title='Command', form=form,
                                   errors=['Invalid input.'], user=username)

        ansi_escaped = ansi_escape(output)
        htmlified = ansi_escaped.replace('\n', '<br>')
        logger.debug('Route /index was called and returned htmlified data.')

        return render_template('index.html', title='Command', form=form,
                               output=htmlified, user=username)

    return render_template('index.html', title='Command', form=form,
                           user=username)


@app.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    logger.debug(f'User "{username}" successfully logged out.')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        logger.debug(f'Logged in user "{current_user.username}" called /login.')
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            logger.info('Undefined User or invalid PW (called /login).')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        logger.info(f'User "{user.username}" successfully logged in.')
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form,
                           user='Guest')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        logger.debug(f'Logged in user "{current_user.username}" called /register.')
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        logger.debug(f'New user "{user.username}" successfully registered.')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form,
                           user='Guest')
