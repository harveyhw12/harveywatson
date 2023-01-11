from app import models, db, utilities, user_datastore, app
from time import sleep
import random, string, unittest, requests
from sqlalchemy import and_
import datetime
import math
import click

live_num_screens = 10
seats_per_screen = [x ** 2 for x in range(8, 17) for f in (1, 2)]
min_seats_per_row = 10
max_seats_per_row = 2 * min_seats_per_row
default_num_movies = 10

test_num_movies = 25
test_num_users = 25
test_num_screens = 5
test_num_seats = 500
test_num_reservations = 400
test_num_showings = 300
test_num_tickets = 2000
test_num_transactions = 300

TMDB_API_KEY = "61ef4fbecf526fda5a8e8dc72bbc92b9"


# populates movies model using TMDB api
def populate_movies_from_tmdb():
    response = requests.get(
        "https://api.themoviedb.org/3/movie/popular?api_key={}&language=en&region=GB".format(TMDB_API_KEY))
    results = response.json()["results"]
    for movie_listing in results[:default_num_movies]:
        populate_movie(movie_listing["id"])
    db.session.commit()


def populate_movie(tmdb_id, returns=False):

    movies = models.Movie.query.filter_by(id=tmdb_id).all()
    # checks if the movie is already in the database
    if len(movies) == 1 and returns is False:
        movies[0].active = True
        db.session.commit()
        return

    # otherwise, queries TMDB API
    movie_info = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en&region=GB".format(tmdb_id,
                                                                                        TMDB_API_KEY)).json()
    keywords = requests.get("https://api.themoviedb.org/3/movie/{}/keywords?api_key={}".format(tmdb_id,
                                                                                               TMDB_API_KEY)).json()
    credits = requests.get(
        "https://api.themoviedb.org/3/movie/{}/credits?api_key={}".format(tmdb_id, TMDB_API_KEY)).json()
    release_dates = requests.get(
        "https://api.themoviedb.org/3/movie/{}/release_dates?api_key={}".format(tmdb_id,
                                                                                TMDB_API_KEY)).json()
    # movie = models.Movie.query.filter_by(tmdb_id=tmdb_id).first()

    # if not movie:
    movie = models.Movie(tmdb_id=tmdb_id)

    movie.title = movie_info["title"]
    movie.tagline = movie_info["tagline"]
    movie.overview = movie_info["overview"]
    movie.runtime = movie_info["runtime"]
    movie.release_date = datetime.date.fromisoformat(movie_info["release_date"])
    movie.poster_url = "https://image.tmdb.org/t/p/w500{}".format(movie_info["poster_path"])
    movie.backdrop_url = "https://image.tmdb.org/t/p/w1280{}".format(movie_info["backdrop_path"])
    movie.vote_average = movie_info["vote_average"]
    movie.vote_count = movie_info["vote_count"]
    movie.is_adult = movie_info["adult"]
    movie.active = True
    try:
        movie.certification = \
        list(filter(lambda x: x['iso_3166_1'] == 'GB', release_dates['results']))[0]["release_dates"][0]["certification"]
    except:
        movie.certification = None
    if movie.certification == '':
        movie.certification = None
    movie.cast = list()
    for cast_member in credits['cast']:
        actor = models.CastMember.query.filter_by(tmdb_id=cast_member['id']).first()
        if not actor:
            actor = models.CastMember(tmdb_id=cast_member['id'])

        actor.name = cast_member['name']
        if cast_member["profile_path"] is not None:
            actor.profile_url = "https://image.tmdb.org/t/p/w185{}".format(
                cast_member["profile_path"])
        order = cast_member['order']
        # create many-to-many association between the movie and the cast member
        actor_movie_association = models.CastMovieAssociation(order=order)
        actor_movie_association.cast = actor
        movie.cast.append(actor_movie_association)

    movie.keywords = list()
    for keyword_info in keywords['keywords']:
        keyword = models.Keyword.query.filter_by(tmdb_id=keyword_info['id']).first()
        if not keyword:
            keyword = models.Keyword(tmdb_id=keyword_info['id'])

        keyword.name = keyword_info['name']

        movie.keywords.append(keyword)
    if returns is True:
        return movie
    db.session.add(movie)


def delete_movie(id):
    movies = models.Movie.query.all()
    for movie in movies:
        if int(movie.id) == int(id):
            movie.active = False


def delete_showing(id):
    showings = models.Showing.query.all()
    for showing in showings:
        if int(showing.id) == int(id):
            db.session.delete(showing)


