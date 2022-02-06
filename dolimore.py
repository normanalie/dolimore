from app import create_app, db, admin

from app.admin_views import IndexView, UserView
from app.models import User

admin.index_view = IndexView()
admin.add_view(UserView(User, db.session))

app = create_app()