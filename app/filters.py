
#-*- coding: utf8-*-

import time

def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, time.localtime(value))


