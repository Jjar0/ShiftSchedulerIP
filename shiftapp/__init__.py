from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from datetime import datetime

# get the base package path
base_dir = os.path.abspath(os.path.dirname(__file__))

# create the Flask app + static and template folders
app = Flask(
    __name__,
    static_folder=os.path.join(base_dir, 'static'),
    template_folder=os.path.join(base_dir, 'templates')
)

# app config
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shifts.db'

# init database
db = SQLAlchemy(app)

# setup login manager
loginManager = LoginManager(app)
loginManager.login_view = 'login'  # redirect if not logged in

from shiftapp.models import User

# load user
@loginManager.user_loader
def loadUser(userId):
    return User.query.get(int(userId))

# import routes
from shiftapp import routes

# filter to get weekday from date string
@app.template_filter('weekday')
def weekdayFilter(dateStr):
    try:
        dt = datetime.strptime(dateStr, "%Y-%m-%d")
        return dt.strftime("%A")  # returns full weekday name like "Monday"
    except Exception:
        return "Invalid"


