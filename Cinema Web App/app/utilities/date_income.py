from app import models, utilities
from sqlalchemy import and_


# start and end must be formatted as a timedelta object before being passed in
def get_income_between_dates(start, end):
    if start > end:
        return -1
    income = 0
    transactions = models.Transaction.query.filter(and_(models.Transaction.date>=start, models.Transaction.date<=end)).all()
    for transaction in transactions:
        reservations = models.Reservation.get_by_transaction_id(transaction.id)
        for reservation in reservations:
            showing = models.Showing.query.filter_by(id = reservation.showing_id).first()
            tickets = models.Ticket.get_by_reservation_id(reservation.id)
            for ticket in tickets:
                ticket_cost = utilities.get_ticket_cost(showing, ticket)
                income += ticket_cost
    return income
