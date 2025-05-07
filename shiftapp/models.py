from shiftapp import db
from flask_login import UserMixin

# user model for database and login system
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # unique user ID
    username = db.Column(db.String(150), nullable=False, unique=True)  # login name
    password = db.Column(db.String(150), nullable=False)  # plain password (for now)
    role = db.Column(db.String(50), nullable=False)  # admin or employee
