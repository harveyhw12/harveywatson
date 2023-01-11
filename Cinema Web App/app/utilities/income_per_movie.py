from app import models, utilities
import datetime
from sqlalchemy import and_


def get_movie_income(movie_id, cumulative=False):
    cinema_opening = datetime.datetime(year=2021, month=1, day=1)
    today = datetime.datetime.now()
    number_days = (today - cinema_opening).days

    incomes = []
    current_date = cinema_opening
    income = 0
    for i in range(number_days):
        current_date += datetime.timedelta(days=1)
        if not cumulative:
            income = 0
        # get each showing of the movie on this day
        showings = models.Showing.query.filter(and_(models.Showing.movie_id==movie_id, models.Showing.time >= current_date, models.Showing.time <= current_date + datetime.timedelta(days=1))).all()
        for showing in showings:
            # find each reservation for this showing
            reservations = models.Reservation.query.filter_by(showing_id=showing.id).all()
            for reservation in reservations:
                # get each ticket in the reservation
                tickets = models.Ticket.query.filter_by(reservation_id=reservation.id).all()
                for ticket in tickets:
                    # identify  the ticket cost and add to income
                    ticket_cost = utilities.get_ticket_cost(showing, ticket)
                    income += ticket_cost

        timestamp = current_date.replace(tzinfo=datetime.timezone.utc).timestamp()
        incomes.append((timestamp, income))

    return incomes
