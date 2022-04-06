"""
Purpose:
    This file contains the class for Function
"""

from typing import Any, Dict
import numbers
import types


class Function:
    def __init__(self, name: str, desc: str, code: types.FunctionType):
        """
        Purpose:
            Init Function Class
        Args:
            name: Name of function
            desc: description of function
            code: code of the function
        Returns:
            Function class
        """

        self.name = name
        self.desc = desc

        if not callable(code):
            raise ValueError("Code must be a function")

        self.code = code

    def run_code(self, tweet: Dict[str, Any]) -> int:
        """
        Purpose:
            Run the code for the algorithm
        Args:
            tweet: The tweet data to run the algorithm on
        Returns:
            result: number betwen 0 - 100 on how high the tweet should show on the feed
        """
        try:
            result = self.code(tweet)
            print(self.code)
        except Exception as error:
            raise RuntimeError(error)

        if not (isinstance(result, numbers.Number)):
            print(result)
            raise ValueError("Function must return a number")

        if not (result >= -100 and result <= 100):
            print(result)
            raise ValueError("Function must return a number between -100 and 100")

        return result
