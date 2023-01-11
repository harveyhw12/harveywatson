from app import app, utilities, db, forms,models
from flask import render_template, request, redirect, url_for, jsonify, flash
import requests
TMDB_API_KEY = "61ef4fbecf526fda5a8e8dc72bbc92b9"


@app.route('/get-movies')
def get_movies():
    return jsonify({
        "inactive_movies" : inactive_movies
    })


@app.route('/new-movie', methods=["GET", "POST"])
def new_movie():
    inactive_movies = models.Movie.query.filter_by(active=False)
    movie_results = []
    results = []
    return render_template('pages/new_movie.html', inactive_movies=inactive_movies, movie_results=movie_results)


# adds a new movie to the database
@app.route('/add-movie', methods=["GET", "POST"])
def add_movie():
    id = request.args["input"]
    success = True
    utilities.populate_movie(id)
    db.session.commit()
    flash("Movie successfully added to cinema.")
    return jsonify({
        "success": success
    })


# page to show the currently-active movies that could be removed
@app.route('/remove-movie', methods=["GET", "POST"])
def remove_movie():
    movies = models.Movie.query.filter_by(active=True)

    return render_template('pages/remove_movie.html', movies=movies)


# marks a movie as inactive in the database
@app.route('/removing', methods=["GET", "POST"])
def delete_movie():
    id = request.args['input']
    success = True
    if models.Showing.check_future_showings_exist(id):
        success = False
        flash(category="error", message="Showings exist for this movie and therefore it could not be deleted")
        return jsonify({
            "success": success
        })
    utilities.delete_movie(id)
    db.session.commit()
    flash(category="success", message="Movies successfully removed from cinema")
    return jsonify({
        "success":success
    })

# gets a list of movies from TMDB given some search text
@app.route("/get-tmdb-search")
def tmdb_movies():
    movie_name = request.args['title']
    movie_for_page = []
    results = []
    movie_name = movie_name.split(" ")
    movie_string = ""
    for i in range(len(movie_name)):
        if i == len(movie_name)-1:
            movie_string += movie_name[i]
        else:
            movie_string += movie_name[i]
            movie_string += "+"
    response = requests.get("https://api.themoviedb.org/3/search/movie?api_key={}&query={}".format(TMDB_API_KEY, movie_string))
    try:
        results = response.json()['results']
    except:
        exit();
    movies_to_show = []
    movie_ids = []
    movies = models.Movie.query.all()
    for movie in movies:
        movie_ids.append(movie.tmdb_id)
    titles = []
    ids = []
    poster_urls = []
    for result in results:
        if result["id"] not in movie_ids:
            movies_to_show.append(result)
            titles.append(result["title"])
            ids.append(result["id"])
            url = "https://image.tmdb.org/t/p/w500{}".format(result["poster_path"])
            if result["poster_path"] == None:
                url="../../static/images/blank-poster.png"
            poster_urls.append(url)

    for movie in movie_for_page:
        titles.append(movie.title)
        ids.append(movie.tmdb_id)
        poster_urls.append(movie.poster_url)
    return jsonify({
        "titles": titles,
        "ids" : ids,
        "poster_urls" : poster_urls
    })
