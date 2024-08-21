from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userOnly'

@login_manager.user_loader
def load_user(user_id):
    return models.Accounts.query.get(int(user_id))
    
migrate = Migrate(app, db)


from app import views, models
