
from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from app.data_access.user import get_users
from app.dto.user import UserDto
from app.helpers.user_manager import role_required, Roles

bp = Blueprint('users', __name__, url_prefix='/user')


@bp.get('/')
@login_required
def get_user():
    user_dto = UserDto(current_user)

    return jsonify(user_dto)


@bp.get('/all')
@role_required(Roles.ADMIN)
def all_users():
    allusers_dto = [UserDto(user) for user in get_users()]

    return jsonify(allusers_dto)