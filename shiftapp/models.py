from shiftapp import db
from flask_login import UserMixin

# user model for database and login system
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # unique user ID
    username = db.Column(db.String(150), nullable=False, unique=True)  # login name
    password = db.Column(db.String(150), nullable=False)  # plain password (for now)
    role = db.Column(db.String(50), nullable=False)  # admin or employee

# shift model for employee shift
class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    startTime = db.Column(db.String(10), nullable=False)
    endTime = db.Column(db.String(10), nullable=False)
    assignedTo = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref='shifts')
