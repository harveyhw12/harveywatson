from flask_mail import Message
from app import models, utilities
import datetime, locale


def generate_email(reservation):
    locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

    showing = models.Showing.query.filter_by(id=reservation.showing_id).first()
    transaction = models.Transaction.query.filter_by(id=reservation.transaction_id).first()
    user = models.User.query.filter_by(id=transaction.user_id).first()
    tickets = models.Ticket.query.filter_by(reservation_id=reservation.id).all()
    screen = models.Screen.query.filter_by(id=showing.screen_id).first()
    movie = models.Movie.query.filter_by(id=showing.movie_id).first()


    final_seat = ""
    final_cost = 0
    for i in tickets:
        seat = models.Seat.query.filter_by(id=i.seat_id).first()  # needs changing
        final_seat += seat.row + str(seat.column) + " "
        final_cost += utilities.get_ticket_cost(showing, i)

    final_name = user.first_name + ' ' + user.last_name

    users_email = user.email
    film_date = showing.time.strftime("%d/%m/%y")
    purchase_date = transaction.date.strftime("%d/%m/%y")
    film_name = models.Movie.query.filter_by(id=showing.movie_id).first().title
    film_time = showing.time.strftime("%H:%M")
    seat = final_seat
    screen = screen.screen_name
    name_of_user = final_name
    ticket_price = locale.currency(final_cost / 100, symbol=True, grouping=True)
    transaction_id = str(transaction.id)
    certificate = str(movie.certification)

    if (movie.is_adult):
        id_required = "Yes"
    else:
        id_required = "No"

    if transaction.payment_status.name != "paid_cash":
        payment_status = "Card"
    else:
        payment_status = "Cash"

    msg = Message("Tickets", sender='no-reply@dadpad.uk', recipients=[users_email])
    msg.body = """Dear {},\nYour order has been successful. Please find your tickets to {} attached.\nDon't forget\
 that admissions to age-restricted movies may require valid ID.\nWe hope you enjoy your movie and come again!\n
Dadpad Cinema""".format(name_of_user, film_name)
    ticket_args = [film_date, purchase_date, name_of_user, film_name, film_time, seat, screen, ticket_price, payment_status, transaction_id, id_required, certificate]
    utilities.create_ticket(ticket_args[0],ticket_args[1],ticket_args[2],ticket_args[3],ticket_args[4],ticket_args[5],ticket_args[6],ticket_args[7],ticket_args[8],ticket_args[9],ticket_args[10], ticket_args[11]);

    with open("app/utilities/tickets/ticket.pdf",'rb') as file:
        msg.attach(filename="ticket.pdf", disposition="attachment", content_type="application/pdf",data=file.read())
    return msg
