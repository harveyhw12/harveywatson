from app import models


def get_seat_multiplier(seat):
    if isinstance(seat, models.SeatType):
        seat_type = seat
    else:
        seat_type = seat.seat_type
    # regular
    if seat_type == models.SeatType.regular:
        return 1.0
    # vip
    elif seat_type == models.SeatType.vip:
        return 2.0
    # low visibility
    elif seat_type == models.SeatType.low_visibility:
        return 0.7
    # disabled
    elif seat_type == models.SeatType.disabled:
        return 0.9
    # error
    else:
        return 0.0


def get_ticket_multiplier(ticket):
    if isinstance(ticket, models.TicketType):
        ticket_type = ticket
    else:
        ticket_type = ticket.ticket_type
    # standard
    if ticket_type == models.TicketType.regular:
        return 1.0
    # student
    elif ticket_type == models.TicketType.student:
        return 0.75
    # senior
    elif ticket_type == models.TicketType.senior:
        return 0.6
    # children
    elif ticket_type == models.TicketType.child:
        return 0.5
    # error
    else:
        return 0.0


def get_ticket_cost(showing, ticket):
    seat = models.Seat.query.filter_by(id=ticket.seat_id).first()
    multiplier = get_seat_multiplier(seat) * get_ticket_multiplier(ticket)
    cost = int(round(showing.price * multiplier))
    return cost


def get_seat_cost(showing, seat, ticket):
    multiplier = get_seat_multiplier(seat) * get_ticket_multiplier(ticket)
    cost = int(round(showing.price * multiplier))
    return cost
