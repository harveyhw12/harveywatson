from app import db
import enum

class SeatType(enum.Enum):
    regular = 1
    vip = 2
    low_visibility = 3
    disabled = 4

class Seat(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    seat_type = db.Column(db.Enum(SeatType))
    screen_id = db.Column(db.Integer(), db.ForeignKey("screen.id"))
    row = db.Column(db.String(2))
    column = db.Column(db.Integer())
    tickets = db.relationship("Ticket", backref="seat", lazy=True)


    @staticmethod
    def get_all():
        return Seat.query.all()

    @staticmethod
    def get_by_screen_id(screen_id):
        return Seat.query.filter_by(screen_id=screen_id).all()

    @staticmethod
    def get_by_seat_id(seat_id):
        return Seat.query.filter_by(id=seat_id).first()

    @staticmethod
    def new_seat(seat_type, screen_id, row, column, save=True):
        seat = Seat(seat_type=seat_type, screen_id=screen_id, row=row, column=column)
        if save is True:
            db.session.add(seat)
            db.session.commit()
        return seat


