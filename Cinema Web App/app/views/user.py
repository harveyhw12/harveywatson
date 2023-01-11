from flask_security import login_required, current_user, roles_accepted
from flask import render_template, redirect, url_for, flash, request, jsonify, send_from_directory
from app import app, db, user_datastore, forms, utilities, models
from flask_security.signals import user_registered
from flask_security.utils import hash_password, verify_password
import datetime, os, stripe, time, locale
from flask_mail import Mail

stripe.api_key = os.environ["STRIPE_SECRET_KEY"] if "STRIPE_SECRET_KEY" in os.environ else ""

@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    default_role = user_datastore.find_role("customer")
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()


@app.route('/account')
@login_required
def account_page():
    return render_template('pages/account.html')


@app.route('/checkout', methods=["GET", "POST"])
@login_required
@roles_accepted('customer', 'staff', 'manager')
def checkout_page():
    basket = utilities.get_basket(True)

    form = forms.CheckoutForm()
    basket_description = ""
    total = 0
    for item in basket:
        num_tickets = 0
        for ticket in item.tickets:
            num_tickets += item.tickets[ticket]
        basket_description += str(num_tickets) + "x " + models.Movie.get_by_movie_id(item.showing.movie_id).title + ", "
        total += item.price
    basket_description = basket_description[:-2]

    if form.validate_on_submit() and request.method == "POST":
        for i, item in enumerate(basket):
            reservations = models.Reservation.get_by_showing_id(item.showing.id)
            for reservation in reservations:
                tickets = models.Ticket.get_by_reservation_id(reservation.id)
                for ticket in tickets:
                    if ticket.seat_id in list(map(lambda x: x.id, item.seats)):
                        flash("Seat has already been taken")
                        utilities.remove_from_basket(i)
                        return redirect(url_for("basket_page"))

        if form.payment_type.data == "card":
            customer = stripe.Customer.create(
                email=current_user.email,
                source=form.stripe_token.data,
            )

            charge = stripe.Charge.create(
                customer=customer.id,
                amount=total,
                currency='gbp',
                description="Dadpad Cinema tickets: " + basket_description
            )
            transaction = models.Transaction.new_transaction(user_id=current_user.id,
                                                             payment_status=models.PaymentStatus.paid_card if charge.status == "succeeded" else (
                                                                 models.PaymentStatus.pending if charge.status == "pending" else models.PaymentStatus.declined),
                                                             date=datetime.datetime.now(), charge_id=charge.id)

        else:
            transaction = models.Transaction.new_transaction(user_id=current_user.id,
                                                             payment_status=models.PaymentStatus.paid_cash,
                                                             date=datetime.datetime.now(), charge_id=None)

        if form.payment_type.data == "cash" or charge.status == "succeeded":
            for item in basket:
                ticket_list = list()
                for type, number in item.tickets.items():
                    for i in range(number):
                        ticket_list.append(type)
                reservation = models.Reservation.new_reservation(showing_id=item.showing.id,
                                                                 transaction_id=transaction.id)
                for i, seat in enumerate(item.seats):
                    ticket = models.Ticket.new_ticket(seat_id=seat.id, reservation_id=reservation.id,
                                                      ticket_type=ticket_list[i])

                if current_user.has_role("customer"):
                    msg = utilities.generate_email(reservation)
                    mail = Mail(app)
                    mail.send(msg)

            utilities.clear_basket()
            return redirect(url_for("bookings_page"))
        else:
            flash("Payment: {}".format(charge.status))

    if len(basket) != 0:
        return render_template('pages/checkout.html', form=form, total=total, basket_description=basket_description,
                           publishable_key=os.environ["STRIPE_PUBLISHABLE_KEY"])

    return redirect(url_for("basket_page"))

@app.route('/bookings')
@login_required
@roles_accepted('customer', 'staff', 'manager')
def bookings_page():
    transactions = models.Transaction.get_by_user_id(current_user.id)

    reservations = list()

    for transaction in transactions:
        for reservation in models.Reservation.get_by_transaction_id(transaction.id):
            reservation.showing = models.Showing.get_by_showing_id(reservation.showing_id)
            reservation.tickets = models.Ticket.get_by_reservation_id(reservation.id)

            reservation.transaction = transaction

            reservations.append(reservation)

    return render_template("pages/bookings.html", reservations=reservations, PaymentStatus=models.PaymentStatus)

@app.route("/update_firstname")
@login_required
def change_first_name():
    name = request.args["firstname"]
    values = models.User.query.filter(models.User.id == current_user.id).first()
    values.first_name = name
    db.session.commit()

    return jsonify({
        "firstname" : name
    })

@app.route("/update_surname")
@login_required
def change_last_name():
    name = request.args["surname"]
    values = models.User.query.filter(models.User.id == current_user.id).first()
    values.last_name = name
    db.session.commit()

    return jsonify({
        "lastname" : name
    })

@app.route("/update_email")
@login_required
def change_email():
    email = request.args["email"]
    if (len(models.User.query.filter_by(email=email).all()) == 0):
        values = models.User.query.filter(models.User.email == current_user.email).first()
        values.email = email
        db.session.commit()
    else:
        email = "ERROR"

    return jsonify({
        "email" : email
    })

@app.route("/download-tickets/<int:reservation_id>")
@login_required
@roles_accepted("customer", 'staff', 'manager')
def download_ticket_page(reservation_id):
    reservation = models.Reservation.query.filter_by(id=reservation_id).first()
    if reservation.transaction.user_id == current_user.id:
        locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

        showing = models.Showing.query.filter_by(id=reservation.showing_id).first()
        transaction = models.Transaction.query.filter_by(id=reservation.transaction_id).first()
        tickets = models.Ticket.query.filter_by(reservation_id=reservation.id).all()
        screen = models.Screen.query.filter_by(id=showing.screen_id).first()
        movie = models.Movie.query.filter_by(id=showing.movie_id).first()

        final_seat = ""
        final_cost = 0
        for i in tickets:
            seat = models.Seat.query.filter_by(id=i.seat_id).first()  # needs changing
            final_seat += seat.row + str(seat.column) + " "
            final_cost += utilities.get_ticket_cost(showing, i)

        final_name = current_user.first_name + ' ' + current_user.last_name

        users_email = current_user.email
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

        utilities.create_ticket(film_date, purchase_date, name_of_user, film_name, film_time, seat, screen, ticket_price, payment_status, transaction_id, id_required, certificate)

        return send_from_directory(filename="ticket.pdf", directory="utilities/tickets")
    else:
        flash(category="error", message="Not a valid reservation")
        return redirect(url_for("bookings_page"))
