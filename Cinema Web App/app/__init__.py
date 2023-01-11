from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail

app = Flask(__name__)

app.config.from_object('config')

if 'SECURITY_PASSWORD_SALT' not in app.config:
    app.config['SECURITY_PASSWORD_SALT'] = app.config['SECRET_KEY']

db = SQLAlchemy(app)

from app import models, forms


db.create_all()
migrate = Migrate(app, db)

user_datastore = SQLAlchemyUserDatastore(db, models.user.User, models.user.Role)
security = Security(app, user_datastore, register_form=forms.ExtendedRegisterForm)
mail = Mail(app)
app.extensions['mail'].debug = 0


from app import utilities

from app import views

if __name__ == '__main__':
    app.run()
