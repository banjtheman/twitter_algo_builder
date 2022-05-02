"""
Purpose:
    This file contains the class for Algorithm
"""

from typing import Any, Dict, List
from .weighted_function import WeightedFunction
import pickle
from . import utils
import pandas as pd


class Algorithm:
    def __init__(self, name: str, desc: str, functions: List[WeightedFunction]):
        """
        Purpose:
            Init Algorithm Class
        Args:
            name: Name of function
            desc: description of function
            functions: list of functions for the Algorithm
        Returns:
            Algorithm class
        """

        self.name = name
        self.desc = desc
        self.functions = functions
        
    # TODO do we need this function?
    def run_algo(self, tweet: Dict[str, Any]) -> int:
        """
        Purpose:
            Run the code for the algorithm
        Args:
            tweet: The tweet data to run the algorithm on
        Returns:
            result: The rating of your tweet
        """
        result = 0
        try:

            for func in self.functions:
                result += func.run_code(tweet)
        except Exception as error:
            raise RuntimeError(error)

        return result

    def save_algo(self, folder="saved_algos"):
        """
        Purpose:
            Save the algo
        Args:
            folder: folder to save data
        Returns:
            result: The rating of your tweet
        """

        algo_file = f"{folder}/{self.name}.algo"
        algo_json_file = f"{folder}/{self.name}.json"

        # create a pickle file
        picklefile = open(algo_file, "wb")
        # pickle the algo and write it to file
        pickle.dump(self, picklefile)
        # close the file
        picklefile.close()

        algo_json = {"name": self.name, "desc": self.desc, "algo_path": algo_file}

        utils.save_json(algo_json_file, algo_json)


    def process_tweets(self, tweets: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Purpose:
            Run the algorithm on the tweets
        Args:
            tweets - List of tweets
        Returns:
            algo_tweets - sorted tweets based on algo
        """

        tweet_values_list = []

        for tweet in tweets:
            tweet_values_json = {}
            algo_score = 0  # The score for the algo

            # Run all the functions in the algorithm
            for func in self.functions:
                # print(func.get_name())

                curr_value = func.run_code(tweet)  # Run the code on the tweet
                tweet_values_json[func.get_name()] = curr_value  # store value

                # Add to final score
                algo_score += curr_value

            tweet_values_json["algo_score"] = algo_score
            tweet_values_json["twitter_url"] = tweet["twitter_url"]

            # Add to list
            tweet_values_list.append(tweet_values_json)

        # Turn list to df
        df = pd.json_normalize(tweet_values_list)

        # Sort df
        sorted_df = df.sort_values(by=["algo_score"], ascending=False)

        return sorted_df



def load_algo(filename) -> Algorithm:
    """
    Purpose:
        Load the algo
    Args:
        filename: file to load
    Returns:
        Algorithm: The loaded Algorithm
    """
    # read the pickle file
    picklefile = open(filename, "rb")
    # unpickle the dataframe
    loaded_algo = pickle.load(picklefile)
    # close file
    picklefile.close()
    return loaded_algo
