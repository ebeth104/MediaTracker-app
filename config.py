

class Config(object):
    DEBUG = False
    TESTING = False
    
    SECRET_KEY = "#@$^dskv43423"
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:elib20#@localhost/mydatabase'
    
class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    
    
    SESSION_COOKIE_SECURE = False
    
class TestingConfig(Config):
    TESTING = True

    
    SESSION_COOKIE_SECURE = False
    
config_options = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "test": TestingConfig
}
    