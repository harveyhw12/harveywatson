from app import db
import enum


class TicketType(enum.Enum):
    regular = 1
    student = 2
    senior = 3
    child = 4


class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    seat_id = db.Column(db.Integer, db.ForeignKey("seat.id"), nullable=False)
    reservation_id = db.Column(db.Integer, db.ForeignKey("reservation.id"), nullable=False)
    ticket_type = db.Column(db.Enum(TicketType))

    @staticmethod
    def get_all():
        return Ticket.query.all()

    @staticmethod
    def get_by_seat_id(seat_id):
        return Ticket.query.filter_by(seat_id= seat_id).all()

    @staticmethod
    def get_by_reservation_id(reservation_id):
        return Ticket.query.filter_by(reservation_id=reservation_id).all()

    @staticmethod
    def get_by_ticket_type(ticket_type):
        return Ticket.query.filter_by(ticket_type=ticket_type).all()

    @staticmethod
    def new_ticket(seat_id, reservation_id, ticket_type, save=True):
        ticket = Ticket(seat_id=seat_id, reservation_id=reservation_id, ticket_type=ticket_type)
        if save is True:
            db.session.add(ticket)
            db.session.commit()
        return ticket
