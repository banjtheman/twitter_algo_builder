"""
Purpose:
    This file contains the class for WeightedFunction
"""

from typing import Any, Dict
import numbers
from .function import Function


class WeightedFunction:
    def __init__(self, weight: float, func: Function, name: str = None):
        """
        Purpose:
            Init WeightedFunction Class
        Args:
            weight: importance of function
            func: Function
        Returns:
            WeightedFunction class
        """

        if name:
            self.name = name
        else:
            self.name = self.func.name

        self.weight = weight
        self.func = func

    def get_name(self):
        """
        Purpose:
            Get name of function
        Args:
            N/A
        Returns:
            name of function
        """
        return self.name

    def run_code(self, tweet: Dict[str, Any]) -> int:
        """
        Purpose:
            Run the code for the algorithm
        Args:
            tweet: The tweet data to run the algorithm on
        Returns:
            result: the weighted score on how high the tweet should show on the feed
        """
        try:
            result = self.func.run_code(tweet)
        except Exception as error:
            raise RuntimeError(error)

        if not (isinstance(result, numbers.Number)):
            raise ValueError("Function must return a number")

        return result * self.weight
