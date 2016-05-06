# get all the stuff from the csv
import numpy as np
import pandas
print("starting")
df = pandas.read_csv("corpus2.csv", sep='\t', error_bad_lines=False) #ignore bad lines
print("removing null entries")
df = df[pandas.notnull(df['Text'])]
df = df.drop_duplicates(subset = 'Text')
print(df.shape)
# 2600 tweets over 5000
# 6600 tweets over 1000
threshold = 1000
thresh_count = len(df[df['Retweet'] > threshold])
from random import random
def keep(retweets):
    if retweets > threshold:
        return True
    else:
        if random() < float(thresh_count) / float(len(df)-thresh_count):
            return True
        else:
            return False
print("normalizing corpus")
df = df[df['Retweet'].map(keep)]
print(df.shape)

# label data
print("labeling data")
df['Viral'] =df['Retweet'].apply(lambda retweet: 1 if retweet >= threshold else 0)
train_labels = df.Viral.values
labels = list(set(train_labels))

#stemming and stuff
print("stemming")
from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.stem.snowball import *
stemmer = SnowballStemmer('english')
#stemmer = PorterStemmer('english')

#stopwords?
#stop = ['amp', 'cc', 'did', 'don', 'rt', 'll', 'oh', 've', 'yes', 'let', 'going', 'via', 're', 'tweet' ]
stop = []
#http://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
# preProcess(str):
#     url_pattern = re.compile(r'http(s?)://[\w./]+')
#     pic_pattern = re.compile(r'pic.twitter.com/[\w.]+')
#     str = pic_pattern.sub("", str)
#     str = url_pattern.sub("", str)
#     return str
# http://shahmirj.com/blog/extracting-twitter-usertags-using-regex
class NoUrls_CountVectorizer(CountVectorizer):
    def build_preprocessor(self):
        url_pattern = re.compile(r'http(s?)://[\w./]+')
        pic_pattern = re.compile(r'pic.twitter.com/[\w.]+')
        preprocessor = super(NoUrls_CountVectorizer, self).build_preprocessor()
        return lambda doc: (pic_pattern.sub('', url_pattern.sub('', preprocessor(doc)) ))

class NoUrls_Stemmed_CountVectorizer(CountVectorizer):
    def build_preprocessor(self):
        url_pattern = re.compile(r'(?:\@|https?://)\S+')
        pic_pattern = re.compile(r'pic.twitter.com/[\w.]+')
        at_pattern = re.compile(r' (?<=^|(?<=[^a-zA-Z0-9-_\\.]))@([A-Za-z]+[A-Za-z0-9_]+)')
        preprocessor = super(NoUrls_Stemmed_CountVectorizer, self).build_preprocessor()
        return lambda doc: (pic_pattern.sub('', url_pattern.sub('', preprocessor(doc)) ))
    #right now just doing splits on whitespace and stemming 
    def build_tokenizer(self):
        tokenizer = super(NoUrls_Stemmed_CountVectorizer, self).build_tokenizer()
        def process(word):
            if (word.isdigit()):
                if (int(word) >= 1800 and int(word) <= 2050):
                    word = "00000YEAR"
                else: 
                    word = "00000NUM"
            else:
                word =stemmer.stem(word)
            return word
        return lambda doc: (process(w) for w in tokenizer(doc))
vectorizer = NoUrls_Stemmed_CountVectorizer(ngram_range = (1,1), binary =True,
                                    min_df=2, stop_words=stop, strip_accents='ascii')

# separate document content
documents = df.Text
X_count = vectorizer.fit_transform(documents)

# import scipy and get labels and features
import scipy
print("metadata")
linkCount = [df.LinkCount]
linkCount = np.array(linkCount)
X_metadata = scipy.sparse.csr_matrix(linkCount.T)
X = scipy.sparse.hstack([X_count, X_metadata])
train_labels = np.array(train_labels)
train_features = X

# Make SVM classifier
print("starting svm")
from sklearn import svm
# linear or not?
name = "Liblinear"
# loss=?, penalty=?, dual=False?, tol=1e-3
classifier = svm.LinearSVC()
classifier.fit(train_features, train_labels)

#http://stackoverflow.com/questions/25250654/how-can-i-use-a-custom-feature-selection-function-in-scikit-learns-pipeline
#http://zacstewart.com/2014/08/05/pipelines-of-featureunions-of-pipelines.html

