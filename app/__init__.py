from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'


from app import routes, models


# ADMIN PANEL
from app.admin_views import IndexView, UserView
from app.models import User


admin = Admin(app, index_view=IndexView())

admin.add_view(UserView(User, db.session))