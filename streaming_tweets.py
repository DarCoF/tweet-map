# Import packages for data gathering 
import requests
import tweepy
import json
import time

# Import packages for storing data
import dataset
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import create_engine

import init_settings

# Create database file for our tweets.
db = dataset.connect(init_settings.CONNECTION_STRING)
#db = create_engine(init_settings.CONNECTION_STRING, pool_pre_ping = True)

class StreamListener(tweepy.StreamListener): # Create personal subclass from Twitter StreamListener Class.
    def on_status(self, status):
        start = time.time()
        print(start)
        print('fetching tweet')
        if status.retweeted:
            return
        if 'RT' in status.text:
            return
       # if not hasattr(status, "retweeted_status") and status.text.startswith('RT @'):
        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
            
        if coords is not None:
            coords = json.dumps(coords)
                
        if geo is not None:
            geo = json.dumps(geo)

        end = time.time()
        print(end-start)
        table = db[init_settings.TABLE_NAME]

        try :            
            table.insert(dict(user_description = description,
                                followers_count = followers,
                                user_location = loc,
                                coordinates = coords,
                                geoloc = geo,
                                text = text,
                                user_name = name,
                                user_created = user_created,
                                id_str = id_str,
                                created = created,
                                retweet_count = retweets
                                ))
            end = time.time()
            print(end-start)

        except ProgrammingError as err:
            print(err)            

        
    def on_error(self, status_code):
        if status_code == 420:
            return False


# AUTHENTICATION KEYS AND CLASS INSTANTIATION
TWITTER_APP_KEY = init_settings.TWITTER_APP_KEY
TWITTER_APP_SECRET = init_settings.TWITTER_APP_SECRET
TWITTER_KEY = init_settings.TWITTER_KEY
TWITTER_SECRET = init_settings.TWITTER_SECRET

auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
api = tweepy.API(auth)

# Create instance of StreamListener Class
stream_listener = StreamListener()
# Create instance to tweepy Stream class. Two attributes are passed: 
# 1- authentication credentials to establish a connection; 2- stream_listener so that our callback functions are called.
stream = tweepy.Stream(auth = api.auth, listener = stream_listener) 
# Start streaming by calling the filter method. Start streaming from filter.json API
# endpoint and passing them to our listener callback.
stream.filter(track= init_settings.FILTER_TERMS) 