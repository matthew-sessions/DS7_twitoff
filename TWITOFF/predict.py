"""Prediction of Users based on Tweet embeddings."""
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import BASILICA

def predict_user(user1_name, user2_name, tweet_text, cache=None):
    """Determine and return which user is more likely to say something"""
    user_set = pickle.dumps((user1_name, user2_name))
    if cache and cache.exists(user_set):
        log_reg = pickle.loads(cache.get(user_set))
    else:
        user1 = User.query.filter(User.name == user1_name).one()
        user2 = User.query.filter(User.name == user2_name).one()
        user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
        user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
        embeddings = np.vstack([user1_embeddings, user2_embeddings])
        labels = np.concatenate([np.zeros(len(user1.tweets)),
                                 np.ones(len(user2.tweets))])
        log_reg = LogisticRegression().fit(embeddings, labels)
        cache and cache.set(user_set, pickle.dumps(log_reg))
    tweet_embeddings = BASILICA.embed_sentence(tweet_text, model='twitter')
    return log_reg.predict(np.array(tweet_embeddings).reshape(1, -1)),log_reg.predict_proba(np.array(tweet_embeddings).reshape(1, -1))


def logic(user1, user2, num1, num2):
    if num1 > num2:
        return(user1, user2, f'@{user1} is more likely to tweet:')
    else:
        return(user2, user1, f'@{user2} is more likely to tweet:')
