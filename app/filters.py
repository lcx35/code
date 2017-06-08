#-*- coding: utf8-*-
import time

def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(value))

def username(id):
    if id != 0:
        user = User.query.filter_by(id=id).first()
        #user = db.session.query(user).filter_by(id=id).first()
        if user != None:
            return user.username
        else:
            return "已删除"
    else:
        return "未登录"
