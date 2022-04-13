# Twitter Algorithm Builder

On March 24, 2022 Twitter ~~Board~~ Member Elon Musk created a [poll](https://twitter.com/elonmusk/status/1507041396242407424) asking... "Twitter algorithm should be open source"

![Elon Poll](images/elon_twiiter_opensource_poll.png)

With an 82% of responses saying yes, this highlighted an unmet need in the public sphere. This repo provides an opinionated framework to build your own twitter algorithm, that you can use on your own timeline.  

## How it works

![Twitter API](images/twitter_api_diag.png)
The Twitter Algo builder leverages the get [home timeline](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-home_timeline) API endpoint to get a list of tweets for the user. Next the tweets are passed into your input algorithm which scores each tweet. The UI then provides a Feature Correlation graph that highlights which features are affecting the overall score of the algorithm, as well as the ranked tweets.

## Getting Started
TODO

### Twiiter API

### Get Tweets

### Run sample algo

### Update sample algo

### Run streamlit


### Example Algorithms
Here are some example algorithms

### Weighted Random Algo
TODO

### Postive + Tweet Length
TODO
