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

if "stage" not in st.session_state:
    st.session_state.stage = None

ROLES = [None, "Requester", "Responder", "Admin"]

# SideBar Components
st.sidebar.header("S&P500 Index")
with st.sidebar:

    st.session_state["ticker"] = ""


    title = st.text_input("Search for your prefered ticker or select below", placeholder="Search for a symbol", max_chars=4, )
    search = st.button("Search", type="primary")
    #st.caption(":red[Ticker not found]")

    options = ticker_dictionary().keys()
    selected_sector = st.sidebar.pills('Ticker', options, selection_mode="single", )

    if search and title:
        st.session_state["ticker"] = title
        obj = DataIngestion(st.session_state["ticker"])
        df = obj.initiate_data_ingestion()
        title = ""
        st.session_state.data_frame = df
    elif selected_sector:
        st.session_state["ticker"] = ticker_dictionary().get(selected_sector)
        obj = DataIngestion(st.session_state["ticker"])
        df = obj.initiate_data_ingestion()
        selected_Sector = ""
        st.session_state.data_frame = df

  
#st.session_state


# Main Page   
st.title("Stock Market Analysis")

#st.markdown("1. What was the change in price of the stock overtime?")
#st.text("Reviewing the content of our data, we can see that the data is numeric and the date is the index of the data. Notice also that weekends are missing from the records.")

#st.header("Descriptive Statistics about the Data")
st.subheader("Here you go!")
st.text("Find below the last 5 entries of the dataframe")

st.dataframe(df.tail())
#chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
#st.line_chart(chart_data)
st.button("Next", type="primary")