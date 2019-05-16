import os 
basedir = os.path.abspath(os.path.dirname(__file__))



class Config(object):
	DB_CONFIG = {
	    'host': 'localhost',
	    'port': '5432',
	    'database': 'localdatabase',
	    'user': 'postgres',
	    'password': 'root',
	    }
	SQLALCHEMY_DATABASE_URI = "postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s" % DB_CONFIG
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = 'thisissecretkey'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	# run command export DATABASE_URL="postgresql://localdatabase"
	# python manage.py db init
	# python manage.py db migrate
	# python manage.py db upgrade



class DevelopmentConfig(Config):
	DEBUG = True
	DEVELOPMENT = True




class ProductionConfig(Config):
	DEBUG = False



class StagingConfig(Config):
	DEBUG = True
	DEVELOPMENT = True



class TestingConfig(Config):
	DEBUG = True