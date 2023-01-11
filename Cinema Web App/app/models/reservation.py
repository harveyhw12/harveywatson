from app import db


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    showing_id = db.Column(db.Integer, db.ForeignKey("showing.id"), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey("transaction.id"), nullable=False)
    tickets = db.relationship("Ticket", backref='reservation', lazy=True)

    @staticmethod
    def get_all():
        return Reservation.query.all()

    @staticmethod
    def get_by_showing_id(showing_id):
        return Reservation.query.filter_by(showing_id=showing_id).all()

    @staticmethod
    def get_by_transaction_id(transaction_id):
        return Reservation.query.filter_by(transaction_id=transaction_id).all()

    @staticmethod
    def new_reservation(showing_id, transaction_id, save=True):
        reservation = Reservation(showing_id=showing_id, transaction_id=transaction_id)
        if save is True:
            db.session.add(reservation)
            db.session.commit()
        return reservation
