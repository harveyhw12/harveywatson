from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms.validators import DataRequired


class RemoveFromBasketForm(FlaskForm):
    i = HiddenField(validators=[DataRequired()])

