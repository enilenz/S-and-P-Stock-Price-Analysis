"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np

def ticker_OnChange(ticker):
    st.write(ticker)

st.title("Stock Market Analysis")


#add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )

# Using "with" notation
st.sidebar.header("S&P500 Index")
with st.sidebar:
    # add_radio = st.radio(
    #     "Choose a shipping method",
    #     ("Standard (5-15 days)", "Express (2-5 days)")
    # )

    title = st.text_input("Search for your prefered ticker or select below", "")

    options = ["Amazon", "Google", "Microsoft", "Nvidia", "Tesla", "Facebook", ]
    selected_sector = st.sidebar.pills('Ticker', options,)
    

st.markdown("1. What was the change in price of the stock overtime?")
st.text("Reviewing the content of our data, we can see that the data is numeric and the date is the index of the data. Notice also that weekends are missing from the records.")

st.header("Descriptive Statistics about the Data")
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.line_chart(chart_data)