import os
import sys

import numpy as np 
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    

def ticker_OnChange(ticker):
    st.write(ticker)


def ticker_dictionary():
    tickers = {
        "Amazon": "AMZN",
        "Google": "GOOGL",
        "Microsoft": "MSFT",
        "Nvidia": "NVDA",
        "Tesla": "TSLA",
        "Facebook": "FB",
        "Apple": "AAPL",
        "BlackRock": "BLK",
        "Dell": "DELL",
        "Chevron": "CVX",
    }
    return tickers



# Sample Data - Replace this with your actual DataFrame
df = pd.DataFrame({
    'Daily Return': [0.01, 0.02, -0.01, 0.03, -0.02, 0.04, -0.01, 0.02, -0.03, 0.05]
})

# Function to create the histogram and KDE plot
def plot_histogram_kde(data):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Histogram
    ax.hist(data["Daily Return"], bins=50, alpha=0.6, color="blue", density=True, label="Histogram")
    
    # KDE Plot (Kernel Density Estimate)
    sns.kdeplot(data["Daily Return"], ax=ax, color="red", label="KDE")

    ax.set_xlabel("Daily Return")
    ax.set_ylabel("Density")
    ax.set_title("Daily Return Distribution")
    ax.legend()

    plt.tight_layout()
    return(st.pyplot(fig))


def histogram_kde_string():
    return('''
    fig, ax = plt.subplots(figsize=(10, 6))

    # Histogram
    ax.hist(data["Daily Return"], bins=50, alpha=0.6, color="blue", density=True, label="Histogram")
    
    # KDE Plot (Kernel Density Estimate)
    sns.kdeplot(data["Daily Return"], ax=ax, color="red", label="KDE")

    ax.set_xlabel("Daily Return")
    ax.set_ylabel("Density")
    ax.set_title("Daily Return Distribution")
    ax.legend()
''')

