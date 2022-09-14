import os
from datetime import timedelta


# Statement for enabling the development environment
DEBUG = os.environ.get("DEBUG", "false") == "true"
TESTING = os.environ.get("TESTING", "false") == "true"

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = os.environ["DB_URL"]
SQLALCHEMY_ECHO = False
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = False

# Secret key
SECRET_KEY = os.environ["SECRET_KEY"]

BCRYPT_HANDLE_LONG_PASSWORDS = True


# --------JWT--------------
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_TOKEN_LOCATION = ("headers",)
JWT_COOKIE_CSRF_PROTECT = False  # Even though we're a JSON API, this is good practice
JWT_REFRESH_TOKEN_EXPIRES = False
JWT_ACCESS_TOKEN_EXPIRES = False
# JWT_REFRESH_TOKEN_EXPIRES = False
# JWT_ACCESS_TOKEN_EXPIRES = False
JWT_CLAIMS_IN_REFRESH_TOKEN = False
JWT_ERROR_MESSAGE_KEY = "message"
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"
JWT_BLACKLIST_ENABLED = False


# ---------Confirmation Tokens---------
CONFIRMATION_TOKEN_BYTES = 32
CONFIRMATION_TOKEN_EXPIRY = timedelta(days=1)


# ----- CRYPTO -------
BCRYPT_LOG_ROUNDS = 12