from sklearn.base import TransformerMixin
from pandas import DataFrame
from features import *
#define custom transformers
class HourOfDayTransformer(TransformerMixin):
    #gets hour from datetime field
    def transform(self, X, **transform_params):
        hours = X['DateTime'].apply(lambda x: int(x.split(" ")[3].split(":")[0]))
        return hours

    def fit(self, X, y=None, **fit_params):
        return self

import math
class FollowersTransformer(TransformerMixin):
    #gets hour from datetime field
    def transform(self, X, **transform_params):
        followers = X['Followers'].apply(lambda x: int(x) if isinstance(x, str) and x.isdigit() else 0)
        return followers

    def fit(self, X, y=None, **fit_params):
        return self

class ColumnExtractor(TransformerMixin):
    def __init__(self, colName):
        self.colName = colName
        
    def transform(self, X, **transform_params):
        text = X[self.colName].values
        return text

    def fit(self, X, y=None, **fit_params):
        return self

class NormalizeShape(TransformerMixin):
    #X is in format df[''].values
    def transform(self, X, **transform_params):
        normalized_array = scipy.sparse.csr_matrix(np.array((X))).T
        return normalized_array

    def fit(self, X, y=None, **fit_params):
        return self

class HashTagCount(TransformerMixin):
    #gets hashtag count
    def transform(self, X, **transform_params):
        hashcount = X['Text'].apply(lambda x: hashtag_count(x)) #custom function
        return hashcount

    def fit(self, X, y=None, **fit_params):
        return self
    
class MentionCount(TransformerMixin):
    def transform(self, X, **transform_params):
        mentions = X['Text'].apply(lambda x: mention_count(x)) #custom function
        return mentions

    def fit(self, X, y=None, **fit_params):
        return self
    
class CapitalCharRatio(TransformerMixin):
    def transform(self, X, **transform_params):
        ratios = X['Text'].apply(lambda x: capital_char_fraction(x)) #custom function
        return ratios

    def fit(self, X, y=None, **fit_params):
        return self
    
class PhoneCount(TransformerMixin):
    def transform(self, X, **transform_params):
        counts = X['Text'].apply(lambda x: email_count(x)) #custom function
        return counts

    def fit(self, X, y=None, **fit_params):
        return self
    
class EmailCount(TransformerMixin):
    def transform(self, X, **transform_params):
        counts = X['Text'].apply(lambda x: phone_count(x)) #custom function
        return counts

    def fit(self, X, y=None, **fit_params):
        return self

class HappyCount(TransformerMixin):
    def transform(self, X, **transform_params):
        counts = X['Text'].apply(lambda x:  emoticons(x)["happy"]) #custom function
        return counts

    def fit(self, X, y=None, **fit_params):
        return self
    
class SadCount(TransformerMixin):
    def transform(self, X, **transform_params):
        counts = X['Text'].apply(lambda x:  emoticons(x)["sad"]) #custom function
        return counts

    def fit(self, X, y=None, **fit_params):
        return self
    
class PunctuationCount(TransformerMixin):
    def __init__(self, punctuation):
        self.punctuation = punctuation
        
    def transform(self, X, **transform_params):
        counts = X['Text'].apply(lambda x:  alt_punctuation_counts(x)[self.punctuation]) #custom function
        return counts

    def fit(self, X, y=None, **fit_params):
        return self
    
class TweetLength(TransformerMixin):
    def transform(self, X, **transform_params):
        counts = X['Text'].apply(lambda x:  tweet_length(x)) #custom function
        return counts

    def fit(self, X, y=None, **fit_params):
        return self
    
class CamelCounts(TransformerMixin):
    def transform(self, X, **transform_params):
        counts = X['Text'].apply(lambda x:  camel_case_words(x)) #custom function
        return counts

    def fit(self, X, y=None, **fit_params):
        return self
    
class UpperCounts(TransformerMixin):
    def transform(self, X, **transform_params):
        counts = X['Text'].apply(lambda x: all_caps_words(x)) #custom function
        return counts

    def fit(self, X, y=None, **fit_params):
        return self
    
class LowerCounts(TransformerMixin):
    def transform(self, X, **transform_params):
        counts = X['Text'].apply(lambda x: lowercase_words(x)) #custom function
        return counts

    def fit(self, X, y=None, **fit_params):
        return self
        
