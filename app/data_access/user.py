from werkzeug.security import generate_password_hash, check_password_hash

from app.database import db
from app.database.models import User


def get_users(filters=None, order=None):
    query_result = User.query

    if filters:
        query_result = query_result.filter_by(**filters)

    if order == 'email':
        query_result = query_result.order_by(User.email)
    elif order == 'role':
        query_result = query_result.order_by(User.role)

    return query_result.all()


def get_user_by_id(id):
    return User.query.get(id)


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def add_user(email, password, **kwargs):
    password_hash = generate_password_hash(password)

    user = User(email, password_hash, **kwargs)

    db.session.add(user)

    db.session.flush()
    db.session.commit()

    return user


def remove_user(user):
    db.session.delete(user)
    db.session.commit()


def get_user_by_credentials(email, password):
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        return user

    return None
