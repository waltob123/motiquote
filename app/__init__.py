import os
from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
from app.database.db import init_db
from app.models.models import Base

load_dotenv()

init_db(Base)

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)


from .main.route import main
from .auth.route import auth

app.register_blueprint(main)
app.register_blueprint(auth)
