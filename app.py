import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.components.data_ingestion import DataIngestion
from src.exception import CustomException
from src.exception import TickerNotFoundError
from src.logger import logging
from src.utils import ticker_dictionary

from src.pages import second_page

import streamlit as st
import pandas as pd
import numpy as np


df = None


# SideBar Components
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
        #title = ""
        #st.session_state.data_frame = df
    elif selected_sector:
        st.session_state["ticker"] = ticker_dictionary().get(selected_sector)
        obj = DataIngestion(st.session_state["ticker"])
        df = obj.initiate_data_ingestion()
        #selected_Sector = ""
        #st.session_state.data_frame = df

  
#st.session_state


# Main Page   
if st.session_state.stage == None:
    st.title("Stock Market Analysis")

    if df == None:
        st.text("Select your prefered stock from the options in the side bar or search via the stock symbol")
        st.text("Use this link to search")

    if df:
        st.subheader("Here you go!")
        st.text("Find below the last 5 entries of the dataframe")

        st.dataframe(df.tail())
    

st.button("Next", type="primary")

if st.button("Next") and st.session_state.stage == None:
    st.switch_page("second_page.py")
