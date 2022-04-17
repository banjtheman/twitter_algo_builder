"""
Purpose:
    This file contains the class for Algorithm
"""

from typing import Any, Dict, List
from .weighted_function import WeightedFunction
import pickle
from . import utils


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


def load_algo(filename) -> Algorithm:
    """
    Purpose:
        Save the algo
    Args:
        filename: name to save
    Returns:
        result: The rating of your tweet
    """
    # read the pickle file
    picklefile = open(filename, "rb")
    # unpickle the dataframe
    loaded_algo = pickle.load(picklefile)
    # close file
    picklefile.close()
    return loaded_algo
