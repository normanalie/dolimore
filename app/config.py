"""Flask DEVELOPMENT configuration."""
"""
To start app: 
    set FLASK_APP=app
    set FLASK_DEBUG=True
    set FLASK_ENV=development
    flask run
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))


TESTING = True
DEBUG = True
DEVELOPMENT = True
SECRET_KEY = '247MKgKxgc'

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False