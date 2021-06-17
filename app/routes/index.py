
from flask import Blueprint, render_template, request
from flask_login import login_required

from app.forms.quote import WorkForm

bp = Blueprint('main', __name__)

employees = [
    {
        'name': 'Austin Malmberg',
        'hourly_rate': 20.0
    },
    {
        'name': 'Annie Sorensen',
        'hourly_rate': 42.0
    },
    {
        'name': 'Carson King',
        'hourly_rate': 20.0
    },
]


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = WorkForm(request.form, action=request.path)

    return render_template('quote.html', form=form, employees=employees)


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')