# base tables
# hard-codes the screens model with a fixed number of screens and attributes
def create_screens_and_seats():
    for i in range(live_num_screens):
        size = int(math.sqrt(seats_per_screen[i]))

        # create new screen with the calculated height and width with a random screen type
        new_screen = models.Screen.new_screen(str(i+1), size, size, screen_type=random.choice(list(models.ScreenType)))

        seats = []
        # for each seat
        for j in range(seats_per_screen[i]):
            # add 1 to make column value 1-based
            column = j % size + 1
            row_num = math.ceil((j - j % size) / size)
            # add calculate number of rows, add 65 so row 0 is labelled A
            row = chr(row_num + 65)

            seat_type = models.SeatType.regular
            if column == 1 or column == size:
                seat_type = models.SeatType.low_visibility
                seats.append("L")
            # the row closest to the screen is disabled
            elif row == 'A':
                seat_type = models.SeatType.disabled
                seats.append("D")
            # the last two rows are VIP
            elif math.floor(size / 2) + 1 == row_num or math.floor(size / 2) == row_num:
                seat_type = models.SeatType.vip
                seats.append("V")
            else:
                seat_type == models.SeatType.regular
                seats.append("R")
            # this needs adjusting if there are more than 26 rows
            new_seat = models.Seat.new_seat(seat_type, new_screen.id, row, column)


# functions to populate tables for testing
def populate_movies():
    # create 50 movies
    for i in range(test_num_movies):
        tmdb_id = i
        # generates a random quantity of random lowercase ascii characters, such that the resultant string is between 5 and 20 chars
        title = ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(5, 20)))
        tagline = ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(5, 20)))
        overview = ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(5, 20)))
        runtime = random.randint(30, 300)
        release_date = datetime.date(1900, 1, 1) + datetime.timedelta(days=random.randint(1, 44223))
        backdrop_url = "https://r.sine.com/index"
        poster_url = "https://r.sine.com/index"
        active = True
        vote_average = round(random.uniform(0.0, 5.0), 2)
        vote_count = random.randint(0, 50000)
        is_adult = bool(random.getrandbits(1))
        movie = models.Movie.new_movie(tmdb_id=tmdb_id, title=title, tagline=tagline, overview=overview,
                                       runtime=runtime, release_date=release_date, backdrop_url=backdrop_url,
                                       poster_url=poster_url, vote_average=vote_average, vote_count=vote_count,
                                       is_adult=is_adult, active=True)


def populate_users():
    for i in range(test_num_users):
        email = ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(5, 10))) + "@" + ''.join(
            random.choice(string.ascii_lowercase) for i in range(random.randint(5, 10))) + ".com"
        password = ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(5, 20)))
        first_name = ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(5, 20)))
        last_name = ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(5, 20)))
        user = user_datastore.create_user(email=email, password=password, first_name=first_name, last_name=last_name)


def populate_screen():
    for i in range(live_num_screens):
        screen_name = ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(5, 20)))
        height = 5
        width = random.randint(0, 40)
        screen_type = random.choice(list(models.ScreenType))
        screen = models.Screen.new_screen(screen_name=screen_name, height=height, width=width, screen_type=screen_type)


def populate_seats():
    for i in range(test_num_seats):
        seat_type = random.choice(list(models.SeatType))
        screen_id = random.choice(models.Screen.get_all()).id
        row = ''.join(random.choice(string.ascii_lowercase) for i in range(2))
        column = random.randint(0, 40)
        # if a seat with this row and column already exists then retry this loop
        if (len(list(models.Seat.query.filter_by(screen_id=screen_id, row=row, column=column).all())) > 0):
            i -= 1
        else:
            seat = models.Seat.new_seat(seat_type=seat_type, screen_id=screen_id, row=row, column=column)


def populate_reservation():
    for i in range(300):
        showing_id = random.choice(models.Showing.get_all()).id
        transaction_id = random.choice(models.Transaction.get_all()).id
        reservation = models.Reservation.new_reservation(showing_id=showing_id, transaction_id=transaction_id)


def populate_random_showings():
    for i in range(test_num_showings):
        screen_id = random.choice(models.Screen.get_all()).id
        movie_id = random.choice(models.Movie.get_all()).id
        # possibly needs some validation to ensure no showings at the same screen overlap, needs some thought
        time = datetime.date(2021, 1, 1) + datetime.timedelta(days=random.randint(1, 60)) + datetime.timedelta(
            hours=random.randint(0, 23), minutes=random.randint(0, 59))
        price = random.randint(500, 1200)
        showing_type = random.choice(list(models.ShowingType))
        showing = models.Showing.new_showing(screen_id=screen_id, movie_id=movie_id, time=time, price=price,
                                             showing_type=showing_type)


