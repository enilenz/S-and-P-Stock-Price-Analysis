import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.components.data_ingestion import DataIngestion
from src.exception import CustomException
from src.exception import TickerNotFoundError
from src.logger import logging
from src.utils import ticker_dictionary

import streamlit as st
import pandas as pd
import numpy as np

df = None

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = 1  # Start on page 1

# Function to switch pages
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

  

# Main Page   

if st.session_state.page == 1:

    st.sidebar.header("S&P500 Index")
    with st.sidebar:
        st.session_state["ticker"] = ""


        title = st.text_input("Enter a stock ticker (e.g., AAPL):", placeholder="Search for a symbol", max_chars=4, )
        search = st.button("Search", type="primary")
        #st.caption(":red[Ticker not found]")

        options = ticker_dictionary().keys()
        selected_sector = st.sidebar.pills('Ticker', options, selection_mode="single", )

        if search and title:
            st.session_state["ticker"] = title
            obj = DataIngestion(st.session_state["ticker"])
            df = obj.initiate_data_ingestion()
            st.session_state.df = df
            title = ""
            #st.session_state.data_frame = df
        elif selected_sector:
            st.session_state["ticker"] = ticker_dictionary().get(selected_sector)
            obj = DataIngestion(st.session_state["ticker"])
            df = obj.initiate_data_ingestion()
            st.session_state.df = df
            selected_Sector = ""
            #st.session_state.data_frame = df
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    st.title("Stock Market Analysis")
    st.text("The S&P 500 is a stock market index that measures the stock performance of 500 large companies listed on stock exchange in the United States.")

    


    if df is None:
        st.write("In this application, we will discover and explore data from the stock market  will also be predicting future stock prices through a ---- method!")
        st.write("We'll be answering the following questions along the way:")
        st.write("1.) What was the change in price of the stock over time?")
        st.write("2.) What was the daily return of the stock on average?")
        st.write("3.) What was the moving average of the various stocks?")
        st.write("4.) What was the correlation between different stocks'?")
        st.write("5.) How much value do we put at risk by investing in a particular stock?")
        st.write("6.) How can we attempt to predict future stock behavior?")
        st.write("")
        st.text("When you are ready to begin select your prefered stock from the options in the side bar or use the search bar")
        st.write("You can find the symbol of your choice on the S&P500 Wikipedia Page using this [link](%s) " % url)
    
    if df is not None:
        st.subheader("Here you go!")
        st.text("Find below the last 5 entries of the dataframe")
        st.dataframe(df.tail())
        st.write("Reviewing the content of our data, we can see that the data is numeric and the date is the index of the data. Notice also that weekends are missing from the records.")
        st.write("Here is some information about the columns in our dataframe")
        st.write(df.info())
        if st.button("Next", key="next_page_1", type="primary"):
            next_page()

# Page 2: Data Analysis
elif st.session_state.page == 2:
    st.title("1.) What was the change in price of the stock over time?")

    # if "df" in st.session_state:
    #     df = st.session_state.df
    #     st.line_chart(df["Close"])  # Show closing price trend

    st.write("The closing price is the last price at which the stock is traded during the regular trading day. A stock’s closing price is the standard benchmark used by investors to track its performance over time.")
    st.write("Let's see a historical view of the closing price")
    st.line_chart(df["Close"])

    st.header("Volume of Sales")
    st.write("Volume is the amount of an asset or security that changes hands over some period of time, often over the course of a day. For instance, the stock trading volume would refer to the number of shares of security traded between its daily open and close. Trading volume, and changes to volume over the course of time, are important inputs for technical traders.")
    st.write("Now let's plot the total volume of stock being traded each day")
    st.line_chart(df["Volume"])

    if st.button("Previous", key="prev_page_2"):
        prev_page()

    if st.button("Next", key="next_page_2", type="primary"):
        next_page()

# Page 3: More Advanced Analysis
elif st.session_state.page == 3:
    st.title("Advanced Stock Analysis")
    st.write("Perform more advanced stock market analysis here...")

    if st.button("Previous", key="prev_page_3"):
        prev_page()
