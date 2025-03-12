import os
import sys
import io
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.components.data_ingestion import DataIngestion
from src.exception import CustomException
from src.exception import TickerNotFoundError
from src.logger import logging
from src.utils import ticker_dictionary
from src.utils import plot_histogram_kde
from src.utils import histogram_kde_string

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression 

df= None

if "df" not in st.session_state:
    st.session_state.df = None 
# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = 1  # Start on page 1

js = '''
<script>
    var body = window.parent.document.querySelector(".main");
    console.log(body);
    body.scrollTop = 0;
</script>
'''

# Function to switch pages
def next_page():
    st.session_state.page += 1
    st.components.v1.html(js)

def prev_page():
    st.session_state.page -= 1
    st.components.v1.html(js)

def back_to_start():
    st.session_state.page = 1 
    st.session_state.df = None 
    st.components.v1.html(js)



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
            st.session_state.df = obj.initiate_data_ingestion()  # Save df in session state
            title = ""
        elif selected_sector:
            st.session_state["ticker"] = ticker_dictionary().get(selected_sector)
            obj = DataIngestion(st.session_state["ticker"])
            st.session_state.df = obj.initiate_data_ingestion()
            selected_Sector = ""
            
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    st.title("Stock Market Analysis")
    st.text("The S&P 500 is a stock market index that measures the stock performance of 500 large companies listed on stock exchange in the United States.")

    


    if st.session_state.df is None:
        st.write("In this application, we will discover and explore data from the stock market  will also be predicting future stock prices through a ---- method!")
        st.write("We'll be answering the following questions along the way:")
        st.write("1.) What was the change in price of the stock over time?")
        st.write("2.) What was the moving average of the various stocks?") 
        st.write("3.) What was the daily return of the stock on average")
        #st.write("4.) How much value do we put at risk by investing in a particular stock?")
        st.write("4.) How can we attempt to predict future stock behavior?")
        st.write("")
        st.text("When you are ready to begin select your prefered stock from the options in the side bar or use the search bar")
        st.write("You can find the symbol of your choice on the S&P500 Wikipedia Page using this [link](%s) " % url)
    
    if st.session_state.df is not None:
        st.subheader("Here you go!")
        st.text("Find below the last 5 entries of the dataframe")
        st.dataframe(st.session_state.df.tail())
        st.write("Reviewing the content of our data, we can see that the data is numeric and the date is the index of the data. Notice also that weekends are missing from the records.")
        st.write("Here is some information about the columns in our dataframe")
        buffer = io.StringIO()
        st.session_state.df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)
        #st.write(df.info())
        if st.button("Next", key="next_page_1", type="primary"):
            next_page()

# Page 2: Data Analysis
elif st.session_state.page == 2:
    st.title("1.) What was the change in price of the stock over time?")

    if "df" in st.session_state:
        df = st.session_state.df
        #st.line_chart(df["Close"])  # Show closing price trend
    else:
        df = None

    st.write("The closing price is the last price at which the stock is traded during the regular trading day. A stock’s closing price is the standard benchmark used by investors to track its performance over time.")
    st.write("Let's see a historical view of the closing price:")
    st.line_chart(st.session_state.df["Close"])

    st.header("Volume of Sales")
    st.write("Volume is the amount of an asset or security that changes hands over some period of time, often over the course of a day. For instance, the stock trading volume would refer to the number of shares of security traded between its daily open and close. Trading volume, and changes to volume over the course of time, are important inputs for technical traders.")
    st.write("Now let's plot the total volume of stock being traded each day")
    st.line_chart(st.session_state.df["Volume"])
    st.write("Now that we've seen the visualizations for the closing price and the volume traded each day, let's go ahead and caculate the moving average for the stock.")

    if st.button("Previous", key="prev_page_2"):
        prev_page()

    if st.button("Next", key="next_page_2", type="primary"):
        next_page()

# Page 3: More Advanced Analysis
elif st.session_state.page == 3:
    st.title("2.) What was the daily return of the stock on average?")
    st.write("The moving average (MA) is a simple technical analysis tool that smooths out price data by creating a constantly updated average price. The average is taken over a specific period of time, like 10 days, 20 minutes, 30 weeks, or any time period the trader chooses.")
    st.write("For this stock we will be taking a 10, 20 and 50 day moving average period.")
    if "df" in st.session_state and st.session_state.df is not None:
        df = st.session_state.df.copy()  # Work on a copy to avoid state issues

        # Calculate Moving Averages
        ma_days = [10, 20, 50]
        ma_colors = {10: "red", 20: "green", 50: "blue"}
        for ma in ma_days:
            df[f"MA for {ma} days"] = df["Close"].rolling(ma).mean()

        # Save back to session state
        st.session_state.df = df  

        # Plot the Closing Price & Moving Averages
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df.index, df["Close"], label="Closing Price", color="yellow")
        for ma in ma_days:
            ax.plot(df.index, df[f"MA for {ma} days"], label=f"{ma}-Day MA", color=ma_colors[ma])

        # Formatting
        ax.set_title(f"{st.session_state.ticker} Closing Price & Moving Averages")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend()
        ax.grid(True)

        st.write(df.tail())
        st.write("Below is a graph to help notice any trends in the moving average of the stock")
        # Show the plot in Streamlit
        st.pyplot(fig)

        st.write("We see in the graph that the best values to measure the moving average are 10 and 20 days because we still capture trends in the data without noise.")

    else:
        st.write("No data available. Please select a stock first.")




    if st.button("Previous", key="prev_page_3"):
        prev_page()

    if st.button("Next", key="next_page_3", type="primary"):
        next_page()