def populate_tickets(getIncome=False, getTotalTickets=False, startDate=datetime.datetime(year=2021, month=1, day=1),
                     endDate=datetime.datetime(year=2021, month=5, day=1)):
    # dictionary of movies and movie ticket sales - only populated if getTotalTickets is true
    movies = {}
    # tickets to seats is one-to-one, so must ensure the seat hasn't already been used
    seats = []
    total_income = 0
    for i in range(test_num_tickets):
        seat_id = random.choice(models.Seat.get_all()).id
        if seat_id in seats:
            i -= 1
            continue
        else:
            seats.append(seat_id)
        reservation = random.choice(models.Reservation.get_all())
        reservation_id = reservation.id
        showing = models.Showing.query.filter_by(id=reservation.showing_id).first()
        if getTotalTickets is True and startDate <= showing.time and showing.time <= endDate:
            if showing.movie_id not in movies:
                movies[showing.movie_id] = 1
            else:
                movies[showing.movie_id] += 1
        ticket_type = random.choice(list(models.TicketType))
        ticket = models.Ticket.new_ticket(seat_id=seat_id, reservation_id=reservation_id, ticket_type=ticket_type)
        total_income += utilities.get_ticket_cost(showing, ticket)

    if getIncome is True:
        return total_income

    if getTotalTickets is True:
        return movies


def populate_transaction(start=datetime.datetime(year=2021, month=1, day=1)):
    num_days = (datetime.datetime.now() - start).days - 1
    for i in range(test_num_transactions):
        user_id = random.choice(models.User.get_all()).id
        payment_status = random.choice(list(models.PaymentStatus))
        time = start + datetime.timedelta(days=random.randint(1, num_days)) + datetime.timedelta(
            hours=random.randint(0, 23), minutes=random.randint(0, 59))
        transaction = models.Transaction.new_transaction(user_id=user_id, payment_status=payment_status, date=time, charge_id=i)


def populate_db():
    # must be populated in this order due to table relationships
    # 0 foreign keys
    populate_movies_from_tmdb()
    populate_users()
    populate_screen()
    # movie & screens foreign keys
    populate_random_showings()
    # user foreign key
    populate_transaction()
    # screens foreign key
    populate_seats()
    # showings and transactions foreign key
    populate_reservation()
    # seats and reservations
    populate_tickets()


@app.cli.command("populate")
@click.argument("method")
def populate(method):
    if method == "movies":
        print("Populating movies from TMDB")
        populate_movies_from_tmdb()
        print("Finished")
        return
    if method == "screens":
        print("Creating seats and screens")
        create_screens_and_seats()
        print("Finished")
        return
    if method == "roles":
        print("Allocating roles for customer, manager and staff")
        customer = user_datastore.find_or_create_role(name="customer",
                                                      description="Customer for the cinema, can book and view tickets")
        manager = user_datastore.find_or_create_role(name="manager",
                                                     description="Manager for the cinema, ability to view tickets")
        staff = user_datastore.find_or_create_role(name="staff", description="Staff for the cinema, can scan tickets")

        db.session.add(customer)
        db.session.add(manager)
        db.session.add(staff)
        db.session.commit()
        print("Finished")
        return
    if method == "transactions":
        print("Populating transactions")
        populate_transaction()
        print("Finished")
        return
    if method == "reservations":
        print("Populating reservations")
        populate_reservation()
        return
    if method == "showings-today":
        print("Populating showings")
        now = datetime.datetime.now().date()
        utilities.populate_showings(datetime.datetime(day=now.day, month=now.month, year=now.year,
                                                      hour=0, minute=0, second=0))
        return
    if method == "showings-historical":
        print("Populating showings from 01/01/2021")
        start = datetime.datetime(day=1, month=1, year=2021, hour=0, minute=0, second=0)
        num_days = (datetime.datetime.now() + datetime.timedelta(days=7) - start).days
        utilities.populate_showings(start, num_days)

        return
    if method == "tickets":
        print("Populating tickets")
        populate_tickets()
        return
    if method == "screens_and_seats":
        print("Populating screens and seats")
        create_screens_and_seats()
        return
    if method == "all":
        print("Populating every table with quality vegan data")
        populate_db()
        print("Finished")
        return
    print("Please input a schema to populate for (movies, screens, roles, all)")


def tmdb_movies(movie_name):
    if movie_name == "":
        return

    movie_for_page = []
    results = []
    movie_name = movie_name.split(" ")
    movie_string = ""
    for i in range(len(movie_name)):
        if i == len(movie_name)-1:
            movie_string += movie_name[i]
        else:
            print(movie_name[i])
            movie_string += movie_name[i]
            movie_string += "+"
    response = requests.get("https://api.themoviedb.org/3/search/movie?api_key={}&query={}".format(TMDB_API_KEY, movie_string))
    results = response.json()['results']
    movies_to_show = []
    for result in results:
        movies = models.Movie.query.all()
        for movie in movies:
            if result["id"] == movie.id:
                pass
            else:
                movies_to_show.append(result["id"])
                break;
    i=0
    for movie in movies_to_show:
        i+=1
        movie = utilities.populate_movie(result["id"], returns=True)
        movie_for_page.append(movie)
    return movie_for_page
