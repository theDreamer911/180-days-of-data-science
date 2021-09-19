import streamlit as st
import yfinance as yf
import pandas as pd

st.write("""
#Simple Stock Price App

Build with streamlit, this show **closing price** and **volume price** of AAPL stock

""")

tickerSymbol = 'AAPL'

tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period='1d', start='2011-1-1', end='2021-1-1')

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
