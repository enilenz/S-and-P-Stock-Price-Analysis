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


        title = st.text_input("Enter a stock ticker (e.g., AAPL):", "AAPL", placeholder="Search for a symbol", max_chars=4, )
        search = st.button("Search", type="primary")
        #st.caption(":red[Ticker not found]")

        options = ticker_dictionary().keys()
        selected_sector = st.sidebar.pills('Ticker', options, selection_mode="single", )

        if search and title:
            st.session_state["ticker"] = title
            obj = DataIngestion(st.session_state["ticker"])
            df = obj.initiate_data_ingestion()
            title = ""
            #st.session_state.data_frame = df
        elif selected_sector:
            st.session_state["ticker"] = ticker_dictionary().get(selected_sector)
            obj = DataIngestion(st.session_state["ticker"])
            df = obj.initiate_data_ingestion()
            selected_Sector = ""
            #st.session_state.data_frame = df

    st.title("Stock Market Analysis")
    
    #st.text("Select your prefered stock from the options in the side bar or search via the stock symbol")
    #st.text("Use this link to search")
    st.subheader("Here you go!")
    st.text("Find below the last 5 entries of the dataframe")
    #st.dataframe(df.tail())
    

    if st.button("Next", key="next_page_1", type="primary"):
        next_page()

# Page 2: Data Analysis
elif st.session_state.page == 2:
    st.title("")

    if "df" in st.session_state:
        df = st.session_state.df
        st.line_chart(df["Close"])  # Show closing price trend

    st.write("Additional analysis can go here...")

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
