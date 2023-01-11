from flask_wtf import FlaskForm
from wtforms import HiddenField, ValidationError
from wtforms.validators import DataRequired
from app import models


class AddToBasketForm(FlaskForm):
    showing_id = HiddenField(validators=[DataRequired()])
    seat_ids = HiddenField(validators=[DataRequired()])
    tickets = HiddenField(validators=[DataRequired()])

    def validate(self):

        showing = models.Showing.get_by_showing_id(self.showing_id.data)
        if not showing:
            raise ValidationError("Not a valid showing ID")

        seats = self.seat_ids.data.split(",")
        tickets = self.tickets.data.split(",")

        count = 0
        for ticket in tickets:
            count += int(ticket)

        if len(seats) != count:
            raise ValidationError("Different number of seats and tickets")

        for seat_id in seats:
            seat = models.Seat.get_by_seat_id(seat_id)

            if not seat:
                raise ValidationError("Not a valid seat ID")

            if seat.screen_id is not showing.screen_id:
                raise ValidationError("Seat is not in screen for showing")

        if len(tickets) != len(models.TicketType):
            raise ValidationError("Ticket types are not valid")

        return True
