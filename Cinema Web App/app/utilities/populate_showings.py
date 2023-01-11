import random
import datetime
from app import models
from sqlalchemy import and_


class Movie:
    movie = None;

    def __init__(self, movie):
        self.movie = movie


class Screen:
    id = None
    name = None
    time = datetime.time(hour=9)
    showings = []

    def __init__(self, id, name, time):
        self.time = time
        self.id = id
        self.name = name


class Showing:
    movie = None
    start = None
    end = None

    def __init__(self, movie, start, end):
        self.movie = movie
        self.start = start
        self.end = end


def schedule(screens, movies):
    j = 0
    for i in screens:
        random.shuffle(movies)
        i.showings = []
        start_time = i.time
        # while the time is between 9am and 1am
        while i.time < start_time + datetime.timedelta(hours=16):
            if j == len(movies):
                j = 0
                random.shuffle(movies)
            while j < len(movies):
                # if current time + length of film is beyond 1am, break
                if i.time+datetime.timedelta(minutes=movies[j].movie.runtime+60) > start_time + datetime.timedelta(hours=16):
                    # skip screen's time ahead to 1am
                    i.time = start_time + datetime.timedelta(hours=16)
                    break
                else:
                    # otherwise, append this showing to this screen's list of showings
                    # with movie length including 30 mins of ads
                    i.showings.append(Showing(movies[j], i.time, i.time+datetime.timedelta(minutes=movies[j].movie.runtime+30)))
                    # increase the screen's 'simulated' time and proceed to next movie,
                    # plus 60 mins to allow for cleaning after the previous movie
                    i.time += datetime.timedelta(minutes=movies[j].movie.runtime+60)
                    j += 1


def populate_showings(date_from, num_days=7):
    today = datetime.datetime(year=date_from.year, month=date_from.month, day=date_from.day, hour=9, minute=0, second=0)
    showings = models.Showing.query.filter(and_(models.Showing.time >= today, models.Showing.time <= today + datetime.timedelta(days=num_days))).all()
    if len(showings) > 0:
        return 0
    screens = models.Screen.query.all()
    movies = models.Movie.query.filter_by(active=True).all()
    movie_objs = []
    screen_objs = []
    # create a movie object for each movie found
    for i in movies:
        movie_objs.append(Movie(i))
    # create a screen object for each screen found
    for i in screens:
        screen_objs.append(Screen(i.id, i.screen_name, today))
    # schedule should populate the screens objects with an array of showings
    schedule(screen_objs, movie_objs)
    # commits the showings to the database
    for day in range(num_days):
        for screen in screen_objs:
            for showing in screen.showings:
                showing_type = random.choice(list(models.ShowingType) + [models.ShowingType.regular for x in range(4)])
                models.Showing.new_showing(screen_id=screen.id,
                                           showing_type=showing_type,
                                           movie_id=showing.movie.movie.id,
                                           time=showing.start+datetime.timedelta(days=day),
                                           price=1000)
    return 1
