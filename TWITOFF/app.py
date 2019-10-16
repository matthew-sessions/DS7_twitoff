"""Main application for twitoff"""

from decouple import config
from flask import Flask, render_template, request, url_for, redirect
from .models import DB, User
import os
from .twitter import *

def create_app():
    """create and configures an instance of a flask app"""
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['ENV'] = config('ENV') #should change this later to production
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('home.html', title='Home', users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        u1 = User(name='matthew')
        DB.session.add(u1)
        DB.session.commit()
        return render_template('base.html', title='DB Reset')

    @app.route("/user/<value>")
    def list_tweets(value):
        user_tweets = TWITTER.get_user(value)
        tweets = user_tweets.timeline(count=200,exclude_replies=True,
                                        include_rts=False,mode='extended')
        js = tweets[0]._json
        js = js['user']['name']
        screen_name = js
        var = value
        return(render_template('user.html', tweets=tweets, screen_name=screen_name, var=var))

    @app.route('/user')
    def list_tweets2():
        name = request.args.get('name')
        return(redirect(f'/user/{name}'))
    return(app)
