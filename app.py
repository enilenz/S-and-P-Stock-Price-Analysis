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

def ticker_OnChange(ticker):
    st.write(ticker)

# SideBar Components
st.sidebar.header("S&P500 Index")
with st.sidebar:


    title = st.text_input("Search for your prefered ticker or select below", "", placeholder="Search for a symbol")

    options = ticker_dictionary().keys()
    selected_sector = st.sidebar.pills('Ticker', options, selection_mode="single")

    st.button("Search", type="primary")
    st.write(ticker_dictionary().get(selected_sector))

    #obj = DataIngestion(selected_sector)
    #obj.initiate_data_ingestion()


# Main Page   
st.title("Stock Market Analysis")

st.markdown("1. What was the change in price of the stock overtime?")
st.text("Reviewing the content of our data, we can see that the data is numeric and the date is the index of the data. Notice also that weekends are missing from the records.")

st.header("Descriptive Statistics about the Data")
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.line_chart(chart_data)
st.button("Next", type="primary")