
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, Length, Email

from app.forms import AppForm

password_validators = [
    DataRequired(),
    Length(min=6, message='Password must be at least 6 characters')
]


class LoginForm(AppForm):
    name = 'Login'

    email = EmailField(
        'Email',
        validators=[
            Email(message='Invalid email address')
        ],
        description='someone@example.com'
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ],
        description='******'
    )


class RegistrationForm(LoginForm):
    name = 'Register'

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            *password_validators,
            EqualTo('password', message='Passwords do not match'),
        ],
        description='******'
    )
