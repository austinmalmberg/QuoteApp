from datetime import datetime

from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_dt = db.Column(db.DateTime, default=datetime.utcnow())
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(20), default='user')

    # gas_price_per_gal
    # min_quote_price

    def __init__(self, email, password_hash, role=None):
        self.email = email
        self.password_hash = password_hash
        self.role = 'user' if role is None else role


# class Employee(db.Model):
#     id
#     name
#     hourly_wage
#
#     user_id
#     user
#
#
# class Vehicle(db.Model):
#     id
#     make_model
#     mpg
#
#     user_id
#     user
#
#
# class Quote(db.Model):
#     id
#     description
#     amount
#
#     user_id
#     user
