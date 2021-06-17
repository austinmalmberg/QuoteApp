
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user

from app.data_access.user import add_user, get_user_by_credentials, get_user_by_email
from app.forms.auth import RegistrationForm, LoginForm
from app.helpers.user_manager import get_unauthorized_redirect

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.email.data

        if get_user_by_email(email):
            flash('Email already registered')

        else:
            # create and login user
            user = add_user(email, form.password.data)
            login_user(user)

            return redirect(url_for('index'))

    return render_template('auth.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = get_user_by_credentials(form.email.data, form.password.data)

        if user is not None:
            login_user(user)

            # if the user was redirected to the login page (on account of @login_required),
            # we want to redirect the user back there
            redirect_path = get_unauthorized_redirect()

            return redirect(url_for('index') if redirect_path is None else redirect_path)

        flash('Invalid email or password')

    return render_template('auth.html', form=form)


@bp.get('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))
