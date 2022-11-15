from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    psw = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    address_line_1 = db.Column(db.String(255), nullable=False)
    address_line_2 = db.Column(db.String(255))
    town = db.Column(db.String(255))
    city = db.Column(db.String(255), nullable=False)
    postcode = db.Column(db.String(255), nullable=False)
    number1 = db.Column(db.integer, nullable=False)
    number2 = db.Column(db.String(14))
    occupation = db.Column(db.String(255))
    flyerId = db.Column(db.String(255))
    operatorId = db.Column(db.String(255))
    NAAID = db.Column(db.String(255))