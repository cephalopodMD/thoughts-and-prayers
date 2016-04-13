import json, sys, re, nltk
from pprint import pprint
from sets import Set
nltk.download("punkt")
tweets = []
# accepts json argument, creates bag of words for tweet
class Tweet:
	def __init__(self, json):
		self.json = json
		porter = nltk.PorterStemmer()
		tokens = nltk.word_tokenize(preprocess(json["text"]))
		self.terms = Set([porter.stem(t.lower()) for t in tokens])
# number of favorites normalized by number of followers		
def favoriteScore(tweet):
    return float(tweet.json["favourites_count"]) / tweet.json["followers_count"]
# number of retweets normalized by number of followers
def retweetScore(tweet):
    return float(tweet.json["retweet_count"]) / tweet.json["followers_count"]
# reads each json object in the file
def loadFile(file):
	for line in file:
		x=json.loads(line)
		tweets.append(Tweet(x))
	return
# removes hyperlinks and user mentions from text of tweet
def preprocess(str):
	return re.sub(r"(?:\@|https?\://)\S+", "", str)
f = open(sys.argv[1]) #file name is command line arg
loadFile(f)
print(tweets[0].terms)
