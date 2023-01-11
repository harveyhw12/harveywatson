from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class NewMovieForm(FlaskForm):
        movie_name = StringField("Movie Title", validators=[DataRequired()])
