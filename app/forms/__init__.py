
from flask_wtf import FlaskForm
from wtforms.fields import DecimalField


class AppForm(FlaskForm):
    name = 'AppForm'
    button_text = 'Submit'

    def __init__(self, formdata, action=None, **kwargs):
        super(AppForm, self).__init__(formdata, **kwargs)

        if action:
            self.action = action


class CurrencyField(DecimalField):
    places = 2