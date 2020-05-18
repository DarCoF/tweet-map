# tweet-map
## Introduction
At the end 'Tweet_analysis.ipynb' a simple interactive map shows a collectiong of tweets divided by sentiment. The code presented here works as a simple template for streaming tweets directly from Twitter API, applying a simple sentiment analysis and, finally, plotting those tweets across the globe based on user_location.

For this particular study, three keywords related with Tesla were specified for the streaming filter. But the code is structured in a way that any filter could be apply easily.

## How it works?
The code is composed by three different files:
- settings.py
- streaming_tweets.py
- Tweet_analysis

# settings.py
Several variables must be initialized such as access and token keys for Twitter API; filter keywords; database string...

# streaming_tweets.py
If not desired, there is no need to modify anything from this file. Just run it and it'll start fetching off tweets from API through tweepy.
However, if you wish to modify which properties must be extracted from each tweet json, simply modify the StreamListener class as you please!

# Tweet_analysis
Main core of the study is here. Tweets are transfered into a dataframe, clean, user location converted into coordinates, sentiment analysis applied to text and tweets are plotted in map.


## Requirements
All requirements for this projects are listed in requirements.txt.
