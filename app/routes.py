from app import app
from app import db
from app.forms import CommandForm
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.helper import ansi_escape
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


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': current_user.username.capitalize()}
    return render_template('index.html', title='Home', user=user)


@app.route('/command')
@login_required
def command():
    form = CommandForm(request.args)
    if request.args.get('submit', False):
        command = form.command.data
        if not command:
            return render_template('command.html', title='Command', form=form,
                                   errors=['This field is required.'])
        try:
            ex_command = ['ls', '-hal']
            ex_command.extend(quote(command).split())
            output = check_output(ex_command, stderr=STDOUT).decode()
        except Exception as e:
            return render_template('command.html', title='Command', form=form,
                                   errors=[str(e)])

        ansi_escaped = ansi_escape(output)
        htmlified = ansi_escaped.replace('\n', '<br>')
        return render_template('command.html', title='Command', form=form,
                               output=htmlified)

    return render_template('command.html', title='Command', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)
