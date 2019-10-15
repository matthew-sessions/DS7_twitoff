"""Main application for twitoff"""

from flask import Flask, render_template
from .models import DB
import os


def create_app():
    """creates and configures an instace of a flask app"""

    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    DB.init_app(app)

    @app.route('/')
    def root():
        return('Welcome')
    return(app)
