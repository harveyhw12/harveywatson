import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.environ["CSRF_SESSION_KEY"] if "CSRF_SESSION_KEY" in os.environ else "N@eX&T&@6??6?&#$cL!QeK#BYSe@GRtrmgqiA4A5"

# Secret key for signing cookies
SECRET_KEY = os.environ["SECRET_KEY"] if "SECRET_KEY" in os.environ else "o73X8Q$izE5EBGtNNBHsP@zeEjKBm5LR@Qmh?3L?"

# Flask Security settings
SECURITY_REGISTERABLE=True
SECURITY_RECOVERABLE=True
SECURITY_TRACKABLE=True
SECURITY_CHANGEABLE=True

SECURITY_RESET_URL="/forgot-password"
SECURITY_CHANGE_URL="/change-password"
SECURITY_POST_CHANGE_VIEW="/account"


# Flask Mail settings

MAIL_SERVER="smtp.sendgrid.net"
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME="apikey"
MAIL_PASSWORD= os.environ.get("SENDGRID_API_KEY")
MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
