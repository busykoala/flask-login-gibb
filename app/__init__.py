from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config['SECRET_KEY'] = 'whatever'
app.config['SESSION_TYPE'] = 'filesystem'


from app import routes  # noqa