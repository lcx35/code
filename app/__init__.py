from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
#from config import *

app = Flask(__name__)
app.config.from_object('config')
uri = 'mongodb://codeadmin:codeadmin@127.0.0.1/?authSource=admin'
#db = MongoClient(app.config['DATABASE_URI'])
db = MongoClient(uri).codeadmin

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views
