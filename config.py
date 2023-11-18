

class Config(object):
    DEBUG = False
    TESTING = False
    
    SECRET_KEY = "YOUR SECRET KEY"
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:password@localhost/mydatabase'
    
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
    
