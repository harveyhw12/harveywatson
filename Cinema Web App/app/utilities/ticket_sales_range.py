from app import models
from sqlalchemy import and_
import datetime


def ticket_sales_range(movie_ids, start_date, end_date):

    movie_tickets = {}
    for movie_id in movie_ids:
        movie_tickets[movie_id] = []

    number_days = (end_date - start_date).days
    # initialise at start date
    current_day = start_date
    dates = []
    # iterate through days in the range
    for i in range(number_days):
        timestamp = current_day.replace(tzinfo=datetime.timezone.utc).timestamp()
        dates.append(timestamp)

        # for each movie, count the number of ticket sales on this day
        for movie in movie_ids:
            # initialise the current day with 0 ticket sales
            movie_tickets[movie].append(0)

            # get all showings of this movie within the date range

            showings = models.Showing.query.filter(and_(models.Showing.movie_id == movie,
                                                        models.Showing.time >= current_day,
                                                        models.Showing.time <= current_day +
                                                        datetime.timedelta(hours=23, minutes=59))).all()
            # for each valid showing
            for showing in showings:
                # for each reservation to this showing
                reservations = showing.reservations
                # for each reservation
                for reservation in reservations:
                    # update the count of tickets for the current day with the number in this reservation
                    movie_tickets[movie][-1] += len(reservation.tickets)


        # add 1 to the current day
        current_day += datetime.timedelta(days=1)

    movie_tickets_output = {}
    for movie in movie_tickets:
        title = models.Movie.get_movie_title_by_id(movie)
        if title != -1:
            movie_tickets_output[models.Movie.get_movie_title_by_id(movie)] = movie_tickets[movie]

    return movie_tickets_output, dates


