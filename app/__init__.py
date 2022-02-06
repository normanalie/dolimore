from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
admin = Admin()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    admin.init_app(app)

    from . import routes, models
    app.register_blueprint(routes.bp)

    from .dolibarr import Dolibarr
    Dolibarr.config(app.config["DOLIBARR_API_KEY"], app.config["DOLIBARR_BASE_URL"])

    return app

