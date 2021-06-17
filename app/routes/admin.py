import itertools

from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.exceptions import abort

from app.data_access.user import get_users, get_user_by_id, remove_user
from app.helpers.user_manager import role_required, Roles

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.get('/')
@role_required(Roles.ADMIN)
def index():
    users = get_users(order='role')

    return render_template(
        'admin.html',
        users=users
    )


@bp.post('/users/<int:id>/delete')
@role_required(Roles.ADMIN)
def delete_user(id):
    user = get_user_by_id(id)

    if user is None:
        abort(404)

    remove_user(user)
    flash('User deleted')

    return redirect(url_for('admin.index'))
