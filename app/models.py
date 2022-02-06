from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User: {self.username}>'


@login.user_loader  # Give the user object to flask-login based on the id
def user_loader(id):
    return User.query.get(int(id))  # user_loader give a id:string, db need id:int