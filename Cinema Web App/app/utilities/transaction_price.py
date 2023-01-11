from app import models
from .ticket_cost_calculator import get_ticket_cost


def get_transaction_income(transaction):
    income = 0
    reservations = models.Reservation.query.filter_by(transaction_id = transaction.id).all()
    for reservation in reservations:
        showing = models.Showing.get_by_showing_id(reservation.showing_id)
        tickets = models.Ticket.get_by_reservation_id(reservation.id)
        for ticket in tickets:
            ticket_cost = get_ticket_cost(showing, ticket)
            income += ticket_cost
    return income
