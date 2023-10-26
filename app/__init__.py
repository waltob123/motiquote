from flask import Flask
from app.database.db import init_db
from app.models.models import Base

init_db(Base)

app = Flask(__name__)

from .main.route import main
from .users.route import users

app.register_blueprint(main)
app.register_blueprint(users, url_prefix='/users')