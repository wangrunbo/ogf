# App
DEBUG = False
BCRYPT_LEVEL = 13

# Session
SECRET_KEY = '\x1b\xae\xa6\xe2\x97\t\xe4\\\x12v\xf6B\x1a!E\xd5\xdcL\xb3T\xe6?\xd9\xec'
PERMANENT_SESSION_LIFETIME = 3600

# DataResource
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@host/db?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# Form
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = '9\x0ct:\xa7.r\xbc\x9b\xd8\xa6\xec\xfb\x0c\x9e\xee\x98\xd4>x]N8\x06'

# Mail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = None
MAIL_MAX_EMAILS = None

# Config
TOKEN_SALT = 'QokRn0cWdaYyF9HWGDFKssHPjSJhaBZ5mdS-U3eCwt2OLphVTKz7BUrsjPjenUy88wLnojITvX-EDR3FCyjA'
