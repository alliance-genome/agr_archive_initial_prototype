import os

class Config(object):
    WEBPACK_MANIFEST_PATH = './build/manifest.json'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRODUCTION = False

    def print_config(config):
        print "Running with Config: "
        print "\tDEBUG: " + str(config.DEBUG)
        print "\tAPI_PASSWORD: " + str(config.API_PASSWORD)
        print "\tSQLALCHEMY_ECHO: " + str(config.SQLALCHEMY_ECHO)
        print "\tSQLALCHEMY_DATABASE_URI: " + str(config.SQLALCHEMY_DATABASE_URI)
        print "\tES_INDEX: " + str(config.ES_INDEX)
        print "\tES_HOST: " + str(config.ES_HOST)
        print "\tES_AWS: " + str(config.ES_AWS)
        print "\tPRODUCTION: " + str(config.PRODUCTION)

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    if 'API_PASSWORD' in os.environ and os.environ['API_PASSWORD']:
        API_PASSWORD = os.environ['API_PASSWORD']
    if 'DATABASE_URL' in os.environ and os.environ['DATABASE_URL']:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    if 'ES_INDEX' in os.environ and os.environ['ES_INDEX']:
        ES_INDEX = os.environ['ES_INDEX']
    if 'ES_HOST' in os.environ and os.environ['ES_HOST']:
        ES_HOST = os.environ['ES_HOST']
    ES_AWS = True
    PRODUCTION = True

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

    if 'API_PASSWORD' in os.environ and os.environ['API_PASSWORD']:
        API_PASSWORD = os.environ['API_PASSWORD']
    else:
        API_PASSWORD = 'api_password'

    if os.environ['DATABASE_URL']:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

    if 'ES_INDEX' in os.environ and os.environ['ES_INDEX']:
        ES_INDEX = os.environ['ES_INDEX']
    else:
        ES_INDEX = 'searchable_items_blue'

    if 'ES_HOST' in os.environ and os.environ['ES_HOST']:
        ES_HOST = os.environ['ES_HOST']
    else:
        ES_HOST = '127.0.0.1:9200'

    ES_AWS = False

    def __init__(self):
        Config.print_config(self)

