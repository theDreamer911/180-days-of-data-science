from bs4.element import SoupStrainer
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import streamlit as st
import seaborn as sns
from PIL import Image
import pandas as pd
import numpy as np
import requests
import base64
import json
import time

from streamlit.elements import image
from streamlit.elements.form import current_form_id

##########
# Page Layout
st.set_page_config(layout='wide')

########
# Title
image = Image.open('logo.png')

st.image(image, width=500)

st.title("Crypto Price App")

st.markdown("""
This app from CoinMarketCap Scrapping Method FreeCodeCamp - Data Professor
""")

# ----------
# About
expanded_bar = st.expander("About")
expanded_bar.markdown("""
Libraries: base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
""")

# -----------
# Page Layout (contd.)
col1 = st.sidebar
col2, col3 = st.columns((2, 1))

# -----------
# Sidebar  - Main Panel
col1.header('Input Options')

# Sidebar - Currency Price Unit
currency_price_unit = col1.selectbox(
    "Select currency for price", ('USD', 'BTH', 'ETH'))

# ------------


# @st.cache
def load_data():
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')

    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

    for i in listings:
        coins[str(i['id'])] = i['slug']

    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []

    for i in listings:
        coin_name.append(i['slug'])
        coin_symbol.append(i['symbol'])
        price.append(i['quote'][currency_price_unit]['price'])
        percent_change_1h.append(
            i['quote'][currency_price_unit]['percent_change_1h'])
        percent_change_24h.append(
            i['quote'][currency_price_unit]['percent_change_24h'])
        percent_change_7d.append(
            i['quote'][currency_price_unit]['percent_change_7d'])
        market_cap.append(i['quote'][currency_price_unit]['market_cap'])
        volume_24h.append(i['quote'][currency_price_unit]['volume_24h'])

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h',
                      'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h
    return df


df = load_data()

# Sidebar -cryptocurrency selection
sorted_coin = sorted(df['coin_symbol'])
selected_coin = col1.multiselect('Cryptcurrency', sorted_coin, sorted_coin)

df_selected_coin = df[(df['coin_symbol'].isin(selected_coin))]

# Sidebar  - Show off
num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

# Sidebar - Percent Timeframe
percent_timeframe = col1.selectbox(
    'Percent Change Time Frame', ['7d', '24h', '1h'])
percent_dict = {'7d': 'percent_change_7d',
                "24h": 'percent_change_24h', '1h': 'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

# Sidebar - Sorting Values
sort_values = col1.selectbox('Sort Values?', ['Yes', 'No'])

col2.subheader('Price Data of Selected Cryptocurrency')
col2.write("Data Dimensions: " + str(df_selected_coin.shape[0]) + ' rows and ' + str(
    df_selected_coin.shape[1]) + ' columns.')

col2.dataframe(df_coins)

# Download the CSV


def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv:base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href


col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

# Preparing data for Bar Plot of % price change
col2.subheader('Table of % Price Change')
df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h,
                      df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
col2.dataframe(df_change)

# Conditional creation of bar plot
col3.subheader("Bar Plot of % Price Change")

if percent_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_7d'])
    col3.write('*7 days period')
    plt.figure(figsize=(5, 25))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_7d'].plot(
        kind='barh', color=df_change.postive_percent_change_7d.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_24h'])
    col3.write('*24 hour period')
    plt.figure(figsize=(5, 25))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_24h'].plot(
        kind='barh', color=df_change.postive_percent_change_24h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_1h'])
    col3.write('*1 hour period')
    plt.figure(figsize=(5, 25))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_1h'].plot(
        kind='barh', color=df_change.postive_percent_change_1h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