# Page 4: More Advanced Analysis
elif st.session_state.page == 4:
    st.title("3.) What was the daily return of the stock on average?")
    st.write("Now that we've done some baseline analysis, let's go ahead and dive a little deeper. We're now going to analyze the risk of the stock. In order to do so we'll need to take a closer look at the daily changes of the stock, and not just its absolute value. Let's go ahead and use pandas to retrieve the daily returns for the stock")
    st.write(" We'll use pct_change to find the percent change for each day")

    code = '''df['Daily Return'] = df['Close'].pct_change()
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlabel("Year")
ax.set_ylabel("Percentage Change")
#ax.set_title("Daily Return Distribution")
ax.legend()
ax.plot(df['Daily Return'],  linestyle='--',)'''
    st.code(code)
    

    if "df" in st.session_state and st.session_state.df is not None:
        df = st.session_state.df.copy()  

        df['Daily Return'] = df['Close'].pct_change()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.set_xlabel("Year")
        ax.set_ylabel("Percentage Change")
        #ax.set_title("Daily Return Distribution")
        ax.legend()
        ax.plot(df['Daily Return'],  linestyle='--',)

        st.pyplot(fig)
        st.write("Great, now let's get an overall look at the average daily return using a histogram. We'll use seaborn to create both a histogram and kde plot on the same figure.")
        st.code(histogram_kde_string())
        plot_histogram_kde(df)

    if "df" in st.session_state:
        df = st.session_state.df
        #st.line_chart(df["Close"])  # Show closing price trend

    if st.button("Previous", key="prev_page_4"):
        prev_page()

    if st.button("Next", key="next_page_4", type="primary"):
        next_page()


# Page 3: More Advanced Analysis
elif st.session_state.page == 5:
    st.title("4.) How can we attempt to predict future stock behavior?")
    st.write("In this section we take a look at a step by step process involved in predicting the closing price of a stock.")
    st.write("Let's have another look at our stock data and deteremine the necessary features to make our predictions.")

    if "df" in st.session_state and st.session_state.df is not None:
        df = st.session_state.df.copy()  
        st.write(df.tail())
        st.header("Defining explanatory variables")
        st.write("An explanatory variable is a variable that is manipulated to determine the value of the stock price the next day. Simply, they are the features which we want to use to predict the closing prices. The explanatory variables in this strategy are the moving averages for past 10 days and 20 days.")
        st.write("We drop the NaN values using dropna() function and store the feature variables in X.")
        
        code = '''

        df= df.dropna() 
        X = df[['MA for 10 days','MA for 20 days']] 
        X.tail()
        '''
        st.code(code, )


        df= df.dropna() 
        X = df[['MA for 10 days','MA for 20 days']] 
        st.write(X.tail())

        # Save back to session state
        #st.session_state.df = df  
        #ticker value 
        ticker = st.session_state.ticker
        st.header("Define dependent  variables")
        st.write("Similarly, the dependent variable depends on the values of the explanatory variables. Simply put, it is the "+ ticker+" price which we are trying to predict. We store the " + ticker+"  price in y.")
        code ='''
        y = df['Close']
        y.tail()
        '''
        st.code(code,)

        y = df['Close']
        y.tail()
        st.write(y.tail())


        st.header("Splitting the data into training and testing dataset")
        st.write("In this step, we split the predictors and output data into train and test data. The training data is used to create the linear regression model, by pairing the input with expected output. The test data is used to estimate how well the model has been trained.")


        code = '''
        t=.8 
        t = int(t*len(df)) 
        # Train dataset 
        X_train = X[:t] 
        y_train = y[:t]  
        # Test dataset `
        X_test = X[t:] 
        y_test = y[t:]
        '''

        st.code(code,)

        t=.8 
        t = int(t*len(df)) 
        X_train = X[:t] 
        y_train = y[:t]  
        X_test = X[t:] 
        y_test = y[t:]

        linear = LinearRegression().fit(X_train,y_train)

        predicted_price = linear.predict(X_test)  
        predicted_price = pd.DataFrame(predicted_price, index=y_test.index, columns = ['price'])  
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(predicted_price)
        ax.plot(y_test)
        #predicted_price.plot(figsize=(10,5))  
        #y_test.plot()  
        ax.legend(['predicted_price','actual_price'])  
        ax.set_ylabel("AAPL Price")  
        st.pyplot(fig)













    if st.button("Previous", key="prev_page_5"):
        prev_page()

    if st.button("Next", key="next_page_5", type="primary"):
        next_page()


# Page 3: More Advanced Analysis
elif st.session_state.page == 6:
    st.title("Summary")
    st.write("In this application, we discovered and explored stock market data from the YAHOO Finance website using the yfinance API.")
    st.write("We visualized both the closing price of the stock and the volume traded in order to notice the dominant trends that occur overtime.")
    st.write("We calculated the stock's Moving Average in order to smooth out price fluctuations and potentially spot buy/sell opportunities")
    st.write("Using the close price of the stock we were able to build a simple Linear Regression model that was able to predict the closing price based on the stock's moving average.")


    if "df" in st.session_state:
        df = st.session_state.df
        #st.line_chart(df["Close"])  # Show closing price trend

    if st.button("Previous", key="prev_page_6"):
        prev_page()

    if st.button("Back to start", key="next_page_6", type="primary"):
        back_to_start()    
