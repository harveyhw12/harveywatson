from app import app, models, utilities
from flask import render_template, request, jsonify
import datetime, requests
from sqlalchemy import and_


@app.route("/")
def index_page():
    movies = models.Movie.get_all_active()

    movie_casts = {}
    for movie in movies:
        movie_casts[movie.id] = models.CastMovieAssociation.get_top_cast(movie.id, 6)

    db_models = utilities.get_carousel_movies()

    return render_template("pages/index.html", movies=movies, carousel=db_models, movie_casts=movie_casts, navbar_fade_in=True)


@app.route("/movies/<int:movie_id>")
def movie_page(movie_id):
    movie = models.Movie.get_by_movie_id(movie_id)

    movie_cast = models.CastMovieAssociation.get_top_cast(movie.id, 12)

    showings = models.Showing.get_by_movie_id(movie.id, future=True)

    showings = list(utilities.group_showings(showings))
    for showing in showings:
        showing_list = []
        if len(showing[1]) > 1:
            for x in showing[1]:
                pass

            showing[1] = sorted(showing[1], key=lambda x: x.time)

    for index, (day, dayShowings) in enumerate(showings):
        if day == datetime.date.today().strftime("%A %d %b"):
            showings[index] = ("Today", dayShowings)
        elif day == (datetime.date.today() + datetime.timedelta(days=1)).strftime("%A %d %b"):
            showings[index] = ("Tomorrow", dayShowings)

    return render_template("pages/movie.html", movie=movie, showings=showings, ShowingType=models.ShowingType, movie_cast=movie_cast)


@app.route("/api/movies/get_date", methods=["GET"])
def api_movies_by_showing_date():
    input = request.args["input"]
    ids = []
    try:
        date = datetime.datetime.strptime(input, "%d/%m/%Y")
        date_to_search = datetime.datetime(year=date.year, month=date.month,day=date.day,hour=0,minute=0,second=0)
        showings = models.Showing.query.filter(and_(models.Showing.time>=date_to_search,models.Showing.time<=date_to_search+datetime.timedelta(hours=23, minutes=59))).all()
        for showing in showings:
            if showing.movie_id not in ids:
                ids.append(showing.movie_id)
    except:
        movies = models.Movie.query.all()
        titles = []
        keywords = {}
        for movie in movies:
            keywords[movie.id] = [keyword.name for keyword in movie.keywords]
            for key in keywords.keys():
                for word in keywords[key]:
                    if input in word:
                        ids.append(key)
            if input in movie.title.lower():
                ids.append(movie.id)
    return jsonify({"ids": ids})
