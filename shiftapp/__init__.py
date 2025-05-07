from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# create Flask app
app = Flask(__name__)

# app config: secret key and DB path
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shifts.db'

# init database
db = SQLAlchemy(app)

# setup login manager
loginManager = LoginManager(app)
loginManager.login_view = 'login'  # redirect here if not logged in

from shiftapp.models import User

# tell Flask-Login how to load a user from session
@loginManager.user_loader
def loadUser(userId):
    return User.query.get(int(userId))

# import routes so they register with app
from shiftapp import routes
