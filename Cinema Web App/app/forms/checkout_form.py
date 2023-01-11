from flask_wtf import FlaskForm
from wtforms import HiddenField, ValidationError
from wtforms.validators import DataRequired, AnyOf


class CheckoutForm(FlaskForm):
    payment_type = HiddenField(validators=[DataRequired(), AnyOf(["cash", "card"])])
    stripe_token = HiddenField()

    def validate_stripe_token(self, token):
        if self.payment_type == "card" and (self.stripe_token is None or self.stripe_token == ""):
            raise ValidationError("Stripe Token is not defined")
