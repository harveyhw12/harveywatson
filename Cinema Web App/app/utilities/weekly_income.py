from app import models, utilities
import datetime
from sqlalchemy import and_


# day must be formatted as a timedelta object before being passed in
def get_weekly_income(day):
    weekly_income = []
    for i in range(7):
        delta = datetime.timedelta(days=i)
        current_day = day + delta
        income = 0
        transactions = models.Transaction.get_all()
        for transaction in transactions:
            reservations = models.Reservation.get_by_transaction_id(transaction.id)
            count = 0
            for reservation in reservations:
                showing = models.Showing.query.filter_by(id = reservation.showing_id).first()
                if transaction.date.day == current_day.day:
                    tickets = models.Ticket.get_by_reservation_id(reservation.id)
                    price = showing.price
                    for ticket in tickets:
                        ticket_cost = utilities.get_ticket_cost(showing, ticket)
                        income += ticket_cost
        weekly_income.append(income)

    return weekly_income


def get_weekly_income_per_movie(movie_id, day):
    current_date = day
    income_list = []
    for i in range(7):
        income = 0

        showings = models.Showing.query.filter(and_(models.Showing.movie_id==movie_id, models.Showing.time >= current_date, models.Showing.time <= current_date + datetime.timedelta(hours=23, minutes=59))).all()
        for showing in showings:
            reservations = models.Reservation.query.filter_by(showing_id=showing.id)
            for reservation in reservations:
                tickets = models.Ticket.query.filter_by(reservation_id=reservation.id)
                for ticket in tickets:
                    cost = utilities.get_ticket_cost(showing, ticket)
                    income += cost

        income_list.append(income)

        current_date += datetime.timedelta(days=1)

    return income_list


def get_all_weekly_incomes(day, use_id=False, use_active_movies=False):
    week_incomes = {}
    end_date = day + datetime.timedelta(days=7)
    # query all movies that have showings in this week
    showings = models.Showing.query.filter(and_(models.Showing.time >= day, models.Showing.time <= end_date)).all()
    # get dictionary keys
    for showing in showings:
        key = showing.movie.id if use_id else showing.movie.title
        # if the key isn't already in the dictionary add it
        # if only using active movies, only add the movie if it's active
        # if not using active movies, then carry on
        if key not in week_incomes and ((use_active_movies and showing.movie.active) or not use_active_movies):
            week_incomes[key] = get_weekly_income_per_movie(showing.movie_id, day)

    dates = []
    current_date = day - datetime.timedelta(days=1)
    for i in range(7):
        current_date += datetime.timedelta(days=1)
        timestamp = current_date.replace(tzinfo=datetime.timezone.utc).timestamp()
        dates.append(timestamp)

    return week_incomes, dates
