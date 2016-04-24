# methods for getting features of tweets go here
# __init__ is so you can import from the features module

import re

#takes the full tweet text
def mention_count(tweet_text):
    mention_re = re.compile(r"@[a-zA-Z0-9]")
    return len(mention_re.findall(tweet_text))
    
#takes the full tweet text
def phone_count(tweet_text):
    mention_re = re.compile(r"(\+?[0-9]\s?)?(\(?[0-9][0-9][0-9]\(?)?\s?\-?\s?[0-9][0-9][0-9]\s?\-?\s?[0-9][0-9][0-9][0-9]")
    return len(mention_re.findall(tweet_text))
    
