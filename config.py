import os

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or "Ineedtochangethis"
  HOST = ""
  LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
  DEBUG = True
  API_KEY = os.environ.get('API_KEY')
  API_SEC = os.environ.get('API_SEC')
  POSTGRES_PASS = os.environ.get('POSTGRES_PASS')
  SHOPIFY_HOST = os.environ.get('SHOPIFY_HOST')


  POSTGRES = {
    'user': 'benlehman',
    'pw': POSTGRES_PASS,
    'db': 'mapping',
    'host': 'localhost',
    'port': '5432'
  }

  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  SHOPIFY_CONFIG = {
    'API_KEY': API_KEY,
    'API_SEC': API_SEC,
    'HOST': SHOPIFY_HOST,
    'API_VERSION': "2019-07"
  }