# methods for getting features of tweets go here
# __init__ is so you can so you can say
# from features import function
#to import a function into your library

import re

#takes the full tweet text
def mention_count(tweet_text):
    mention_re = re.compile(r"@[a-zA-Z0-9]")
    return len(mention_re.findall(tweet_text))
    
#takes the full tweet text
def phone_count(tweet_text):
    phone_re = re.compile(r"(\+?[0-9]\s?)?(\(?[0-9][0-9][0-9]\(?)?\s?\-?\s?[0-9][0-9][0-9]\s?\-?\s?[0-9][0-9][0-9][0-9]")
    return len(phone_re.findall(tweet_text))
    
#takes the full tweet text
def email_count(tweet_text):
    email_re = re.compile(r"[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+")
    return len(email_re.findall(tweet_text))
    
#takes the full tweet text
#returns dict of happy and sad counts
def emoticons(tweet_text):
    happy_re = re.compile(r"(\:|\;|\B)\-?(\)|\D|\])+")
    sad_re = re.compile(r"(\:|\;|\B)\,?\'?\-?(\(|\[)+")
    happy_count = len(happy_re.findall(tweet_text))
    sad_count = len(sad_re.findall(tweet_text))
    return {"happy":happy_count, "sad":sad_count}

#kind of useless, but maybe there's other stuff to account for?
def tweet_length(tweet_text):
    return len(tweet_text)

#takes tweet text
#returns float fraction of characters in A-Z
def capital_char_fraction(tweet_text):
    all_caps_re = re.compile("[A-Z]")
    caps_count = len(all_caps_re.findall(tweet_text))
    return caps_count / float(len(tweet_text))

#takes tweet text
#returns count of all caps words
def all_caps_words(tweet_text):
    all_caps_re = re.compile("(^|\s)[A-Z]+(\s|\Z)")
    return len(all_caps_re.findall(tweet_text))

#takes tweet text
#returns count of lowercase words
def lowercase_words(tweet_text):
    all_caps_re = re.compile("(^|\s)[a-z]+(\s|\Z)")
    return len(all_caps_re.findall(tweet_text))

#takes tweet text
#returns count of camel case (eg. "The Quick Brown Fox") words
def camel_case_words(tweet_text):
    all_caps_re = re.compile("(^|\s)[A-Z][a-z]+(\s|\Z)")
    return len(all_caps_re.findall(tweet_text))

#takes tweet text
#returns dict of punctuation counts
def punctuation_counts(tweet_text):
    pass
    #incomplete
