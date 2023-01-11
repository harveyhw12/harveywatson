from app import models, utilities
import datetime
from sqlalchemy import and_
from operator import itemgetter


def get_carousel_movies():
    week_ago = datetime.datetime.today() - datetime.timedelta(days=7)
    # test_day = datetime.datetime(year=2021, month=3, day=21, hour=0, minute=0, second=0)
    movie_dic, _ = utilities.get_all_weekly_incomes(week_ago, use_active_movies=True)

    top_movies = []
    # for every movie and every day in a week this will take the movie and sum the money from each day.
    for movie, cash in movie_dic.items():
        top_movies.append((movie, sum(cash)))

    top_movies.sort(key=itemgetter(1))

    if len(top_movies) >= 3:
        return models.Movie.query.filter(
            and_(models.Movie.title.in_([top_movies[0][0], top_movies[1][0], top_movies[2][0]]),
                 models.Movie.active == True)).limit(3).all()
    else:
        return models.Movie.query.filter(models.Movie.active == True).limit(3).all()
