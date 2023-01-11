from app import db
from sqlalchemy import and_
import enum, datetime


class ShowingType(enum.Enum):
    regular = 1
    audio_descriptions = 2
    subtitles = 3


class Showing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    showing_type = db.Column(db.Enum(ShowingType))
    screen_id = db.Column(db.Integer, db.ForeignKey("screen.id"))
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    time = db.Column(db.DateTime)
    reservations = db.relationship('Reservation', backref='showing', lazy=True)

    # must be expressed in pennies not pounds otherwise floating point errors occur
    price = db.Column(db.Integer)

    @staticmethod
    def get_all():
        return Showing.query.all()

    @staticmethod
    def get_by_showing_id(id):
        return Showing.query.filter_by(id=id).first()

    @staticmethod
    def get_by_movie_id(movie_id, future=False):
        if future:
            return Showing.query.filter(and_(Showing.time > datetime.datetime.now(), Showing.movie_id == movie_id)).all()
        else:
            return Showing.query.filter_by(movie_id=movie_id).all()

    @staticmethod
    def new_showing(screen_id, showing_type, movie_id, time, price, save=True):
        showing = Showing(screen_id=screen_id, movie_id=movie_id, time=time, price=price, showing_type=showing_type)
        if save is True:
            db.session.add(showing)
            db.session.commit()
        return showing

    # returns True if showings exist in the future; False otherwise
    @staticmethod
    def check_future_showings_exist(movie_id):
        if len(Showing.get_by_movie_id(movie_id, future=True)) > 0:
            return True
        return False
