from app import db
import datetime
import enum

class ScreenType(enum.Enum):
    regular = 1
    three_dimensional = 2
    imax = 3


class Screen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.String(length=100))

    height = db.Column(db.Integer)
    width = db.Column(db.Integer)
    screen_type = db.Column(db.Enum(ScreenType))
    seats = db.relationship('Seat', backref='screen', lazy="dynamic")
    showings = db.relationship('Showing', backref="screen", lazy=True)

    @staticmethod
    def get_all():
        return Screen.query.all()

    @staticmethod
    def get_by_screen_id(id):
        return Screen.query.get(id)

    @staticmethod
    def new_screen(screen_name, height, width, screen_type, save=True):
        screen = Screen(screen_name=screen_name, height=height, width=width, screen_type=screen_type)
        if save is True:
            db.session.add(screen)
            db.session.commit()
        return screen
