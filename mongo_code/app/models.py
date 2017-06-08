from app import app
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
import time

#db = MongoClient(app.config['DATABASE_URI'], connect=False).codeadmin
client = MongoClient(app.config['DBHOST'], app.config['DBPORT'], connect=False)
#client = MongoClient(app.config['DBHOST'], app.config['DBPORT'])
db = client[app.config['DBNAME']]
db.authenticate(app.config['DBUSER'], app.config['DBPASS'], app.config['DBAUTH_SOURCE'])
user_coll = db[app.config['USER_COLLECTION']]
domain_coll = db[app.config['DOMAIN_COLLECTION']]
log_coll = db[app.config['LOG_COLLECTION']]


class User():

    def __init__(self, username):
        self.username = username
        self.password = None
        self.master = None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

    @staticmethod
    def find_one(username):
        user = user_coll.find_one({ 'name': username })
        return user

    @staticmethod
    def find(number, page):
        u = number*(page - 1)
        users = user_coll.find().skip(u).limit(number)
	count = user_coll.find().count()
	remainder = count % number
	if remainder == 0:
		count = count // number
	else:
		count = count // number + 1
        return users, count

    @staticmethod
    def save(username, master, password):
        password_hash = generate_password_hash(password)
        _id = user_coll.save({ 'name': username, 'master': master, 'password': password_hash })
        return _id

    @staticmethod
    def update(username, master, password):
        password_hash = generate_password_hash(password)
        _id = user_coll.update({ 'name': username }, { '$set' : { 'master': master, 'password': password_hash }})
        return _id

    @staticmethod
    def remove(username):
        _id = user_coll.remove({ 'name': username })
        return _id


class Domain():

    def __init__(self, domain):
        self.domain = domain
        self.ip = None
        self.test_directory = None
        self.directory = None
        self.c_version = None
        self.n_version = None
        self.user = None
        self.password = None

    def get_id(self):
        return self.domain

    @staticmethod
    def find_one(domain):
        domain = domain_coll.find_one({ 'domain': domain })
        return domain

    @staticmethod
    def find(number,page):
        u = number*(page - 1)
        domains = domain_coll.find().skip(u).limit(number)
	count = domain_coll.find().count()
	remainder = count % number
	if remainder == 0:
		count = count // number
	else:
		count = count // number + 1
        return domains, count

    @staticmethod
    def save(domain, ip, test_directory, directory, c_version, n_version, user, password):
        _id = domain_coll.save({ 'domain': domain, 'ip': ip, 'test_directory': test_directory, 'directory': directory,'c_version': c_version, 'n_version': n_version, 'user': user, 'password': password })
        return _id

    @staticmethod
    def update(domain, ip, test_directory, directory, c_version, n_version, user, password):
        _id = domain_coll.update({ 'domain': domain }, { '$set': { 'ip': ip, 'test_directory': test_directory, 'directory': directory,'c_version': c_version, 'n_version': n_version, 'user': user, 'password': password } })
        return _id

    @staticmethod
    def remove(domain):
        _id = domain_coll.remove({ 'domain': domain })
        return _id


class Log():

    def __init__(self, username):
        self.username = username
        self.datetime = None
        self.action = None
        self.result = None

    @staticmethod
    def save(username, action, result):
        datetime = int(time.time())
        _id = log_coll.save({ 'datetime': datetime, 'username': username, 'action': action, 'result': result})
        return _id

    @staticmethod
    def find(number,page):
	count = log_coll.find().count()
        u = number*(page-1)
        logs = log_coll.find().sort([('datetime', -1)]).skip(u).limit(number)
	remainder = count % number
	if remainder == 0:
		count = count // number
	else:
		count = count // number + 1
        return logs, count
