from flask import Flask, url_for, redirect
from flask_login import current_user
from flask_admin import AdminIndexView

from app.models import User

class AdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
           u = User.query.get(current_user.get_id())
           return True
        return False
        
