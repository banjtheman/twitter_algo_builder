import random
from textblob import TextBlob

from .algo_interface import TwitterAlgorithm
from algo_builder.function import Function
from algo_builder.weighted_function import WeightedFunction
from algo_builder.algorithm import Algorithm


def tweet_length(tweet):
    """
    Purpose:
        The longer the tweet, the higher I want to see
    Args:
        tweet: tweet data
    Returns:
        score based on tweet length
    """

    char_lens = len(tweet["full_text"])

    # edge case if longer than 280 chars
    if char_lens > 280:
        char_lens = 280

    return float(char_lens / 2.8)


def textblob_sent(tweet):
    """
    Purpose:
        Postive tweets have higher score
    Args:
        tweet: tweet data
    Returns:
        score based on sentiment
    """
    analysis = TextBlob(tweet["full_text"])
    score = analysis.sentiment.polarity

    if score >= 1.0:
        score = 1.0

    final_score = score * 100

    # safety check
    if final_score > 100.0:
        return 100

    return final_score


class SimpleAlgo(TwitterAlgorithm):
    def define_algo() -> Algorithm:
        """
        Purpose:
            Define a simple algo
        Args:
            N/A
        Returns:
            random algo
        """
        # Make a tweet length function
        tweet_length_func = Function(
            "Tweet Length", "Longer tweets are more important", tweet_length
        )

        # Make a tweet length function
        text_blob_sent = Function(
            "TextBlob Sentiment", "Postive tweets are higher", textblob_sent
        )

        # Make three different weighted random functions
        weighted_func2 = WeightedFunction(1, tweet_length_func, "tweet_length")
        weighted_func3 = WeightedFunction(1, text_blob_sent, "textblob_sent")

        # Create Random algo using all three functions
        rand_algo = Algorithm(
            "Simple Algo",
            "Tweet Length and Sentiment",
            [weighted_func2, weighted_func3],
        )

        return rand_algo
