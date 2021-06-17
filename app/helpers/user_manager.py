from datetime import datetime, timedelta
import functools
import pytz

from flask import redirect, url_for, flash, request, session
from flask_login import LoginManager, login_required, current_user
from werkzeug.exceptions import abort

from app.data_access.user import get_user_by_id

login = LoginManager()

UNAUTHORIZED_REDIRECT_SESSION_VARIABLE = 'redirected_from'
UNAUTHORIZED_REDIRECT_TIMEOUT_MINUTES = 10


class Roles:
    ADMIN = 'admin'
    USER = 'user'


def init_app(app):
    login.init_app(app)


@login.user_loader
def load_user(id):
    return get_user_by_id(id)


@login.unauthorized_handler
def handle_unauthorized_user():
    if request.path.startswith('/api'):
        # abort API requests. This will be caught by the exception handler, which will return a JSON error
        abort(401)

    # set intended destination so that we can redirect the user there once logged in
    set_unauthorized_redirect(request.path)

    flash('You must be logged in to do that')

    return redirect(url_for('auth.login'))


def role_required(roles):
    """
    A decorator for limiting access to certain user by their role. Users with a role not in the list/set specified will
    encounter a 401 Unauthorized error.

    :param roles: a list or set of roles that can access the view
    :return: the decorated view
    """

    def decorated_view(view):

        @functools.wraps(view)
        @login_required
        def wrapped_view(*args, **kwargs):

            if (type(roles) is list or type(roles) is set) and current_user.role in roles or \
                    current_user.role == roles:
                return view(*args, **kwargs)

            abort(403)

        return wrapped_view

    return decorated_view


def set_unauthorized_redirect(path):
    session[UNAUTHORIZED_REDIRECT_SESSION_VARIABLE] = dict(
        path=path,
        attempt_dt=datetime.now(pytz.UTC)
    )


def get_unauthorized_redirect():
    if UNAUTHORIZED_REDIRECT_SESSION_VARIABLE not in session:
        return None

    redirect_info = session[UNAUTHORIZED_REDIRECT_SESSION_VARIABLE]
    session.pop(UNAUTHORIZED_REDIRECT_SESSION_VARIABLE, None)

    if datetime.now(pytz.UTC) <= redirect_info['attempt_dt'] + timedelta(minutes=UNAUTHORIZED_REDIRECT_TIMEOUT_MINUTES):
        return redirect_info['path']
