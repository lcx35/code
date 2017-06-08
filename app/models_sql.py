from app import db
from werkzeug.security import check_password_hash, generate_password_hash
import time

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),unique = True)
    password = db.Column(db.String(100))
    master = db.Column(db.String(10))

    def __repr__(self):
        return '<User %r>' % (self.username)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
#        return unicode(self.id)
        return self.id

class Domain(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    domain = db.Column(db.String(50), unique = True)
    ip = db.Column(db.String(15))
    test_directory = db.Column(db.String(50))
    directory = db.Column(db.String(50))
    c_version = db.Column(db.Integer)
    n_version = db.Column(db.Integer)
    user = db.Column(db.String(10))
    password = db.Column(db.String(20))

    def __repr__(self):
        return '<Domain %r>' % (self.Domain)


class Log(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    datetime = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    domain_id = db.Column(db.Integer, default = 0)
    f_version = db.Column(db.Integer, default = 0)
    action = db.Column(db.String(50))
    result = db.Column(db.Integer)


