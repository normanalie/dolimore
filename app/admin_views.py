from flask import Flask, url_for, redirect
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from app.models import User

class IndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            u = User.query.get(current_user.get_id())
            if u.is_admin:
                return True
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))
        

class UserView(ModelView):
    column_exclude_list = ["password_hash"]
