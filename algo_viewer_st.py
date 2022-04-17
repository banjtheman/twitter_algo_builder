"""
Purpose:
    Start Python Algo Viewer
"""

# Python imports
from typing import Type, Union, Dict, Any, List, Tuple
import requests
import glob

# 3rd party imports
import streamlit as st
import streamlit.components.v1 as components
from yellowbrick.target import FeatureCorrelation
import pandas as pd

# import plotly.express as px
# import altair as alt

# project imports
import test_algo_builder
import algo_builder.utils as utils
import algo_builder.algorithm


def feature_correlation(df: pd.DataFrame) -> None:
    """
    Purpose:
        Renders a feature correlation graph
    Args:
        df - Pandas dataframe
    Returns:
        N/A
    """
    target_string = "algo_score"

    feature_cols = [
        col
        for col in df.columns
        if col != target_string and col != "twitter_url" and df[col].dtype != "object"
    ]

    # method = st.selectbox(
    #     "Select the correlation method", ["mutual_info-regression", "pearson"]
    # )
    method = "mutual_info-regression"
    try:
        viz = FeatureCorrelation(method=method, feature_names=feature_cols, sort=True)
        viz.fit(df[feature_cols], df[target_string])
        fig = viz.fig
        ax = viz.show()
        fig.axes.append(ax)
        # show the viz
        st.write(fig)

    except Exception as error:
        st.write(df[target_string])
        st.error(error)


class Tweet(object):
    def __init__(self, s, embed_str=False):
        if not embed_str:
            # Use Twitter's oEmbed API
            # https://dev.twitter.com/web/embedded-tweets
            api = "https://publish.twitter.com/oembed?url={}".format(s)
            response = requests.get(api)
            self.text = response.json()["html"]
        else:
            self.text = s

    def _repr_html_(self):
        return self.text

    def component(self):
        return components.html(self.text, height=600)


def sidebar() -> None:
    """
    Purpose:
        Shows the side bar
    Args:
        N/A
    Returns:
        N/A
    """

    st.sidebar.title("Twitter Algo Viewer")

    pages = ["Home"]
    default_page = 0
    page = st.sidebar.selectbox("Go To", options=pages, index=default_page)

    if page == "Home":
        home_page()

    else:
        st.error("Invalid Page")


def home_page():
    """
    Purpose:
        Show home page
    Args:
        N/A
    Returns:
        N/A
    """

    st.title("Twitter Algo Viewer")
    st.subheader("Bring your own algo")

    algo_jsons = glob.glob("saved_algos/*.json")
    # Algo metadata
    algo_data_map = {}

    print(algo_jsons)
    for algo_json in algo_jsons:

        algo_data = utils.load_json(algo_json)

        algo_name = algo_data["name"]
        algo_desc = algo_data["desc"]
        algo_path = algo_data["algo_path"]

        # make new entry in map
        algo_data_map[algo_name] = {}
        algo_data_map[algo_name]["desc"] = algo_desc
        algo_data_map[algo_name]["algo"] = algo_path

    # Get list of algos

    print(algo_data_map)

    # Select Algo
    algos = list(algo_data_map.keys())
    selected_algo = st.selectbox("Algorithms", algos)

    # Have two cols, one for no aglo, one with algo?

    num_tweets = st.number_input(label="Number of tweets", value=20, max_value=200)

    if st.button("Get Tweets"):

        # Get Raw tweets
        raw_tweets = test_algo_builder.get_home_timeline(num_tweets)
        curr_algo_path = algo_data_map[selected_algo]["algo"]

        try:
            curr_algo = algo_builder.algorithm.load_algo(curr_algo_path)
        except Exception as error:
            st.error(error)
            st.stop()

        st.header(curr_algo.name)
        st.subheader(curr_algo.desc)

        # Run algo on tweets
        df = test_algo_builder.process_tweets(raw_tweets, curr_algo)

        # st.write(sorted_df)
        st.subheader("Given Input Weights")

        col1, col2, col3 = st.columns(3)
        col_list = [col1, col2, col3]

        for index, func in enumerate(curr_algo.functions):

            cur_col = index % 3  # Multipe of 3 for each weight
            col_list[cur_col].metric(func.get_name(), round(func.weight, 2))

        st.header("Feature Correlation")

        st.write(
            "This graph highlights which features are the most important in effecting the overall score of the algorithm."
        )
        feature_correlation(df)

        # Display tweets with the score
        for index, tweet in df.iterrows():

            st.metric("Score", tweet["algo_score"])

            with st.expander("Detials"):

                col1, col2, col3 = st.columns(3)
                col_list = [col1, col2, col3]

                for index, func in enumerate(curr_algo.functions):

                    name = func.get_name()

                    cur_col = index % 3  # Multipe of 3 for each weight
                    col_list[cur_col].metric(name, round(tweet[name], 2))

            tweet_display = Tweet(tweet["twitter_url"]).component()


def app() -> None:
    """
    Purpose:
        Controls the app flow
    Args:
        N/A
    Returns:
        N/A
    """

    # Spin up the sidebar, will control which page is loaded in the
    # main app
    sidebar()


def main() -> None:
    """
    Purpose:
        Controls the flow of the streamlit app
    Args:
        N/A
    Returns:
        N/A
    """

    # Start the streamlit app
    app()


if __name__ == "__main__":
    main()
