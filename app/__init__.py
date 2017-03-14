from flask import Flask
from flask_login import LoginManager
from .filters import datetimeformat

app = Flask(__name__)

#app.config['DEBUG'] = True
app.config['DEBUG'] = False
app.config['TESTING'] = False
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'code admin'

app.config['DATABASE_URI'] = 'mongodb://codeadmin:codeadmin@123.206.14.167/?authSource=admin'

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

env = app.jinja_env
env.filters['datetimeformat'] = datetimeformat

from app import views
