from flask import render_template, jsonify, request, redirect, url_for, flash
from app import app, models, utilities, forms, db
from sqlalchemy import and_
from flask_security import roles_accepted, login_required
import random, datetime, requests

"""
there are four types of comparison

1 : get cinema's overall income
    - plot this on a line graph of income (y) against time (x)
    - scale time ticks dynamically based on the range of dates that showings exist for
    
2 : get the income for all movies in a given week
    plot this on:
    - a bart chart of income (y) against movie (x)
    - a line graph of time (x) 

3 : get income for a given movie
    - plot this on a line graph with income (y) against time (x) and scale time ticks dynamically
    
4 : compare ticket sales for movies between two dates
    plot this on:
    - a line graph with ticket sales (y) against time (x)
        - plot each movie as 1 series on the graph
    - a bar chart with ticket sales (y) against movie (x)
"""


@app.route('/graphs')
@login_required
@roles_accepted("staff", "manager")
def staff_graphs_page():
    today = datetime.datetime.now()
    next_week = today + datetime.timedelta(days=7)
    return render_template('pages/graphs.html', today=today.strftime("%Y-%m-%d"),next_week=next_week.strftime("%Y-%m-%d"))


@app.route('/api/graphs/total-income')
@login_required
@roles_accepted("staff", "manager")
def api_total_income_graph():
    incomes = utilities.get_total_income()
    incomes_cumulative = utilities.get_total_income(cumulative=True)
    return jsonify({
        "incomes": incomes,
        "incomes_cumulative": incomes_cumulative
    })


# comparison 2
@app.route('/api/graphs/weekly-analysis')
@login_required
@roles_accepted("staff", "manager")
def api_weekly_analysis_graph():
    date_as_datetime = datetime.datetime.strptime(request.args["week"], "%Y-%m-%d")
    to_send, dates = utilities.get_all_weekly_incomes(date_as_datetime)
    return jsonify({
        "movies": to_send,
        "dates": dates
    })


# populates dropdown box with current movies being shown
@app.route('/api/movies', methods=["GET"])
@login_required
@roles_accepted("staff", "manager")
def api_movies():
    return jsonify(list(map(lambda x: {"title": x.title, "id": x.id}, models.Movie.query.all())))


# comparison 3
@app.route('/api/graphs/movie-income', methods=["GET"])
@login_required
@roles_accepted("staff", "manager")
def api_movie_income_graph():
    movie_id = request.args['id']
    incomes = utilities.get_movie_income(movie_id)
    incomes_cumulative = utilities.get_movie_income(movie_id, cumulative=True)
    return jsonify({
        "incomes": incomes,
        "incomes_cumulative": incomes_cumulative
    })


# comparison 4
@app.route('/api/graphs/ticket-sales-range')
@login_required
@roles_accepted("staff", "manager")
def api_ticket_sales_graph():
    movie_ids = request.args['ids'].split(",") if "ids" in request.args or request.args["ids"] != "" else []
    start_date = datetime.datetime.strptime(request.args["start_date"], "%Y-%m-%d")
    end_date = datetime.datetime.strptime(request.args["end_date"], "%Y-%m-%d")
    ticket_sales, dates = utilities.ticket_sales_range(movie_ids, start_date, end_date)
    return jsonify({
        "ticket_sales": ticket_sales,
        "dates": dates
    })


@app.route('/edit-showings')
@login_required
@roles_accepted("staff", "manager")
def edit_showings():
    return render_template("/pages/edit-showings.html", ShowingType=models.ShowingType)


@app.route('/get-screens')
@login_required
@roles_accepted("staff", "manager")
def get_screens():
    return jsonify(list(map(lambda x: {"name": x.screen_name, "id": x.id}, models.Screen.query.all())))


@app.route('/get-showings')
@login_required
@roles_accepted("staff", "manager")
def get_showings():
    screen_id = int(request.args['screen_id'])
    date = request.args['date']
    date_as_datetime = datetime.datetime.strptime(date, "%Y-%m-%d")
    showings = models.Showing.query.filter(and_(models.Showing.screen_id==int(screen_id), models.Showing.time >= date_as_datetime, models.Showing.time <= date_as_datetime + datetime.timedelta(days=1))).all()
    ids = {}
    for showing in showings:
        ids[showing.id] = [showing.time, showing.movie.title]
    return jsonify({
        "showings":ids
    })


@app.route("/edit-chosen-showings/<int:showing_id>")
@login_required
@roles_accepted("staff", "manager")
def edit_chosen_showings(showing_id):
    total = 0
    success = True
    showings = models.Showing.query.filter_by(id=showing_id)
    for showing in showings:
        reservations = models.Reservation.query.filter_by(showing_id=showing.id).all()
        if len(reservations) > 0:
            for reservation in reservations:
                tickets = models.Ticket.query.filter_by(reservation_id=reservation.id).all()
                total += len(tickets)
    if total != 0:
        success = False
        flash(category="error", message="Tickets exist for this showing and therefore it could not be deleted")
    else:
        utilities.delete_showing(showing_id)
        db.session.commit();
    return redirect(url_for("edit_showings"))


@app.route("/create-showing")
@login_required
@roles_accepted("staff", "manager")
def create_showing():
    success = True
    screen_id = request.args['screen_id']
    movie_id = request.args['movie_id']
    time = request.args['time']
    time_as_datetime = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M")
    showing_type = request.args["showing_type"]
    movie_runtime = models.Movie.query.filter_by(id=movie_id).first().runtime
    showings = models.Showing.query.filter(and_(models.Showing.screen_id == screen_id,models.Showing.time >=time_as_datetime, models.Showing.time <= time_as_datetime+datetime.timedelta(minutes=movie_runtime))).all()
    if len(showings) != 0:
        success = False
    else:
        if showing_type == "1":
            showing_type = models.ShowingType.regular
        elif showing_type == "2":
            showing_type = models.ShowingType.audio_descriptions
        else:
            showing_type = models.ShowingType.subtitles
        models.Showing.new_showing(screen_id, showing_type, movie_id, time_as_datetime, 1000)

    return jsonify({
        "success" : success
    })


@app.route("/schedule-showing", methods=['GET','POST'])
@login_required
@roles_accepted("staff", "manager")
def schedule_showings():

    if utilities.populate_showings(datetime.datetime.now()) == 0:
        flash(category="error", message="Movies already scheduled for this week")
    else:
        flash(message="Successfully scheduled movies")
    return redirect(url_for("account_page"))
