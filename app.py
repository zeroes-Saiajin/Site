from flask import Flask
from flask_login import LoginManager
from pony.flask import Pony
from model import db
from configuration import config

app = Flask(__name__)
app.config.update(config)

Pony(app)
login_manager = LoginManager(app)
login_manager.nickname_view_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.User.get(id=user_id)