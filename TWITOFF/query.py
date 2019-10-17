from .models import *
from .twitter import *


def populate_data(username):
    try:
        User.query.filter(User.name == username).one()
        return(True)
    except:
        twitter_user = TWITTER.get_user(username)
        tweets=twitter_user.timeline(count=200, exclude_replies=True,
        include_rts=False, tweet_mode='extended')
        db_user=User(id=twitter_user.id,name=twitter_user.screen_name,
        full_name=twitter_user.name, newest_tweet_id=tweets[0].id)

        for tweet in tweets:
            embedding=BASILICA.embed_sentence(tweet.full_text,
                                                model='twitter')
            db_tweet=Tweet(date_posted=str(tweet.created_at), id=tweet.id,text=tweet.full_text[:500],
                            embedding=embedding)
            DB.session.add(db_tweet)
            db_user.tweets.append(db_tweet)

        DB.session.add(db_user)
        DB.session.commit()
        return(False)

def drop_user(name):
    userq = User.query.filter(User.name == name)
    userid = userq[0].id
    tweets = Tweet.query.filter(Tweet.user_id==userid)
    userq.delete(synchronize_session=False)
    tweets.delete(synchronize_session=False)
    DB.session.commit()
