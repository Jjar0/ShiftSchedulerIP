from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shifts.db'

db = SQLAlchemy(app)
loginManager = LoginManager(app)
loginManager.login_view = 'login'

from shiftapp import routes