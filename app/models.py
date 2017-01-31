from app import db
from werkzeug.security import check_password_hash, generate_password_hash

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
        user = db.user.find_one({ 'name': username })
        return user

    @staticmethod
    def find(number, page):
        u = number*(page - 1)
#        b = number*page
        users = db.user.find().skip(u).limit(number)
	count = db.user.find().count()
	remainder = count % number
	if remainder == 0:
		count = count // number
	else:
		count = count // number + 1
        return users, count

    @staticmethod
    def save(username, master, password):
        password_hash = generate_password_hash(password)
        _id = db.user.save({ 'name': username, 'master': master, 'password': password_hash })
        return _id

    @staticmethod
    def update(username, master, password):
        password_hash = generate_password_hash(password)
        _id = db.user.update({ 'name': username }, { '$set' : { 'master': master, 'password': password_hash }})
        return _id

    @staticmethod
    def remove(username):
        _id = db.user.remove({ 'name': username })
        return _id


class Domain():

    def __init__(self, domain):
        self.domain = domain
        self.ip = None
        self.directory = None
        self.c_version = None
        self.n_version = None
        self.user = None
        self.password = None

    def get_id(self):
        return self.domain

    @staticmethod
    def find_one(domain):
        domain = db.domain.find_one({ 'domain': domain })
        return domain

    @staticmethod
    def find(number,page):
        u = number*(page-1)
        b = number*page
        domains = db.domain.find().skip(u).limit(b)
        return domains

    @staticmethod
    def save(domain, ip, directory, c_version, n_version, user, password):
        _id = db.domain.save({ 'domain': domain, 'ip': ip, 'directory': directory,'c_version': c_version, 'n_version': n_version, 'user': user, 'password': password })
        return _id

    @staticmethod
    def update(domain, ip, test_directory, directory, c_version, n_version, user, password):
        _id = db.domain.update({ 'domain': domain }, { '$set': { 'ip': ip, 'test_directory': test_directory, 'directory': directory,'c_version': c_version, 'n_version': n_version, 'user': user, 'password': password } })
        return _id

    @staticmethod
    def remove(domain):
        _id = db.domain.remove({ 'domain': domain })
        return _id


