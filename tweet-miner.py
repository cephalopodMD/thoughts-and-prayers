import json, sys, re
from pprint import pprint
tweets = []
# number of favorites normalized by number of followers
def favoriteScore(tweet):
    return float(tweet["favourites_count"]) / tweet["followers_count"]
# number of retweets normalized by number of followers
def retweetScore(tweet):
    return float(tweet["retweet_count"]) / tweet["followers_count"]
# reads each json object in the file
def loadFile(file):
	for line in file:
		x=json.loads(line)
		tweets.append(x)
	return
# removes hyperlinks and user mentions from text of tweet
def preprocess(str):
	return re.sub(r"(?:\@|https?\://)\S+", "", str)
f = open(sys.argv[1]) #file name is command line arg
loadFile(f)
print(preprocess(tweets[0]["text"]))
