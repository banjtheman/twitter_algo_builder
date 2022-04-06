# Python imports
import argparse
import json
import logging
import os
from typing import Dict, Any
import random

import pandas as pd
import twitter


CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN_KEY = os.environ["ACCESS_TOKEN_KEY"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]


def get_home_timeline():
    """
    Purpose:
        Get tweets from your timeline
    Args:
        N/A
    Returns:
        tweets from timeline
    """
    twitter_api = twitter.Api(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token_key=ACCESS_TOKEN_KEY,
        access_token_secret=ACCESS_TOKEN_SECRET,
        tweet_mode="extended",
    )

    timeline_tweets = twitter_api.GetHomeTimeline(contributor_details=True)
    # home_timeline = [i.full_text for i in timeline_tweets]

    # Create tweet url_field

    twitter_json_list = []

    for tweet in timeline_tweets:

        username = tweet.user.screen_name  # Username vlaue
        id_str = tweet.id_str  # id str

        curr_tweet = tweet._json  # JSON object

        # Get the twitter url
        curr_tweet["twitter_url"] = f"https://twitter.com/{username}/status/{id_str}"

        # Add the json to list
        twitter_json_list.append(curr_tweet)

    return twitter_json_list


def rand_algo(tweets):
    """
    Purpose:
        Randomly sort tweets
    Args:
        tweets - tweets from API
    Returns:
        algo_tweets - sorted tweets based on algo
    """

    for tweet in tweets:
        # Give a random score to each tweet
        tweet["algo_score"] = random.randint(0, 100)

    return tweets


def weighted_rand_algo(tweets, weight_names, weight_values):
    """
    Purpose:
        Randomly sort tweets
    Args:
        tweets - tweets from API
    Returns:
        algo_tweets - sorted tweets based on algo
    """

    tweet_values_list = []

    for tweet in tweets:
        # Give a random score to each tweet
        tweet_values_json = {}
        algo_score = 0  # The score for the algo

        for index, weight_name in enumerate(weight_names):

            # Random number times weight
            curr_value = random.randint(0, 100) * weight_values[index]
            tweet_values_json[weight_name] = curr_value
            # Add to final score
            algo_score += curr_value

        tweet_values_json["algo_score"] = algo_score
        tweet_values_json["twitter_url"] = tweet["twitter_url"]

        # Add to list
        tweet_values_list.append(tweet_values_json)

    # Turn list to df
    df = pd.json_normalize(tweet_values_list)

    return df


def main():
    """
    Purpose:
        Show home page
    Args:
        N/A
    Returns:
        N/A
    """
    print("Getting Tweets")

    # Load Tweets
    timeline_tweets = get_home_timeline()

    # Define algo
    weight_names = ["rand_val_3", "rand_val_5", "rand_val_2"]
    weight_values = [0.3, 0.5, 0.2]

    # Run algo
    df = weighted_rand_algo(timeline_tweets, weight_names, weight_values)

    # Sort df
    sorted_df = df.sort_values(by=["algo_score"], ascending=False)

    print(sorted_df)

    # Run your algo...
    # algo_tweets = rand_algo(timeline_tweets)

    # Sort algo tweets
    # algo_tweets = sorted(algo_tweets, key=lambda x: x["algo_score"], reverse=True)

    # Display tweets with the score
    # for tweet in algo_tweets:
    #     print(f"Score: {tweet['algo_score']}\n Text:{tweet['full_text']}")

    print("Done and done")


if __name__ == "__main__":
    loglevel = logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    main()
