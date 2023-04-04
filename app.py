#IMPORTING NECESSARY MODULES/LIBRARIES
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.subplots as sp
import credentials
import settings
import mysql.connector
import pandas as pd
import time
import itertools
import math
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.express as px
import datetime
from IPython.display import clear_output
from plotly.subplots import make_subplots
import plotly.graph_objs as go

from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import nltk
from sqlalchemy import create_engine
import numpy as np
import requests
import json

#FUNCTIONS
def clean_content(content):
    content = re.sub(r"http\S+", "", content)
    content = content.replace('&amp;', 'and')
    content = re.sub('[^A-Za-z0-9]+', ' ', content)
    content = content.lower()
    return content

def create_filtered_sen(content):
    tokenwords = word_tokenize(content)
    stop_words = set(stopwords.words('english'))
    filtered_sen = [word for word in tokenwords if word not in stop_words]
    return filtered_sen

def create_frequency_df(filtered_sen):
    fdist = FreqDist(filtered_sen)
    fd = pd.DataFrame(fdist.most_common(20),
                    columns=["Word", "Frequency"]).drop([0]).reindex()
    return fd

api_key =credentials.CMC_API_KEY

def get_ethereum_price(api_key):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    }
    params = {"id": "1027"}  # Ethereum's ID on CoinMarketCap
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    price = data["data"]["1027"]["quote"]["USD"]["price"]
    timestamp = data["data"]["1027"]["last_updated"]
    return price, timestamp

# Fetch Ethereum price data
eth_price, timestamp = get_ethereum_price(api_key)
ethereum_prices = [eth_price]
timestamps = [pd.to_datetime(timestamp)]

#INITIALIZING APP

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#CREATING LAYOUT
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1("Real-time Twitter Sentiment Analysis of Ethereum"), style={'textAlign':'center'}
                    ,
                )
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="sentiment-graph"),
                )
            ],
            className="mb-3",
        ),
        dcc.Interval(id="interval", interval=60 * 1000, n_intervals=0),  # 60 seconds interval
    ],
    fluid=True,
)

@app.callback(
    Output("sentiment-graph", "figure"),
    [Input("interval", "n_intervals")],)

