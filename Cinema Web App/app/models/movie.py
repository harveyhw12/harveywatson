from app import db, models

keywords_movies = db.Table('keywords_movies', db.Column("keyword_id", db.Integer(), db.ForeignKey("keyword.id")),
                           db.Column("movie_id", db.Integer(), db.ForeignKey("movie.id")))


class CastMovieAssociation(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    cast_member_id = db.Column(db.Integer, db.ForeignKey('cast_members.id'), primary_key=True)
    order = db.Column(db.Integer)
    cast = db.relationship("CastMember")

    @staticmethod
    def get_top_cast(movie_id, number_actors):
        movie_cast_associations = CastMovieAssociation.query.filter_by(movie_id=movie_id).order_by(CastMovieAssociation.order).all()
        movie_cast = []
        for actor in movie_cast_associations:
            movie_cast.append(models.CastMember.query.filter_by(id=actor.cast_member_id).first())
        movie_cast = movie_cast[:number_actors]
        return movie_cast


class CastMember(db.Model):
    __tablename__ = "cast_members"
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer)
    name = db.Column(db.String)
    profile_url = db.Column(db.String)

    @staticmethod
    def get_by_id(cast_id):
        return CastMember.query.filter_by(id=cast_id).first()


class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer)
    name = db.Column(db.String)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(255))
    tagline = db.Column(db.String(255))
    overview = db.Column(db.Text)
    runtime = db.Column(db.Integer)
    release_date = db.Column(db.Date)
    backdrop_url = db.Column(db.String(255))
    poster_url = db.Column(db.String(255))
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer)
    is_adult = db.Column(db.Boolean)
    certification = db.Column(db.String(3))
    active = db.Column(db.Boolean())
    showings = db.relationship('Showing', backref="movie", lazy=True)
    cast = db.relationship('CastMovieAssociation')
    keywords = db.relationship('Keyword', secondary=keywords_movies, backref=db.backref('movies', lazy=True))

    @staticmethod
    def get_by_movie_id(movie_id):
        return Movie.query.get(movie_id)

    @staticmethod
    def get_all():
        return Movie.query.all()

    @staticmethod
    def get_all_active():
        return Movie.query.filter_by(active=True).all()

    @staticmethod
    def get_showing_movie_title(showing):
        return Movie.query.filter_by(id=showing.movie_id).first().title

    @staticmethod
    def get_movie_title_by_id(movie_id):
        movie = Movie.query.filter_by(id=movie_id).first()
        if movie is None:
            return -1
        else:
            return Movie.query.filter_by(id=movie_id).first().title

    @staticmethod
    def new_movie(tmdb_id, title, tagline, overview, runtime, release_date, backdrop_url, poster_url, vote_average,
                  vote_count, is_adult, save=True, active=True):
        movie = Movie(tmdb_id=tmdb_id, title=title, tagline=tagline, overview=overview, runtime=runtime,
                      release_date=release_date, backdrop_url=backdrop_url, poster_url=poster_url,
                      vote_average=vote_average, vote_count=vote_count, is_adult=is_adult, active=active)
        if save is True:
            db.session.add(movie)
            db.session.commit()
        return movie
