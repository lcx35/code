#from config import *
from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from .filters import datetimeformat


app = Flask(__name__)

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'code admin'

#app.config.from_object('config')
app.config['DATABASE_URI'] = 'mongodb://codeadmin:codeadmin@123.206.14.167/?authSource=admin'

#uri = 'mongodb://codeadmin:codeadmin@123.206.14.167/?authSource=admin'
db = MongoClient(app.config['DATABASE_URI']).codeadmin
#db = MongoClient(uri).codeadmin

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

#env = Environment(loader=FileSystemLoader('/data/www/code/app/static'))
env = app.jinja_env
env.filters['datetimeformat'] = datetimeformat

from app import views
