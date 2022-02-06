from flask import url_for, redirect, request, render_template
from flask_login import current_user
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

from app import db
from app.models import User
from app.forms import SignupForm

class IndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            u = User.query.get(current_user.get_id())
            if u.is_admin:
                return True
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))
        

class UserView(ModelView):
    column_exclude_list = ["password_hash"]

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        form = SignupForm()
        errors = []

        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            is_admin = form.is_admin.data
            u = User(username=username, email=email, is_admin=is_admin)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('admin.index'))
        
        if request.method == 'POST' and not form.validate():
            errors.append(form.errors)

        return self.render('admin/signup.html', form=form, errors=errors)