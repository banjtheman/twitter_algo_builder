"""
Purpose:
    This file contains the class for Algorithm
"""

from typing import Any, Dict, List
from .weighted_function import WeightedFunction


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
