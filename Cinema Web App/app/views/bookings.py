from app import app, models, utilities, forms
from flask import render_template, jsonify, request, url_for, redirect, flash


@app.route('/showing/<int:showing_id>', methods=["GET", "POST"])
def showing_page(showing_id):
    showing = models.Showing.get_by_showing_id(showing_id)

    showing.movie = models.Movie.get_by_movie_id(showing.movie_id)
    showing.screen = models.Screen.get_by_screen_id(showing.screen_id)

    prices = dict(
        (ticket_type.name, dict((seat_type.name, utilities.get_ticket_multiplier(ticket_type) *
                                 utilities.get_seat_multiplier( seat_type) * showing.price)
                                for seat_type in models.SeatType)) for ticket_type in models.TicketType)

    form = forms.AddToBasketForm()
    if request.method == "POST" and form.validate_on_submit():
        seat_ids = form.seat_ids.data.split(",")

        tickets = form.tickets.data.split(",")

        are_available = True

        reservations = models.Reservation.get_by_showing_id(showing_id)

        for reservation in reservations:
            for ticket in models.Ticket.get_by_reservation_id(reservation.id):
                if ticket.seat_id in seat_ids:
                    are_available = False
        if not are_available:
            flash("Seats are no longer available")
        else:
            utilities.add_showing_to_basket(form.showing_id.data, seat_ids, {
                "regular": int(tickets[0]),
                "child": int(tickets[1]),
                "student": int(tickets[2]),
                "senior": int(tickets[3])
            })
            return redirect(url_for("basket_page"))

    return render_template("pages/showing.html", showing=showing, prices=prices, form=form)


@app.route('/showing/<int:showing_id>/seats', methods=["GET"])
def get_seats_for_showing(showing_id):
    showing = models.Showing.get_by_showing_id(showing_id)

    # get all reservations to this showing
    reservations = models.Reservation.get_by_showing_id(showing_id)

    """ 
    a list of the tickets already-booked tickets to this showing
    it's initialised with the IDs of the seats to this showing that the user already has in their basket, 
    stopping them from booking the same seat more than once in the same transaction
    """
    tickets = utilities.get_seats_in_basket_for_showing(showing_id)
    for reservation in reservations:
        # for each reservation to this showing, append the ticket ids in the reservation
        tickets = tickets + [ticket.seat_id for ticket in models.Ticket.get_by_reservation_id(reservation.id)]

    seats = models.Seat.get_by_screen_id(showing.screen_id)
    grid = dict()
    for seat in seats:
        if seat.row not in grid.keys():
            grid[seat.row] = dict()
        grid[seat.row][seat.column] = {
            "id": seat.id,
            "type": seat.seat_type.name,
            "taken": True if next(filter(lambda ticket: ticket == seat.id, tickets), False) else False
        }

    return jsonify(grid)


@app.route("/basket", methods=["GET", "POST"])
def basket_page():
    form = forms.RemoveFromBasketForm()
    if form.validate_on_submit():
        utilities.remove_from_basket(int(form.i.data))

    basket = utilities.get_basket(True)

    total = 0
    for item in basket:
        total += item.price

    empty = False
    if len(basket) == 0:
        empty = True
    return render_template("pages/basket.html", basket=enumerate(basket), total=total, removeForm=form, empty=empty)
