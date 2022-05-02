# Python imports
import logging

# my imports
import algos
import algo_builder.algorithm as algo


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

    # Load algo
    loaded_algo = algo.load_algo('saved_algos/Random algo.algo')
    print(f"Loaded algo {loaded_algo.name}")

    print("Done and Done")


if __name__ == "__main__":
    loglevel = logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    main()
