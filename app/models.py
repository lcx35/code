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
    def find(number,page):
        u = number*(page-1)
        b = number*page
        users = db.user.find().skip(u).limit(b)
        return users

    @staticmethod
    def save(username, master, password):
        password_hash = generate_password_hash(password)
        _id = db.user.save({ 'name': username, 'master': master, 'password': password_hash })
        return _id

    @staticmethod
    def update(username, password):
        password_hash = generate_password_hash(password)
        _id = db.user.update({ 'name': username }, { '$set' : { 'password': password_hash }})
        return _id

    @staticmethod
    def remove(username):
        _id = db.user.remove({ 'name': username })
        return _id