# train and test
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.feature_selection import SelectKBest, chi2
import time
t0 = time.time()
pipeline = Pipeline([
    ('features', FeatureUnion([
        ('binary_unigram', Pipeline([ 
            ('extract', ColumnExtractor(colName = 'Text')),
            ('vectorizer',   NoUrls_CountVectorizer(ngram_range = (1,1), binary =True,
                                            min_df=2, stop_words=stop, strip_accents='ascii'))
        ])),
         ('semicolon_count', Pipeline([
            ('extract', PunctuationCount(punctuation = ';')),
            ('normalize',   NormalizeShape()),
        ])),
         ('colon_count', Pipeline([
            ('extract', PunctuationCount(punctuation = ':')),
            ('normalize',   NormalizeShape()),
        ])),
        ('questionmark_count', Pipeline([
            ('extract', PunctuationCount(punctuation = '?')),
            ('normalize',   NormalizeShape()),
        ])),
        ('exclamation_count', Pipeline([
            ('extract', PunctuationCount(punctuation = '!')),
            ('normalize',   NormalizeShape()),
        ])),
        ('hyphen_count', Pipeline([
            ('extract', PunctuationCount(punctuation = '-')),
            ('normalize',   NormalizeShape()),
        ])),
        ('period_count', Pipeline([
            ('extract', PunctuationCount(punctuation = '.')),
            ('normalize',   NormalizeShape()),
        ])),
         ('quotation_count', Pipeline([
            ('extract', PunctuationCount(punctuation = '"')),
            ('normalize',   NormalizeShape()),
        ])),
         ('apostrophe_count', Pipeline([
            ('extract', PunctuationCount(punctuation = '\'')),
            ('normalize',   NormalizeShape()),
        ])),
         ('sad_count', Pipeline([
            ('extract', SadCount()),
            ('normalize',   NormalizeShape()),
        ])),
        ('happy_count', Pipeline([
            ('extract', HappyCount()),
            ('normalize',   NormalizeShape()),
        ])),
        ('phone_count', Pipeline([
            ('extract', PhoneCount()),
            ('normalize',   NormalizeShape()),
        ])),
        ('email_count', Pipeline([
            ('extract', EmailCount()),
            ('normalize',   NormalizeShape()),
        ])),
        ('hashtag_count', Pipeline([
            ('extract', HashTagCount()),
            ('normalize',   NormalizeShape()),
        ])),
        ('mention_count', Pipeline([
            ('extract', MentionCount()),
            ('normalize',   NormalizeShape()),
        ])),
        ('link_count', Pipeline([
            ('extract', ColumnExtractor(colName = 'LinkCount')),
            ('normalize',   NormalizeShape()),
        ])),
        ('follower_count', Pipeline([
            ('extract', FollowersTransformer()),
            ('normalize',   NormalizeShape()),
        ])),
        ('hourofday', Pipeline([
            ('gethour', HourOfDayTransformer()),
            ('normalize',   NormalizeShape()),
        ])),
    ])),
    ('feature_selector', SelectKBest(chi2, k=4000)),
    ('classifier',  svm.LinearSVC(penalty='l1', dual=False, C=0.1)) 
])

from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
#adapted from http://zacstewart.com/2015/04/28/document-classification-with-scikit-learn.html
k_fold = KFold(n=len(df), n_folds=10)
scores = []
confusion = np.array([[0, 0], [0, 0]])

for train_indices, test_indices in k_fold:
    #train_text = df.iloc[train_indices]['Text'].values
    train_text = df.iloc[train_indices]
    train_y = df.iloc[train_indices]['Viral'].values
    
    #test_text = df.iloc[test_indices]['Text'].values
    test_text = df.iloc[test_indices]
    test_y = df.iloc[test_indices]['Viral'].values
    
    pipeline.fit(train_text, train_y)
    predictions = pipeline.predict(test_text)

    #update totals
    confusion += confusion_matrix(test_y, predictions)
    score = f1_score(test_y, predictions, pos_label=1)
    scores.append(score)
t1 = time.time()
total = t1-t0
print('Time:', total)
print('Total tweets classified:', len(df))
print('Score:', sum(scores)/len(scores))
print('Confusion matrix:')
print(confusion)
print("precision:")
print(precision_score(test_y, predictions, pos_label = 1))
print("recall:")
print(recall_score(test_y, predictions, pos_label = 1))
