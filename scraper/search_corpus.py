# Copyright (C) 2012-2013 Wesley Baugh
#
# This work is licensed under the Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit:
# http://creativecommons.org/licenses/by-nc-sa/3.0/
#
# This file was created using the streaming example from Tweepy
# as a general guide. Tweepy is licensed under the MIT License
# and is Copyright (c) 2009-2010 Joshua Roesslein.

"""Collects all tweets from the sample Public stream using Twitter's
streaming API, and saves them to a file for later use as a corpus.

The sample Public stream "Returns a small random sample of all public
statuses. The Tweets returned by the default access level are the same,
so if two different clients connect to this endpoint, they will see the
same Tweets."

This module consumes tweets from the sample Public stream and puts them
on a queue. The tweets are then consumed from the queue by writing them
to a file in JSON format as sent by twitter, with one tweet per line.
This file can then be processed and filtered as necessary to create a
corpus of tweets for use with Machine Learning, Natural Language Processing,
and other Human-Centered Computing applications.
"""

from __future__ import print_function

import sys
import threading
import Queue
import time
import socket
import httplib

from tweepy import OAuthHandler, RateLimitError, Stream, Cursor, API
from tweepy.streaming import StreamListener
from tweepy.utils import import_simplejson
from tweepy.error import TweepError
import staticconf
json = import_simplejson()


# Configuration file that contains the Twitter API credentials.
CONFIG_FILE = 'config.yaml'

# Number of seconds to wait after an exception before restarting the stream.
tcpip_delay = 0.25
MAX_TCPIP_TIMEOUT = 16
http_delay = 5
MAX_HTTP_TIMEOUT = 320

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except RateLimitError:
            return
        except TweepError:
            return

def main():
    staticconf.YamlConfiguration(CONFIG_FILE)
    auth = OAuthHandler(
        staticconf.read_string('twitter.consumer_key'),
        staticconf.read_string('twitter.consumer_secret'),
    )
    auth.set_access_token(
        staticconf.read_string('twitter.access_token'),
        staticconf.read_string('twitter.access_token_secret'),
    )
    api = API(auth)
    for tweet in limit_handled(Cursor(api.search,
        q='from:cnnbrk OR from:BBCBreaking OR from:CNN OR from:BBCWorld OR from:nytimes OR from:TIME OR from:AP OR from:Reuters OR from:NPR OR from:BreakingNews OR from:FoxNews OR from:WSJ OR from:AJEnglish OR from:TheEconomist OR from:CBSNews OR from:washingtonpost OR from:BBCNews OR from:NewsHour OR from:guardiannews', 
            #q=' OR '.join('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'),
            since="2016-04-20",
            until="2016-04-21",
            lang="en").items()):
        print(json.dumps(tweet._json))

if __name__ == '__main__':
    sys.exit(main())
