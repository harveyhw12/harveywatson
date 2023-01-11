from flask import session
from app import models
from .ticket_cost_calculator import get_seat_cost

BASKET_SESSION_KEY = "basket"


class BasketItem:
    def __init__(self, showing, seats, tickets, populate=False):
        if not populate:
            self.showing = showing
            self.seats = seats
            self.tickets = tickets
            self.price = 0
        else:
            self.showing = models.Showing.get_by_showing_id(showing)
            self.tickets = tickets
            ticket_list = list()
            for type, number in tickets.items():
                for i in range(number):
                    ticket_list.append(type)
            self.seats = list()
            self.price = 0
            for i, seat_id in enumerate(seats):
                seat = models.Seat.get_by_seat_id(seat_id)
                self.seats.append(seat)
                self.price += get_seat_cost(self.showing, seat, models.TicketType[ticket_list[i]])


def _check_basket_exists():
    if BASKET_SESSION_KEY not in session:
        session[BASKET_SESSION_KEY] = list()


def _add_to_basket(item):
    basket = session[BASKET_SESSION_KEY]
    same_showing_found = False
    for reservation in basket:
        if item['showing_id'] == reservation['showing_id']:
            for seat in item['seat_ids']:
                reservation['seat_ids'].append(seat)
            reservation['tickets']['child'] += item['tickets']['child']
            reservation['tickets']['regular'] += item['tickets']['regular']
            reservation['tickets']['senior'] += item['tickets']['senior']
            reservation['tickets']['student'] += item['tickets']['student']
            same_showing_found = True
            break

    if same_showing_found is False:
        basket.append(item)

    session[BASKET_SESSION_KEY] = basket


def remove_from_basket(index):
    _check_basket_exists()
    basket = session[BASKET_SESSION_KEY]
    basket.pop(index)
    session[BASKET_SESSION_KEY] = basket


def clear_basket():
    _check_basket_exists()
    session[BASKET_SESSION_KEY] = list()


def add_showing_to_basket(showing_id, seat_ids, tickets):
    _check_basket_exists()
    _add_to_basket({
        "showing_id": showing_id,
        "seat_ids": seat_ids,
        "tickets": tickets
    })


def get_basket(populate=False):
    if BASKET_SESSION_KEY not in session:
        return list()
    return list(map(lambda i: BasketItem(i["showing_id"], i["seat_ids"], i["tickets"], populate), session[BASKET_SESSION_KEY]))


def print_basket():
    _check_basket_exists()
    for item in session[BASKET_SESSION_KEY]:
        print(item)


def basket_length():
    return len(session[BASKET_SESSION_KEY]) if BASKET_SESSION_KEY in session else 0


def tickets_in_basket():
    _check_basket_exists()
    number_tickets = 0
    for reservation in session[BASKET_SESSION_KEY]:
        number_tickets += len(reservation['seat_ids'])

    return number_tickets


def get_seats_in_basket_for_showing(showing_id):
    _check_basket_exists()
    seats_in_basket = []
    for reservation in session[BASKET_SESSION_KEY]:
        if reservation['showing_id'] == str(showing_id):
            for seat_id in reservation['seat_ids']:
                seats_in_basket.append(int(seat_id))
    return seats_in_basket
