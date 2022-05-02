import random

from .algo_interface import TwitterAlgorithm
from algo_builder.function import Function
from algo_builder.weighted_function import WeightedFunction
from algo_builder.algorithm import Algorithm


def rand_func(tweet):
    """
    Purpose:
        Return a random number between -100 and 100
    Args:
        N/A
    Returns:
        random number
    """

    return random.randint(-100, 100)


class Random_3_algo(TwitterAlgorithm):
    def define_algo() -> Algorithm:
        """
        Purpose:
            Define a random algo
        Args:
            N/A
        Returns:
            random algo
        """
        # Make a random function
        rand_func_action = Function(
            "Random Function", "Returns a random value", rand_func
        )

        # Make three different weighted random functions
        weighted_func2 = WeightedFunction(0.2, rand_func_action, "rand_func2")
        weighted_func3 = WeightedFunction(0.3, rand_func_action, "rand_func3")
        weighted_func5 = WeightedFunction(0.5, rand_func_action, "rand_func5")

        # Create Random algo using all three functions
        rand_algo = Algorithm(
            "Random algo",
            "Return random score",
            [weighted_func2, weighted_func3, weighted_func5],
        )

        return rand_algo
