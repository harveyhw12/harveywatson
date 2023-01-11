from flask_security.forms import RegisterForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, EqualTo


class ExtendedRegisterForm(RegisterForm):
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
