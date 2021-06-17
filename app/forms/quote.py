
from wtforms.fields import DecimalField, TextAreaField

from app.forms import AppForm, CurrencyField


class WorkForm(AppForm):
    name = 'Work'
    button_text = 'Save Quote'

    description = TextAreaField(
        'Description'
    )

    hours = DecimalField(
        'Estimated Hours',
        description='Hours to complete the job',
        places=2,
        default=1.0
    )

    # manual OR sum of employee hourly_rate
    hourly_rate = CurrencyField(
        'Hourly Rate',
        description='Enter hourly rate or select from employees',
        default=0.0
    )

    # hours * sum_hourly_rate
    labor = CurrencyField(
        'Labor',
        default=0.0,
    )

    supplies = CurrencyField(
        'Parts/Supplies',
        default=0.0
    )

    misc = CurrencyField(
        'Misc',
        default=0.0
    )

    profit = CurrencyField(
        'Profit',
        default=0.0
    )

    profit_margin = DecimalField(
        'Profit Margin',
        description='Calculate profit based on the expenses amount',
        places=2,
        default=10.0,
    )

    estimate_minimum = CurrencyField(
        'Estimate Minimum',
        default=0.0
    )

    tax_rate = DecimalField(
        'Tax Rate',
        default=7.25
    )
