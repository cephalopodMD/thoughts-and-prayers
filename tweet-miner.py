import json, sys, re, nltk, csv
from pprint import pprint
from sets import Set
nltk.download("punkt")
tweets = []
unigrams = []
reload(sys)
sys.setdefaultencoding("UTF8")
# accepts json argument, creates bag of words for tweet
class Tweet:
	def __init__(self, csv):
		self.csv = csv
		porter = nltk.PorterStemmer()
		try:
			tokens = nltk.word_tokenize(preprocess(csv["Text"]))
		except UnicodeDecodeError:
			pass
		self.terms = []
		for token in tokens:
			try:
				t = porter.stem(token.lower())
				self.terms.append(t)
				if not t in unigrams:
					unigrams.append(t)
			except UnicodeDecodeError:
				pass
		self.terms = Set(self.terms)
# number of favorites normalized by number of followers		
def favoriteScore(tweet):
    return float(tweet.csv["Favorite Count"]) / tweet.json["Followers"]
# number of retweets normalized by number of followers
def retweetScore(tweet):
    return float(tweet.json["Retweet"]) / tweet.json["Followers"]
# reads each json object in the file
def loadFile(reader):
	for line in reader:
		tweets.append(Tweet(line))
	return
# removes hyperlinks and user mentions from text of tweet
def preprocess(string):
	string = re.sub(r'[^\w]', ' ', string)
	string = re.sub('_', ' ', string)
	return re.sub(r"(?:\@|https?\://)\S+", "", string)
f = open(sys.argv[1]) #file name is command line arg
reader = csv.DictReader(f,delimiter="\t")
loadFile(reader)
f2 = open("un.txt", "w")
#print tweets[1].csv["retweet_count"]
unigrams.sort()
#print unigrams
for u in unigrams:
	f2.write("%s\n" % u)
	#f2.write("%s %s\n" % (tweet.csv["Followers"], tweet.csv["Retweet"]))
