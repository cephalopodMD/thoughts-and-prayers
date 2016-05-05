
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
from time import sleep
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
            sleep(60)
        except TweepError:
            sleep(60)

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

    big_ben_ids = [727256357607464960, 
                   727271714187522048, 
                   727287317912817664, 
                   727302414039158785, 
                   727317768509480960, 
                   727332108876705794, 
                   727347714380419072, 
                   727362055750176768, 
                   727377660742123520, 
                   727393264060534784, 
                   727407354162122753, 
                   727422705876762624,
                   727437555210293248, 
                   727452651210809344, 
                   727468761842876416, 
                   727483610119413760,
                   727498961741856768, 
                   727513051440762881, 
                   727528910452305921, 
                   727543248458149888,
                   727559107612422144, 
                   727574712830857221, 
                   727588550133288961, 
                   727603646221914113,
                   727619000348348416]

    for startid, endid in zip(big_ben_ids, big_ben_ids[1:]):
        for tweet in limit_handled(Cursor(api.search,
                q=' OR '.join('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'),
                since_id=str(startid),
                max_id=str(endid),
                lang="en").items(2500)):
            print(json.dumps(tweet._json))

if __name__ == '__main__':
    sys.exit(main())
