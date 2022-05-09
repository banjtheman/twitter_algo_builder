# Python imports
import logging
import os
from typing import Dict, Any, List

# 3rd party imports
import twitter

# project imports
import algos


CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN_KEY = os.environ["ACCESS_TOKEN_KEY"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]


def get_home_timeline(num_tweets: int = 20) -> List[Dict[str, Any]]:
    """
    Purpose:
        Get tweets from your timeline
    Args:
        num_tweets: number of twetts
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

    timeline_tweets = twitter_api.GetHomeTimeline(
        count=num_tweets, contributor_details=True
    )
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



def main():
    """
    Purpose:
        Show home page
    Args:
        N/A
    Returns:
        N/A
    """
    print("Running algorithm on Tweets")

    # Load Tweets
    timeline_tweets = get_home_timeline()

    # Define Algo
    rand_algo = algos.Random_3_algo.define_algo()
    rand_algo.save_algo()

    # Run algo on tweets
    df = rand_algo.process_tweets(timeline_tweets)
    #df.to_csv("test.csv",index=False) # Save csv output

    print(df)
    print("Done and Done")


if __name__ == "__main__":
    loglevel = logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    main()
