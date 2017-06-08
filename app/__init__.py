from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .filters import datetimeformat

app = Flask(__name__)

app.config['DEBUG'] = True
#app.config['DEBUG'] = False
#app.config['TESTING'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'code admin'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:XIAOzi2308842@192.168.2.55/codeadmin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.config['DATABASE_URI'] = 'mongodb://codeadmin:codeadmin@123.206.14.167/?authSource=admin'
#app.config['DBHOST'] = '123.206.14.167'
#app.config['DBPORT'] = 27017
#app.config['DBUSER'] = 'codeadmin'
#app.config['DBPASS'] = 'codeadmin'
#app.config['DBAUTH_SOURCE'] = 'admin'
#app.config['DBNAME'] = 'codeadmin'
#app.config['USER_COLLECTION'] = 'user'
#app.config['DOMAIN_COLLECTION'] = 'domain'
#app.config['LOG_COLLECTION'] = 'log'

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


env = app.jinja_env
env.filters['datetimeformat'] = datetimeformat
#env.filters['username'] = username


#@app.context_processor
#def db(table):
#    client = MongoClient(app.config['DBHOST'], app.config['DBPORT'], connect=False)
#    db = client[app.config['DBNAME']]
#    db.authenticate(app.config['DBUSER'], app.config['DBPASS'], app.config['DBAUTH_SOURCE'])
#    coll = db[table]
#    return coll

#from app import views
from app import views
