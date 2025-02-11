import streamlit as st
import yfinance as yf
import pandas as pd

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = 1  # Start on page 1

# Function to switch pages
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

# Page 1: Stock Data Loader
if st.session_state.page == 1:
    st.title("Stock Market Analysis")

    ticker = st.text_input("Enter a stock ticker (e.g., AAPL):", "AAPL")

    if st.button("Load Data"):
        stock = yf.Ticker(ticker)
        df = stock.history(period="1mo")  # Get last 1 month of data
        st.session_state.df = df  # Store in session state
        st.write(df)

    # Use a unique key for the button to prevent duplication issues
    if st.button("Next", key="next_page_1"):
        next_page()

# Page 2: Data Analysis
elif st.session_state.page == 2:
    st.title("Stock Data Analysis")

    if "df" in st.session_state:
        df = st.session_state.df
        st.line_chart(df["Close"])  # Show closing price trend

    st.write("Additional analysis can go here...")

    if st.button("Previous", key="prev_page_2"):
        prev_page()

    if st.button("Next", key="next_page_2"):
        next_page()

# Page 3: More Advanced Analysis
elif st.session_state.page == 3:
    st.title("Advanced Stock Analysis")
    st.write("Perform more advanced stock market analysis here...")

    if st.button("Previous", key="prev_page_3"):
        prev_page()
