import os

import flask

app = flask.Flask(__name__)

from . import views  # noqa E402
