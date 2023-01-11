from app import app, utilities
from flask import render_template, request, redirect
import datetime
import locale


@app.errorhandler(404)
def not_found_page(error):
    return render_template('pages/404.html'), 404


@app.context_processor
def context():
    tickets_in_basket = utilities.tickets_in_basket()
    theme = utilities.get_theme()
    return {
        "tickets_in_basket": tickets_in_basket if tickets_in_basket > 0 else "",
        "theme": theme
    }


@app.template_filter()
def format_datetime(value, format="%d-%m-%Y"):
    if type(value) is not datetime.date and type(value) is not datetime.datetime and type(value) is not datetime.time:
        value = datetime.datetime.fromisoformat(value)
    return value.strftime(format)


@app.template_filter()
def format_money(value):
    locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')
    return locale.currency(int(value) / 100, symbol=True, grouping=True)


@app.route('/update_theme/<theme>', methods=["POST", "GET"])
def update_theme(theme):
    attempt_update = utilities.set_theme(theme)
    if not attempt_update:
        # the arg was invalid
        pass
    return redirect(request.referrer)


@app.route("/.well-known/acme-challenge/<challenge>")
def lets_encrypt_ssl_validation(challenge):
    if challenge == "8f9_UKfQ-hWfYO5MnmUwjVyN7ZSboG89ErTRocK6HGk":
        return "8f9_UKfQ-hWfYO5MnmUwjVyN7ZSboG89ErTRocK6HGk.9NArLPJeWhHK51QMXegTu8TZCBiAyZZ9z3o_vUQzm5U"
