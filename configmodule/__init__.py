import os, logging
from distutils.util import strtobool

basedir = os.path.abspath(__file__ + "/../../")
print basedir

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SSL_DISABLE = False
	SQLALCHEMY_RECORD_QUERIES = True	
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = os.environ.get('MAIL_PORT', 465)
	MAIL_USE_SSL = bool(strtobool(os.environ.get('MAIL_USE_SSL')))
	MAIL_USE_TLS = bool(strtobool(os.environ.get('MAIL_USE_TLS')))
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	MAIL_SUBJECT_PREFIX = '[Michigan Hackers]'
	MAIL_SENDER = 'Michigan Hackers <michiganhackers@umich.edu>'
	
	TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
	TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
	TWILIO_FROM_NUMBER = os.environ.get('TWILIO_FROM_NUMBER')

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	TWILIO_TEST_SEND_TO_NUMBER = os.environ.get('TWILIO_TEST_SEND_TO_NUMBER')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
	TESTING = True
	SERVER_NAME = 'localhost'
	TWILIO_TEST_SEND_TO_NUMBER = os.environ.get('TWILIO_TEST_SEND_TO_NUMBER')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
	WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data.sqlite')

	@classmethod
	def init_app(cls, app):
		Config.init_app(app)

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}

