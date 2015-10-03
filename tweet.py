import sys
import os
import twitter
from random import choice

user1 = sys.argv[1]
user2 = sys.argv[2]

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

# This will print info about credentials to make sure they're correct
# print api.VerifyCredentials()

# Get tweets from one user's timeline

def get_tweets(username):
    """Gets all tweets for a user from the API and stores them in a list"""

    timeline_info = api.GetUserTimeline(screen_name=username)
    #statuses = [s.text for s in timeline_info]

    one_long_tweet = [] #List will be separated by ", u"

    # Can this loop below be written as a list comprehension?
    for status in timeline_info:
        tweet = status.text
        if tweet[0:2] != "RT":
            one_long_tweet.append(tweet)

    return one_long_tweet

def mix_lists(list1, list2):
    """Alternates between lists adding each tweet to a master string"""

    #Find out which list is shorter and store that length as n
    n = min(len(list1), len(list2))

    master_string = ""

    for i in range(n): 
        master_string += list1[i] + " "
        master_string += list2[i] + " "

    #Disregard other tweets if one list is longer than the other so that one user 
    #doesn't take over the markov tweet.

    return master_string


def make_chains(master_string):
    """Takes the master_string and returns a dictionary of markov chains"""

    tweetionary = {}

    words = master_string.split()

    for i in range(len(words)-2):
        word1 = words[i]
        word2 = words[i + 1]
        word3 = words[i + 2]

        #Filters out words starting with @ and https:// and adds other words to tweetionary
        if word1.startswith("@"):     
            word1 = word1[1:]
        elif word1.startswith("https://") or word1.startswith("http://") :
            pass 
        else:
            key = (word1, word2)
            value = word3

            if key not in tweetionary:
                tweetionary[key] = []

            tweetionary[key].append(value)

    return tweetionary

def make_text(tweetionary):
    """Takes a dictionary of markov chains and returns random text"""

    # Start with a capital letter
    # Not really necessary for tweets

    # keys_list = tweetionary.keys()
    # capital_keys = [key for key in keys_list if key[0].istitle()]
    # new_key = choice(capital_keys)
    # text = [new_key[0], new_key[1]]

    key = choice(tweetionary.keys())
    words = [key[0], key[1]]

    while key in tweetionary:
    # Keep looping until we have a key that isn't in the chains
    # (which would mean it was the end of our original text)
    #
    # Note that for long texts (like a full book), this might mean
    # it would run for a very long time.

    word = choice(tweetionary[key])
    words.append(word)
    key = (key[1], word)

user1_tweets = get_tweets(user1)
user2_tweets = get_tweets(user2)
all_tweets = mix_lists(user1_tweets, user2_tweets)


