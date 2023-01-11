import os, tempfile, unittest, datetime, random
from app import app, db, utilities, models
from sqlalchemy import and_, or_
from dotenv import load_dotenv


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        app.config['TESTING'] = True
        app.config['WTF_CSRV_ENABLED'] = False
        app.config['DEBUG'] = False
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test_app.db')
        self.app = app.test_client()
        db.create_all()

        self.assertEqual(app.debug, False)

    def tearDown(self):
        db.drop_all()

    # # jake
    def test_get_seat_multiplier_1(self):

        utilities.populate_db()

        # give seat type 1
        seat = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=1, column=1, row=1, save=False)
        multiplier = utilities.get_seat_multiplier(seat)
        # ensure 1 is returned
        self.assertEqual(multiplier, 1.0)

    def test_get_seat_multiplier_2(self):
        utilities.populate_db()

        # give seat type 2
        seat = models.Seat.new_seat(seat_type=models.SeatType.vip, screen_id=1, row=1, column=1, save=False)
        multiplier = utilities.get_seat_multiplier(seat)
        # ensure 2 is returned
        self.assertEqual(multiplier, 2.0)

    def test_get_seat_multiplier_3(self):
        utilities.populate_db()

        # pass seat with type 3
        seat = models.Seat.new_seat(seat_type=models.SeatType.low_visibility, screen_id=1, row=1, column=1, save=False)
        multiplier = utilities.get_seat_multiplier(seat)
        # ensure 0.7 is returned
        self.assertEqual(multiplier, 0.7)

    def test_get_seat_multiplier_4(self):
        utilities.populate_db()
        # pass seat with type 4
        seat = models.Seat.new_seat(seat_type=models.SeatType.disabled, screen_id=1, row=1, column=1, save=False)
        multiplier = utilities.get_seat_multiplier(seat)
        # ensure 0.9 is returned
        self.assertEqual(multiplier, 0.9)

    def test_get_ticket_multiplier_1(self):
        utilities.populate_db()
        # pass ticket with type 1
        ticket = models.Ticket.new_ticket(seat_id=models.Seat.query.first().id,
                                          reservation_id=models.Reservation.query.first().id,
                                          ticket_type=models.TicketType.regular)
        multiplier = utilities.get_ticket_multiplier(ticket)
        # ensure 1.0 is returned
        self.assertEqual(multiplier, 1.0)

    def test_get_ticket_multiplier_2(self):
        utilities.populate_db()
        # pass ticket with type 2
        ticket = models.Ticket.new_ticket(seat_id=models.Seat.query.first().id,
                                          reservation_id=models.Reservation.query.first().id,
                                          ticket_type=models.TicketType.student)
        multiplier = utilities.get_ticket_multiplier(ticket)
        # ensure 0.75 is returned
        self.assertEqual(multiplier, 0.75)

    def test_get_ticket_multiplier_3(self):
        utilities.populate_db()
        # pass ticket with type 3
        ticket = models.Ticket.new_ticket(seat_id=models.Seat.query.first().id,
                                          reservation_id=models.Reservation.query.first().id,
                                          ticket_type=models.TicketType.senior)
        multiplier = utilities.get_ticket_multiplier(ticket)
        # ensure 0.6 is returned
        self.assertEqual(multiplier, 0.6)

    def test_get_ticket_multiplier_4(self):
        utilities.populate_db()
        # pass ticket with type 4
        ticket = models.Ticket.new_ticket(seat_id=models.Seat.query.first().id,
                                          reservation_id=models.Reservation.query.first().id,
                                          ticket_type=models.TicketType.child)
        multiplier = utilities.get_ticket_multiplier(ticket)
        # ensure 0.5 is returned
        self.assertEqual(multiplier, 0.5)

    def test_get_ticket_cost(self):
        utilities.populate_db()
        ticket_types = {
            models.TicketType.regular: 1.0,
            models.TicketType.student: 0.75,
            models.TicketType.senior: 0.6,
            models.TicketType.child: 0.5
        }
        seat_types = {
            models.SeatType.regular: 1.0,
            models.SeatType.vip: 2.0,
            models.SeatType.low_visibility: 0.7,
            models.SeatType.disabled: 0.9
        }
        # for each ticket multiplier
        for t_type in ticket_types:
            # for each seat multiplier
            for s_type in seat_types:
                ticket = models.Ticket.new_ticket(seat_id=models.Seat.query.filter_by(seat_type=s_type).first().id,
                                                  reservation_id=1, ticket_type=t_type)
                showing = models.Showing.query.first()
                # if result != ticket_multipliers[i-1] * seat_multipliers[i-1]
                calculated_cost = utilities.get_ticket_cost(showing, ticket)
                expected_cost = int(round(ticket_types[t_type] * seat_types[s_type] * showing.price))
                # if calculated_cost != expected_cost:
                #     # assert false
                #     self.assertEqual(1, 0, "The calculated ticket cost {0} is not equal to {1}".format(calculated_cost,
                #                                                                                        expected_cost), )
        self.assertEqual(calculated_cost, expected_cost)

    def test_get_total_income_initial(self):
        # populate_db to populate all tables
        # track the total income of the transactions as they're added
        # use get_total_income to check if total = amounts that went in

        # must be populated in this order due to table relationships
        # 0 foreign keys
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        # movie & screens foreign keys
        utilities.populate_showings(datetime.date(2021, 1, 1))
        # user foreign key
        utilities.populate_transaction(delta=10)
        # screens foreign key
        utilities.populate_seats()
        # showings and transactions foreign key
        utilities.populate_reservation()
        # seats and reservations
        expected_total_income = utilities.populate_tickets(getIncome=True)
        calculated_value = utilities.get_total_income(cumulative=True)[-1][1]

        self.assertEqual(expected_total_income, calculated_value)

    def test_get_total_income_new_transaction(self):
        # populate_db to populate all tables
        # track the total income of the transactions as they're added

        # must be populated in this order due to table relationships
        # 0 foreign keys
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        # movie & screens foreign keys
        utilities.populate_showings(datetime.date(2021, 1, 1))
        # user foreign key
        utilities.populate_transaction(delta=5)
        # screens foreign key
        utilities.populate_seats()
        # showings and transactions foreign key
        utilities.populate_reservation()
        # seats and reservations

        original_expected_total_income = utilities.populate_tickets(getIncome=True)
        calculated_value = utilities.get_total_income()

        transaction_date = datetime.date(2021, 1, 1) + datetime.timedelta(days=random.randint(1, 10))
        # add a new transaction
        transaction = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                         date=transaction_date, charge_id=1)
        # add a new reservation for this transaction
        showing = models.Showing.query.first()
        reservation = models.Reservation.new_reservation(showing_id=showing.id, transaction_id=transaction.id)

        # add a new ticket for  this reservation
        seat = models.Seat.query.first()
        ticket = models.Ticket.new_ticket(seat_id=seat.id, reservation_id=reservation.id,
                                          ticket_type=models.TicketType.regular)
        ticket_cost = utilities.get_ticket_cost(showing, ticket)
        # use get_total_income to check if new total = old_total + new transaction amount
        self.assertEqual(original_expected_total_income + ticket_cost, utilities.get_total_income(cumulative=True)[-1][1])

    def test_get_total_income_repeat(self):
        # populate database to populate all tables
        # track total income

        # must be populated in this order due to table relationships
        # 0 foreign keys
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        # movie & screens foreign keys
        utilities.populate_showings(datetime.date(2021, 1, 1))
        # user foreign key
        utilities.populate_transaction(delta=6)
        # screens foreign key
        utilities.populate_seats()
        # showings and transactions foreign key
        utilities.populate_reservation()
        # seats and reservations

        # use get_total income to compare to the amount inputted, store the returned value
        expected_total_income = utilities.populate_tickets(getIncome=True)
        calculated_value = utilities.get_total_income(cumulative=True)[-1][1]
        # run get_total_income again and compare to the result from the last call - if the values are different, assert false
        calculated_value2 = utilities.get_total_income(cumulative=True)[-1][1]
        self.assertTrue(expected_total_income == calculated_value and calculated_value2 == calculated_value)

    def test_get_weekly_income_initial(self):
        # populate_db to populate all tables
        # track total income inserted for the week after a specific day
        # use get_weekly_income to track income after the specific day
        # compare values

        # populates the database
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        utilities.populate_showings(datetime.date(2021, 1, 1))
        utilities.populate_transaction(datetime.date(2021, 1, 1), 4)
        utilities.populate_seats()
        utilities.populate_reservation()
        utilities.populate_tickets()
        utilities.get_total_income()
        # 8th June 2021
        start_day = datetime.datetime(2021, 1, 1)
        weekly_income = utilities.get_weekly_income(start_day)

        self.assertTrue(sum(weekly_income) > 0)

    def test_get_weekly_income_new_transaction_mid(self):
        # new transaction at some point during the week on one day and check total is correct
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        utilities.populate_showings(datetime.date(2021, 1, 1))
        utilities.populate_transaction(datetime.date(2021, 1, 1), 4)
        utilities.populate_seats()
        utilities.populate_reservation()
        utilities.populate_tickets()
        utilities.get_total_income()
        # 8th June 2021
        start_day = datetime.datetime(2021, 1, 1)
        weekly_income_before = utilities.get_weekly_income(start_day)
        transaction_date = datetime.datetime(2021, 1, 5)

        new_screen = models.Screen.new_screen(screen_name="10", width=10, height=10,
                                              screen_type=models.ScreenType.regular)
        new_showing = models.Showing.new_showing(screen_id=new_screen.id, movie_id=models.Movie.query.first().id,
                                                 time=datetime.datetime(year=2021, month=7, day=10), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_transaction = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=transaction_date, charge_id=1)
        new_reservation = models.Reservation.new_reservation(showing_id=new_showing.id,
                                                             transaction_id=new_transaction.id)
        seat1 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=2)
        seat2 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=3)
        new_ticket_1 = models.Ticket.new_ticket(seat_id=seat1.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        new_ticket_2 = models.Ticket.new_ticket(seat_id=seat2.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        price = utilities.get_transaction_income(new_transaction)

        weekly_income_after = utilities.get_weekly_income(start_day)

        self.assertTrue(weekly_income_before < weekly_income_after)

    def test_get_weekly_income_new_transaction_end(self):
        # new transaction at the end of the week (e.g. on the last day of that range)
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        utilities.populate_showings(datetime.date(2021, 1, 1))
        utilities.populate_transaction(datetime.date(2021, 1, 1), 4)
        utilities.populate_seats()
        utilities.populate_reservation()
        utilities.populate_tickets()
        utilities.get_total_income()
        # 8th June 2021
        start_day = datetime.datetime(2021, 1, 1)
        weekly_income_before = utilities.get_weekly_income(start_day)
        transaction_date = datetime.datetime(2021, 1, 7)

        new_screen = models.Screen.new_screen(screen_name="10", width=10, height=10,
                                              screen_type=models.ScreenType.regular)
        new_showing = models.Showing.new_showing(screen_id=new_screen.id, movie_id=models.Movie.query.first().id,
                                                 time=datetime.datetime(year=2021, month=7, day=10), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_transaction = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=transaction_date, charge_id=1)
        new_reservation = models.Reservation.new_reservation(showing_id=new_showing.id,
                                                             transaction_id=new_transaction.id)
        seat1 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=2)
        seat2 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=3)
        new_ticket_1 = models.Ticket.new_ticket(seat_id=seat1.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        new_ticket_2 = models.Ticket.new_ticket(seat_id=seat2.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        price = utilities.get_transaction_income(new_transaction)

        weekly_income_after = utilities.get_weekly_income(start_day)
        self.assertTrue(weekly_income_before < weekly_income_after)

    def test_get_weekly_income_new_transaction_before(self):
        # new transaction outside the week range (before the day)
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        utilities.populate_showings(datetime.date(2021, 1, 1))
        utilities.populate_transaction(datetime.date(2021, 1, 1), 4)
        utilities.populate_seats()
        utilities.populate_reservation()
        utilities.populate_tickets()
        utilities.get_total_income()
        # 8th June 2021
        start_day = datetime.datetime(2021, 1, 1)
        weekly_income_before = utilities.get_weekly_income(start_day)
        transaction_date = datetime.datetime(2020, 1, 15)

        new_screen = models.Screen.new_screen(screen_name="10", width=10, height=10,
                                              screen_type=models.ScreenType.regular)
        new_showing = models.Showing.new_showing(screen_id=new_screen.id, movie_id=models.Movie.query.first().id,
                                                 time=datetime.datetime(year=2021, month=7, day=10), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_transaction = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=transaction_date, charge_id=1)
        new_reservation = models.Reservation.new_reservation(showing_id=new_showing.id,
                                                             transaction_id=new_transaction.id)
        seat1 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=2)
        seat2 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=3)
        new_ticket_1 = models.Ticket.new_ticket(seat_id=seat1.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        new_ticket_2 = models.Ticket.new_ticket(seat_id=seat2.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)

        weekly_income_after = utilities.get_weekly_income(start_day)

        self.assertTrue(weekly_income_before == weekly_income_after)

    def test_get_weekly_income_new_transaction_after(self):
        # new transaction outside the week range (after the day + 7 days)
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        utilities.populate_showings(datetime.date(2021, 1, 1))
        utilities.populate_transaction(datetime.date(2021, 1, 1), 4)
        utilities.populate_seats()
        utilities.populate_reservation()
        utilities.populate_tickets()
        utilities.get_total_income()
        # 8th June 2021
        start_day = datetime.datetime(2021, 1, 1)
        weekly_income_before = utilities.get_weekly_income(start_day)
        transaction_date = datetime.datetime(2021, 1, 15)

        new_screen = models.Screen.new_screen(screen_name="10", width=10, height=10,
                                              screen_type=models.ScreenType.regular)
        new_showing = models.Showing.new_showing(screen_id=new_screen.id, movie_id=models.Movie.query.first().id,
                                                 time=datetime.datetime(year=2021, month=7, day=10), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_transaction = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=transaction_date, charge_id=1)
        new_reservation = models.Reservation.new_reservation(showing_id=new_showing.id,
                                                             transaction_id=new_transaction.id)
        seat1 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=2)
        seat2 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=3)
        new_ticket_1 = models.Ticket.new_ticket(seat_id=seat1.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        new_ticket_2 = models.Ticket.new_ticket(seat_id=seat2.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)

        weekly_income_after = utilities.get_weekly_income(start_day)

        self.assertTrue(weekly_income_before == weekly_income_after)

    # harvey
    def test_get_income_between_dates_same_day(self):
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        utilities.populate_showings(datetime.date(2021, 1, 1))
        utilities.populate_transaction(datetime.date(2021, 1, 1), 1)
        utilities.populate_seats()
        utilities.populate_reservation()
        utilities.populate_tickets()
        utilities.get_total_income()
        expected_income = 0
        transactions = models.Transaction.query.filter_by(date=datetime.datetime(year=2021, month=1, day=2)).all()
        for i in transactions:
            reservations = models.Reservation.query.filter_by(transaction_id=i.id).all()
            for j in reservations:
                showing = models.Showing.query.filter_by(id=j.showing_id).first()
                tickets = models.Ticket.query.filter_by(reservation_id=j.id).all()
                for q in tickets:
                    step_income = utilities.get_ticket_cost(showing, q)
                    expected_income += step_income

        new_screen = models.Screen.new_screen(screen_name="10", width=10, height=10,
                                              screen_type=models.ScreenType.regular)
        new_showing = models.Showing.new_showing(screen_id=new_screen.id, movie_id=models.Movie.query.first().id,
                                                 time=datetime.datetime(year=2021, month=1, day=3), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_transaction = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=datetime.datetime(2021, 1, 2), charge_id=1)
        new_reservation = models.Reservation.new_reservation(showing_id=new_showing.id,
                                                             transaction_id=new_transaction.id)
        seat1 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=2)
        seat2 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=3)
        new_ticket_1 = models.Ticket.new_ticket(seat_id=seat1.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        new_ticket_2 = models.Ticket.new_ticket(seat_id=seat2.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        price = utilities.get_transaction_income(new_transaction)
        expected_income += price
        calculated_income = utilities.get_income_between_dates(datetime.datetime(2021, 1, 2),
                                                               datetime.datetime(2021, 1, 2))
        self.assertEqual(expected_income, calculated_income)
        # ensures only income is returned from the exact day

    def test_get_income_between_dates_invalid(self):
        self.assertEqual(-1, utilities.get_income_between_dates(datetime.date(year=2021, month=1, day=12),
                                                                datetime.date(year=2020, month=1, day=12)))

    def test_get_income_between_dates_mid(self):
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        utilities.populate_showings(datetime.date(2021, 1, 1))
        utilities.populate_transaction(datetime.date(2021, 1, 1), 20)
        utilities.populate_seats()
        utilities.populate_reservation()
        utilities.populate_tickets()
        utilities.get_total_income()
        expected_income = 0
        transactions = models.Transaction.query.filter(
            and_(models.Transaction.date >= datetime.datetime(year=2021, month=1, day=2),
                 models.Transaction.date <= datetime.datetime(year=2021, month=1, day=5))).all()
        for i in transactions:
            reservations = models.Reservation.query.filter_by(transaction_id=i.id).all()
            for j in reservations:
                showing = models.Showing.query.filter_by(id=j.showing_id).first()
                tickets = models.Ticket.query.filter_by(reservation_id=j.id).all()
                for q in tickets:
                    expected_income += utilities.get_ticket_cost(showing, q)
        new_screen = models.Screen.new_screen(screen_name="10", width=10, height=10,
                                              screen_type=models.ScreenType.regular)
        new_showing = models.Showing.new_showing(screen_id=new_screen.id, movie_id=models.Movie.query.first().id,
                                                 time=datetime.datetime(year=2021, month=1, day=3), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_transaction = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=datetime.datetime(2021, 1, 4), charge_id=1)
        new_reservation = models.Reservation.new_reservation(showing_id=new_showing.id,
                                                             transaction_id=new_transaction.id)
        seat1 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=2)
        seat2 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=3)
        new_ticket_1 = models.Ticket.new_ticket(seat_id=seat1.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        new_ticket_2 = models.Ticket.new_ticket(seat_id=seat2.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        price = utilities.get_transaction_income(new_transaction)
        expected_income += price
        calculated_income = utilities.get_income_between_dates(datetime.datetime(2021, 1, 2),
                                                               datetime.datetime(2021, 1, 5))
        self.assertEqual(expected_income, calculated_income)
        # new transaction at some point during the dates and check new total is correct

    def test_get_income_between_dates_end(self):
        # new transaction on the final date, ensure the total updates
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        utilities.populate_showings(datetime.date(2021, 1, 1))
        utilities.populate_transaction(datetime.date(2021, 1, 1), 5)
        utilities.populate_seats()
        utilities.populate_reservation()
        utilities.populate_tickets()
        utilities.get_total_income()
        expected_income = 0
        transactions = models.Transaction.query.filter(
            and_(models.Transaction.date >= datetime.datetime(year=2021, month=1, day=2),
                 models.Transaction.date <= datetime.datetime(year=2021, month=1, day=5))).all()
        for i in transactions:
            reservations = models.Reservation.query.filter_by(transaction_id=i.id).all()
            for j in reservations:
                showing = models.Showing.query.filter_by(id=j.showing_id).first()
                tickets = models.Ticket.query.filter_by(reservation_id=j.id).all()
                for q in tickets:
                    temp = utilities.get_ticket_cost(showing, q)
                    expected_income += temp

        new_screen = models.Screen.new_screen(screen_name="10", width=10, height=10,
                                              screen_type=models.ScreenType.regular)
        new_showing = models.Showing.new_showing(screen_id=new_screen.id, movie_id=models.Movie.query.first().id,
                                                 time=datetime.datetime(year=2021, month=1, day=3), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_transaction = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=datetime.datetime(2021, 1, 5), charge_id=1)
        new_reservation = models.Reservation.new_reservation(showing_id=new_showing.id,
                                                             transaction_id=new_transaction.id)
        seat1 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=2)
        seat2 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=3)
        new_ticket_1 = models.Ticket.new_ticket(seat_id=seat1.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        new_ticket_2 = models.Ticket.new_ticket(seat_id=seat2.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        price = utilities.get_transaction_income(new_transaction)
        expected_income += price
        calculated_income = utilities.get_income_between_dates(datetime.datetime(2021, 1, 2),
                                                               datetime.datetime(2021, 1, 5))
        self.assertEqual(expected_income, calculated_income)

    def test_get_income_between_dates_before(self):
        # new transaction before the earlier date, ensure the total doesn't change
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        utilities.populate_showings(datetime.date(2021, 1, 1))
        utilities.populate_transaction(datetime.date(2021, 1, 1), 5)
        utilities.populate_seats()
        utilities.populate_reservation()
        utilities.populate_tickets()
        utilities.get_total_income()
        expected_income = 0
        transactions = models.Transaction.query.filter(
            and_(models.Transaction.date >= datetime.datetime(year=2021, month=1, day=2),
                 models.Transaction.date <= datetime.datetime(year=2021, month=1, day=5))).all()
        for i in transactions:
            reservations = models.Reservation.query.filter_by(transaction_id=i.id).all()
            for j in reservations:
                showing = models.Showing.query.filter_by(id=j.showing_id).first()
                tickets = models.Ticket.query.filter_by(reservation_id=j.id).all()
                for q in tickets:
                    expected_income += utilities.get_ticket_cost(showing, q)

        new_screen = models.Screen.new_screen(screen_name="10", width=10, height=10,
                                              screen_type=models.ScreenType.regular)
        new_showing = models.Showing.new_showing(screen_id=new_screen.id, movie_id=models.Movie.query.first().id,
                                                 time=datetime.datetime(year=2021, month=1, day=3), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_transaction = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=datetime.datetime(2020, 1, 5), charge_id=1)
        new_reservation = models.Reservation.new_reservation(showing_id=new_showing.id,
                                                             transaction_id=new_transaction.id)
        seat1 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=2)
        seat2 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=3)
        new_ticket_1 = models.Ticket.new_ticket(seat_id=seat1.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        new_ticket_2 = models.Ticket.new_ticket(seat_id=seat2.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        calculated_income = utilities.get_income_between_dates(datetime.datetime(2021, 1, 2),
                                                               datetime.datetime(2021, 1, 5))
        self.assertEqual(expected_income, calculated_income)

    def test_get_income_between_dates_after(self):
        # new transaction after  the later date, ensure the total doesn't change
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        utilities.populate_showings(datetime.date(2021, 1, 1))
        utilities.populate_transaction(datetime.date(2021, 1, 1), 5)
        utilities.populate_seats()
        utilities.populate_reservation()
        utilities.populate_tickets()
        utilities.get_total_income()
        expected_income = 0
        transactions = models.Transaction.query.filter(
            and_(models.Transaction.date >= datetime.datetime(year=2021, month=1, day=2),
                 models.Transaction.date <= datetime.datetime(year=2021, month=1, day=5))).all()
        for i in transactions:
            reservations = models.Reservation.query.filter_by(transaction_id=i.id).all()
            for j in reservations:
                showing = models.Showing.query.filter_by(id=j.showing_id).first()
                tickets = models.Ticket.query.filter_by(reservation_id=j.id).all()
                for q in tickets:
                    expected_income += utilities.get_ticket_cost(showing, q)

        new_screen = models.Screen.new_screen(screen_name="10", width=10, height=10,
                                              screen_type=models.ScreenType.regular)
        new_showing = models.Showing.new_showing(screen_id=new_screen.id, movie_id=models.Movie.query.first().id,
                                                 time=datetime.datetime(year=2021, month=1, day=3), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_transaction = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=datetime.datetime(2022, 1, 5), charge_id=1)
        new_reservation = models.Reservation.new_reservation(showing_id=new_showing.id,
                                                             transaction_id=new_transaction.id)
        seat1 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=2)
        seat2 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=new_screen.id, row=1, column=3)
        new_ticket_1 = models.Ticket.new_ticket(seat_id=seat1.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        new_ticket_2 = models.Ticket.new_ticket(seat_id=seat2.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        calculated_income = utilities.get_income_between_dates(datetime.datetime(2021, 1, 2),
                                                               datetime.datetime(2021, 1, 5))
        self.assertEqual(expected_income, calculated_income)
        pass

    def test_compare_movies_within(self):
        # pick the date bounds and
        start = datetime.datetime(year=2021, month=1, day=1)
        # populate database, count the number of tickets in range on insertion
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        # movie & screens foreign keys
        utilities.populate_showings(datetime.date(2021, 1, 1))
        # user foreign key
        utilities.populate_transaction()
        # screens foreign key
        utilities.populate_seats()
        utilities.populate_reservation()
        # showings and transactions foreign key
        movies = utilities.populate_tickets(getTotalTickets=True)
        result = utilities.ticket_sales_range(list(movies.keys()), start, start+datetime.timedelta(days=7))
        difference = utilities.populate_tickets(getTotalTickets=True, startDate=start, endDate=start+datetime.timedelta(days=7))

        result2 = utilities.ticket_sales_range(list(movies.keys()), start, start+datetime.timedelta(days=7))
        self.assertNotEqual(result, result2)

    def test_compare_movies_outside(self):
        # count number within range, add new ticket outside this range and check nothing changes
        # pick the date bounds and
        start = datetime.datetime(year=2021, month=1, day=1)
        # populate database, count the number of tickets in range on insertion
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        # movie & screens foreign keys
        utilities.populate_showings(datetime.date(2021, 1, 1))
        # user foreign key
        utilities.populate_transaction()
        # screens foreign key
        utilities.populate_seats()
        utilities.populate_reservation()
        # showings and transactions foreign key

        # create tickets between 1/1/2021 and 1/10/2021
        # movies is the tickets sold in this window
        movies = utilities.populate_tickets(getTotalTickets=True, startDate=start, endDate=start+datetime.timedelta(days=1))
        result = utilities.ticket_sales_range(list(movies.keys()), start, start+datetime.timedelta(days=1))

        # now add a new ticket sale to a showing outside this range
        new_showing = models.Showing.new_showing(screen_id=
                      models.Screen.query.first().id, movie_id=models.Movie.query.first().id,
                                                 time=datetime.datetime(year=2021, month=1, day=3), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_transaction = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=datetime.datetime(2022, 1, 5), charge_id=1)
        new_reservation = models.Reservation.new_reservation(showing_id=new_showing.id,
                                                             transaction_id=new_transaction.id)
        seat1 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=models.Screen.query.first().id, row=1, column=2)
        new_ticket_1 = models.Ticket.new_ticket(seat_id=seat1.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)

        # run the query for a second time - it should be the same as query1
        result2 = utilities.ticket_sales_range(list(movies.keys()), start, start+datetime.timedelta(days=1))
        self.assertEqual(result, result2)

    def test_get_movie_income_none(self):
        result = utilities.get_movie_income(None, cumulative=True)
        self.assertEqual(result[-1][1], 0)

    def test_get_movie_income(self):
        utilities.populate_movies_from_tmdb()
        movie = models.Movie.query.first()

        result = utilities.get_movie_income(movie.id, cumulative=True)
        self.assertEqual(result[-1][1], 0)

    def test_populate_movies(self):
        utilities.populate_screen()
        utilities.populate_movies_from_tmdb()
        utilities.populate_showings(datetime.datetime.now())
        showings = models.Showing.query.all()
        self.assertTrue(len(showings) > 0)

    def test_populate_movies_twice(self):
        utilities.populate_screen()
        utilities.populate_movies_from_tmdb()
        utilities.populate_showings(datetime.datetime.now())
        showings_before = models.Showing.query.all()
        utilities.populate_showings(datetime.datetime.now())
        showings_after = models.Showing.query.all()
        self.assertTrue(showings_before == showings_after)

    def test_get_transaction_price(self):
        utilities.populate_movies_from_tmdb()
        utilities.populate_screen()
        new_showing = models.Showing.new_showing(screen_id=
                      models.Screen.query.first().id, movie_id=models.Movie.query.first().id,
                                                 time=datetime.datetime(year=2021, month=1, day=3), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_transaction = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=datetime.datetime(2022, 1, 5), charge_id=1)
        new_reservation = models.Reservation.new_reservation(showing_id=new_showing.id,
                                                             transaction_id=new_transaction.id)
        seat1 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=models.Screen.query.first().id, row=1, column=2)
        new_ticket_1 = models.Ticket.new_ticket(seat_id=seat1.id, reservation_id=new_reservation.id,
                                                ticket_type=models.TicketType.regular)
        self.assertEqual(utilities.get_ticket_cost(new_showing,new_ticket_1), utilities.get_transaction_income(new_transaction))

    def test_get_weekly_income_per_movie(self):
        utilities.populate_movies_from_tmdb()
        utilities.populate_screen()
        movies = models.Movie.query.all()
        new_showing_1 = models.Showing.new_showing(screen_id=models.Screen.query.all()[0].id, movie_id=movies[0].id,
                                                 time=datetime.datetime(year=2021, month=1, day=3), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_showing_2 = models.Showing.new_showing(screen_id=models.Screen.query.all()[1].id, movie_id=movies[1].id,
                                                 time=datetime.datetime(year=2021, month=1, day=3), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_transaction_1 = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=datetime.datetime(2022, 1, 5), charge_id=1)
        new_transaction_2 = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=datetime.datetime(2022, 1, 5), charge_id=1)
        new_reservation_1 = models.Reservation.new_reservation(showing_id=new_showing_1.id,
                                                             transaction_id=new_transaction_1.id)
        new_reservation_2 = models.Reservation.new_reservation(showing_id=new_showing_2.id,
                                                             transaction_id=new_transaction_2.id)
        seat1 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=models.Screen.query.all()[0].id, row=1, column=2)
        seat2 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=models.Screen.query.all()[1].id, row=1, column=3)
        new_ticket_1 = models.Ticket.new_ticket(seat_id=seat1.id, reservation_id=new_reservation_1.id,
                                                ticket_type=models.TicketType.regular)
        new_ticket_2 = models.Ticket.new_ticket(seat_id=seat2.id, reservation_id=new_reservation_2.id,
                                                ticket_type=models.TicketType.regular)

        self.assertNotEqual(utilities.get_weekly_income_per_movie(movies[0].id, datetime.datetime(year=2021, month=1, day=3)), utilities.get_weekly_income_per_movie(movies[0].id, datetime.datetime(year=2021, month=1, day=3))+utilities.get_weekly_income_per_movie(movies[1].id, datetime.datetime(year=2021, month=1, day=3)))

    def test_get_all_weekly_incomes(self):
        utilities.populate_movies_from_tmdb()
        utilities.populate_screen()
        movies = models.Movie.query.all()
        new_showing_1 = models.Showing.new_showing(screen_id=models.Screen.query.all()[0].id, movie_id=movies[0].id,
                                                 time=datetime.datetime(year=2021, month=1, day=3), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_showing_2 = models.Showing.new_showing(screen_id=models.Screen.query.all()[1].id, movie_id=movies[1].id,
                                                 time=datetime.datetime(year=2021, month=1, day=3), price=600,
                                                 showing_type=models.ShowingType.regular)
        new_transaction_1 = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=datetime.datetime(2022, 1, 5), charge_id=1)
        new_transaction_2 = models.Transaction.new_transaction(user_id=1, payment_status=models.PaymentStatus.paid_card,
                                                             date=datetime.datetime(2022, 1, 5), charge_id=1)
        new_reservation_1 = models.Reservation.new_reservation(showing_id=new_showing_1.id,
                                                             transaction_id=new_transaction_1.id)
        new_reservation_2 = models.Reservation.new_reservation(showing_id=new_showing_2.id,
                                                             transaction_id=new_transaction_2.id)
        seat1 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=models.Screen.query.all()[0].id, row=1, column=2)
        seat2 = models.Seat.new_seat(seat_type=models.SeatType.regular, screen_id=models.Screen.query.all()[1].id, row=1, column=3)
        new_ticket_1 = models.Ticket.new_ticket(seat_id=seat1.id, reservation_id=new_reservation_1.id,
                                                ticket_type=models.TicketType.regular)
        new_ticket_2 = models.Ticket.new_ticket(seat_id=seat2.id, reservation_id=new_reservation_2.id,
                                                ticket_type=models.TicketType.regular)

        weekly_incomes = utilities.get_all_weekly_incomes(datetime.datetime(year=2021, month=1, day=3))

        self.assertTrue(len(weekly_incomes[0].keys()) == 2)

    def test_ticket_generation(self):

        # populate database, count the number of tickets in range on insertion
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        # movie & screens foreign keys
        utilities.populate_showing()
        # user foreign key
        utilities.populate_transaction()
        # screens foreign key
        utilities.populate_seats()
        utilities.populate_reservation()

        utilities.create_ticket("0","0","0","0","0","0","0","0","0","1234","0","0")

        with open("app/utilities/tickets/ticket.pdf",'rb') as file:
            self.assertTrue(os.path.getsize(file) > 0)

    def test_qr_generation(self):


        # populate database, count the number of tickets in range on insertion
        utilities.populate_movies()
        utilities.populate_users()
        utilities.populate_screen()
        # movie & screens foreign keys
        utilities.populate_showing()
        # user foreign key
        utilities.populate_transaction()
        # screens foreign key
        utilities.populate_seats()
        utilities.populate_reservation()

        utilities.create_ticket("0","0","0","0","0","0","0","0","0","1234","0","0")

        with open("app/utilities/tickets/qr.png",'rb') as file:
            self.assertTrue(os.path.getsize(file) > 0)


if __name__ == '__main__':
    unittest.main()
