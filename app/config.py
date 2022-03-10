"""Flask DEVELOPMENT configuration."""
"""
To start app: 
    set FLASK_APP=app
    set FLASK_DEBUG=True
    set FLASK_ENV=development
    set DOLIBARR_API_KEY=yourDolibarrApiKey
    set DOLIBARR_URL=yourDolibarrURL
    flask run
"""

import os
import pymysql
basedir = os.path.abspath(os.path.dirname(__file__))



TESTING = True
DEBUG = True
DEVELOPMENT = True
SECRET_KEY = os.environ.get('SECRET_KEY') or '247MKgKxgc'

UPLOAD_FOLDER = "static/files/upload"
EXPORT_FOLDER = "static/files/export"

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

DOLIBARR_API_KEY = os.environ.get('DOLIBARR_API_KEY')
DOLIBARR_BASE_URL = os.environ.get('DOLIBARR_URL')