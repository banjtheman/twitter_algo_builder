"""
Purpose:
    Start Python Algo Viewer
"""

# Python imports
import random
from typing import Type, Union, Dict, Any, List, Tuple
import requests

# 3rd party imports
import streamlit as st
import streamlit.components.v1 as components
from yellowbrick.target import FeatureCorrelation
import pandas as pd
import plotly.express as px
import altair as alt

# project imports
import test_algo_runner
import test_algo_builder
import algos


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

    pages = ["Home", "Playground", "Schedule", "Team"]
    default_page = 0
    page = st.sidebar.selectbox("Go To", options=pages, index=default_page)

    if page == "Home":
        home_page()
    # elif page == "Playground":
    #     playground_page()
    # elif page == "Schedule":
    #     schedule_page()
    # elif page == "Team":
    #     team_page()
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

    # # Select Algo
    # algos = ["Random"]
    # selected_algo = st.selectbox("Algorithms", algos)

    # # Look in Algos folder

    # # Show Algo
    # code = """def rand_algo(tweets):
    # """
    # st.code(code, language="python")

    # Button to get tweets

    # Have two cols, one for no aglo, one with algo

    num_tweets = st.number_input(label="Number of tweets", value=20, max_value=200)

    if st.button("Get Tweets"):

        # Get Raw tweets
        raw_tweets = test_algo_builder.get_home_timeline(num_tweets)

        ################ TODO: INPUT YOUR ALGO HERE ###############
        # Define algo
        # rand_algo = algos.Random_3_algo.define_algo()

        rand_algo = algos.SimpleAlgo.define_algo()

        ################ TODO: INPUT YOUR ALGO HERE ###############

        st.header(rand_algo.name)
        st.subheader(rand_algo.desc)

        # Run algo on tweets
        df = test_algo_builder.process_tweets(raw_tweets, rand_algo)

        # st.write(sorted_df)
        st.subheader("Given Input Weights")

        col1, col2, col3 = st.columns(3)
        col_list = [col1, col2, col3]

        for index, func in enumerate(rand_algo.functions):

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

                for index, func in enumerate(rand_algo.functions):

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
