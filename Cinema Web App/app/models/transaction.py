from app import db
import enum


class PaymentStatus(enum.Enum):
    paid_card = 1
    paid_cash = 2
    pending = 3
    declined = 4


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reservations = db.relationship("Reservation", backref="transaction", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime)
    payment_status = db.Column(db.Enum(PaymentStatus))
    charge_id = db.Column(db.String)

    @staticmethod
    def get_all():
        return Transaction.query.all()
  
    @staticmethod
    def get_by_user_id(user_id):
        return Transaction.query.filter_by(user_id= user_id).all()

    @staticmethod
    def get_by_payment_status(status):
        return Transaction.query.filter_by(payment_status=status).all()
        
    @staticmethod
    def new_transaction(user_id, payment_status, date, charge_id, save=True):
        transaction = Transaction(user_id=user_id, payment_status=payment_status, date=date, charge_id=charge_id)
        if save is True:
            db.session.add(transaction)
            db.session.commit()
        return transaction
