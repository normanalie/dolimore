from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.login'
admin = Admin()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    from . import routes, mailing, contract, models
    app.register_blueprint(routes.bp)
    app.register_blueprint(mailing.bp, url_prefix="/mailing")
    app.register_blueprint(contract.bp, url_prefix="/contract")

    from .admin_views import IndexView
    admin.init_app(app, index_view=IndexView())

    from .mailing.dolibarr import Dolibarr
    Dolibarr.config(app.config["DOLIBARR_API_KEY"], app.config["DOLIBARR_BASE_URL"])

    return app

