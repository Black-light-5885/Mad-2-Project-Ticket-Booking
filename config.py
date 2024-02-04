
from datetime import datetime, timedelta


SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
SECRET_KEY = 'ticketsecretkey'
SECURITY_PASSWORD_SALT = 'ticketsaltkey'
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False
SECURITY_TOKEN_AUTHENTICATION_HADER = 'Authentication-Token'
JWT_DEFAULT_REALM = 'reapers_domain'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
CACHE_TYPE = 'RedisCache'
CACHE_REDIS_HOST = 'localhost'
CACHE_REDIS_PORT = 6379
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'bookforyou483@gmail.com'
MAIL_PASSWORD = 'xyx'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
