#class Config(object):
#    DEBUG = False
#    TESTING = False
#    WTF_CSRF_ENABLED = True
#    SECRET_KEY = 'code admin'
#    DATABASE_URI = 'mongodb://codeadmin:codeadmin@123.206.14.167/codeadmin?authMechanism=SCRAM-SHA-1'
#
#class ProductionConfig(Config):
#
#class DevelopmentConfig(Config):
#    DEBUG = True
#
#class TestingConfig(Config):
#    TESTING = True


DEBUG = True
TESTING = False
WTF_CSRF_ENABLED = True
SECRET_KEY = 'code admin'
DATABASE_URI = 'mongodb://codeadmin:codeadmin@127.0.0.1:27017/codeadmin?authMechanism=SCRAM-SHA-1'
