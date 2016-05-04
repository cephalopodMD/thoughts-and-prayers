# methods for getting features of tweets go here
# __init__ is so you can so you can say
# from features import function
# to import a function into your library

import re

mention_re = re.compile(r"(^|\s)@[a-zA-Z0-9]")
phone_re = re.compile(r"(\+?[0-9]\s?)?(\(?[0-9][0-9][0-9]\(?)?\s?\-?\s?[0-9][0-9][0-9]\s?\-?\s?[0-9][0-9][0-9][0-9]")
email_re = re.compile(r"[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+")
happy_re = re.compile(r"(\:|\;|\B)\-?(\)|\D|\])+")
sad_re = re.compile(r"(\:|\;|\B)\,?\'?\-?(\(|\[)+")
all_caps_re = re.compile("[A-Z]")
all_caps_re = re.compile("(^|\s)[A-Z]+(\s|\Z)")
all_caps_re = re.compile("(^|\s)[a-z]+(\s|\Z)")
all_caps_re = re.compile("(^|\s)[A-Z][a-z]+(\s|\Z)")
print("yolo")

#takes the full tweet
def hashtag_count(tweet_text):
    return len([ word for word in tweet_text.split() if word.startswith("#") ])

#takes the full tweet text
def mention_count(tweet_text):
	# try this one: re.compile(r' (?<=^|(?<=[^a-zA-Z0-9-_\\.]))@([A-Za-z]+[A-Za-z0-9_]+)')
    
    return len(mention_re.findall(tweet_text))
    
#takes the full tweet text
def phone_count(tweet_text):
    
    return len(phone_re.findall(tweet_text))
    
#takes the full tweet text
def email_count(tweet_text):
    
    return len(email_re.findall(tweet_text))
    
#takes the full tweet text
#returns dict of happy and sad counts
def emoticons(tweet_text):
    
    happy_count = len(happy_re.findall(tweet_text))
    sad_count = len(sad_re.findall(tweet_text))
    return {"happy":happy_count, "sad":sad_count}

#kind of useless, but maybe there's other stuff to account for?
def tweet_length(tweet_text):
    return len(tweet_text)

#takes tweet text
#returns float fraction of characters in A-Z
def capital_char_fraction(tweet_text):
    
    caps_count = len(all_caps_re.findall(tweet_text))
    return caps_count / float(len(tweet_text))

#takes tweet text
#returns count of all caps words
def all_caps_words(tweet_text):
    
    return len(all_caps_re.findall(tweet_text))

#takes tweet text
#returns count of lowercase words
def lowercase_words(tweet_text):
    
    return len(all_caps_re.findall(tweet_text))

#takes tweet text
#returns count of camel case (eg. "The Quick Brown Fox") words
def camel_case_words(tweet_text):
    
    return len(all_caps_re.findall(tweet_text))

#utility function
#takes arbitrary string and character
#returns number of times character occurs in string 
def num_occurrences(string, char):
	count = 0
	for c in string:
		if c == char:
			count += 1
	return count
    
#takes tweet text
#returns dict of punctuation counts
def punctuation_counts(tweet_text):
	period_count = num_occurrences(tweet_text, ".")
	comma_count = num_occurrences(tweet_text, ",")
	semicolon_count = num_occurrences(tweet_text, ";")
	colon_count = num_occurrences(tweet_text, ":")
	exclamation_count = num_occurrences(tweet_text, "!")
	apostrophe_count = num_occurrences(tweet_text, "'")
	quotation_count = num_occurrences(tweet_text, "\"")
	hyphen_count = num_occurrences(tweet_text, "-")
	return {"period":period_count, "comma":comma_count, "semicolon":semicolon_count, "colon":colon_count, "exclamation":exclamation_count, "apostrophe":apostrophe_count, "quotation":quotation_count, "hyphen":hyphen_count}

#takes tweet text
#returns dict of punctuation counts
#this will be about 8 times faster in theory since it's only one pass'
def alt_punctuation_counts(tweet_text):
    result = {'.':0,',':0,';':0,':':0,'!':0,'?':0,'\'':0,'"':0,'-':0,'_':0}
    for char in tweet_text:
        if char in result:
            result[char] += 1
    return result