def update_graph(n):
    clear_output()
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=credentials.MYSQLPASSWORD,
        database="TwitterDB",
        charset = 'utf8'
    )

    timenow=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = "SELECT id_str, text, created_at, polarity FROM {} WHERE created_at >= '{}' " \
                            .format("ethereum",timenow)
    engine = create_engine('mysql+mysqlconnector://root:credentials.MYSQLPASSWORD@localhost:3306/twitterdb')

    df = pd.read_sql(query, con=db_connection)
    df['created_at']=pd.to_datetime(df['created_at'])

    sentiment_figure = make_subplots(
    rows=4, cols=2,
    subplot_titles=("Ethereum Sentiment on Twitter", "Ethereum Price in USD ($) - Powered by CoinMarketCap.com ", "Frequently Used Words in Tweets related to Ethereum",
                    "Top Words Used in Negative Sentiment Tweets", "Top Words Used in Positive Sentiment Tweets"),
    row_heights=[0.3, 0.2, 0.2, 0.3],
    specs=[[{"type": "scatter","colspan":1}, {"type": "scatter","colspan":1}],
           [{"type": "bar", "colspan": 2}, None],
           [{"type": "bar", "colspan": 2}, None],
           [{"type": "bar", "colspan": 2}, None]])

     ### TIME SERIES FOR SENTIMENT ####

    #CLEAN AND TRANSFORM DATA TO ENABLE TIME SERIES
    result = df.groupby([pd.Grouper(key='created_at', freq='2s'), 'polarity']).count().unstack(fill_value=0).stack().reset_index()
    #SETTING PARAMETERS
    result.loc[result['polarity'] < -0.1, 'polarity'] = -1
    result.loc[result['polarity'] > 0.1, 'polarity'] = 1
    result.loc[(-0.1 <= result['polarity']) & (result['polarity'] <= 0.1), 'polarity'] = 0

    result = result.rename(columns={"id_str": "Num of '{}' mentions".format('Ethereum'), "created_at": "Time in UTC"})
    time_series = result["Time in UTC"][result['polarity'] == 0].reset_index(drop=True)
    
    sentiment_figure.add_trace(go.Scatter(
        x=time_series,
        y=result["Num of 'Ethereum' mentions"][result['polarity'] == 0].reset_index(drop=True),
        name="Neutral",
        line=dict(color='rgb(0,143,211)'),
        opacity=0.8), row=1, col=1)

    sentiment_figure.add_trace(go.Scatter(
        x=time_series,
        y=result["Num of 'Ethereum' mentions"][result['polarity'] == -1].reset_index(drop=True),
        name="Negative",
        line=dict(color='rgb(255,127,0)'),
        opacity=0.8), row=1, col=1)

    sentiment_figure.add_trace(go.Scatter(
        x=time_series,
        y=result["Num of 'Ethereum' mentions"][result['polarity'] == 1].reset_index(drop=True),
        name="Positive",
        line=dict(color='rgb(0,211,202)'),
        opacity=0.8), row=1, col=1)
    
    ### ETHEREUM PRICE ###
    sentiment_figure.add_trace(
    go.Scatter(
        x=timestamps,
        y=ethereum_prices,
        name="Ethereum Price",
        line=dict(color='rgb(0,143,211)'),
        opacity=0.8),
        row=1, col=2)

    ## CLEANING & SEPERATING THE DATA ##
    content = clean_content(' '.join(df["text"]))
    filtered_sen = create_filtered_sen(content)
    fd = create_frequency_df(filtered_sen)

    negative_tweets = df[df['polarity'] < -0.1]
    negative_content = clean_content(' '.join(negative_tweets["text"]))
    negative_filtered_sen = create_filtered_sen(negative_content)
    negative_fd = create_frequency_df(negative_filtered_sen)

    positive_tweets = df[df['polarity'] > 0.1]
    positive_content = clean_content(' '.join(positive_tweets["text"]))
    positive_filtered_sen = create_filtered_sen(positive_content)
    positive_fd = create_frequency_df(positive_filtered_sen)
    ### ADDING TRACES FOR BAR GRAPH TO SUB-PLOTS ###
    sentiment_figure.add_trace(go.Bar(x=fd["Word"], y=fd["Frequency"], name="Freq Dist"), row=2, col=1)
    sentiment_figure.update_traces(marker_color='rgb(17,159,249)', marker_line_color='rgb(0,0,0)',
                    marker_line_width=0.5, opacity=0.7, row=2, col=1)

    sentiment_figure.add_trace(go.Bar(x=negative_fd["Word"], y=negative_fd["Frequency"], name="Negative Sentiment Top Words"), row=3, col=1)
    sentiment_figure.update_traces(marker_color='rgb(255,127,0)', marker_line_color='rgb(0,0,0)', marker_line_width=0.5, opacity=0.7, row=3, col=1)

    sentiment_figure.add_trace(go.Bar(x=positive_fd["Word"], y=positive_fd["Frequency"], name="Positive Sentiment Top Words"), row=4, col=1)
    sentiment_figure.update_traces(marker_color='rgb(0,211,202)', marker_line_color='rgb(0,0,0)', marker_line_width=0.5, opacity=0.7, row=4, col=1)
    
    ### UPDATING LAYOUT ###
    sentiment_figure.update_layout(height=2000, width=2000)

    sentiment_figure.update_xaxes(title_text="Time in UTC", row=1, col=1)
    sentiment_figure.update_yaxes(title_text="", row=1, col=1)

    sentiment_figure.update_xaxes(title_text="Time in UTC", row=1, col=2)
    sentiment_figure.update_yaxes(title_text="Ethereum Price in USD ($)", row=1, col=2)

    sentiment_figure.update_xaxes(title_text="Words", row=2, col=1)
    sentiment_figure.update_yaxes(title_text="Frequency", row=2, col=1)

    sentiment_figure.update_xaxes(title_text="Words", row=3, col=1)
    sentiment_figure.update_yaxes(title_text="Frequency", row=3, col=1)

    sentiment_figure.update_xaxes(title_text="Words", row=4, col=1)
    sentiment_figure.update_yaxes(title_text="Frequency", row=4, col=1)

    return sentiment_figure

if __name__ == '__main__':
    app.run_server(debug=True)
