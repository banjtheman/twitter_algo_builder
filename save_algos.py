# Python imports
import logging

# my imports
import algos


def main():
    """
    Purpose:
        Show home page
    Args:
        N/A
    Returns:
        N/A
    """
    print("Saving algorithm")

    # TODO can we get it to save all Algos?
    # Replace with your algo
    # my_algo = algos.SimpleAlgo.define_algo()
    my_algo = algos.Random_3_algo.define_algo()
    my_algo.save_algo()

    print("Done and Done")


if __name__ == "__main__":
    loglevel = logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    main()
