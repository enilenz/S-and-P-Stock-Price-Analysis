import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from exception import CustomException
from exception import TickerNotFoundError
from logger import logging

import yfinance as yf
import pandas as pd
from dataclasses import dataclass

import streamlit as st

@dataclass
class DataTransformationConfig:
    def __init__(self, ticker):
        self.ticker = ticker
        self.processed_data_path = os.path.join("artifacts/preprocessed", ticker) 


class DataTransformation:
     def __init__(self):
         pass
          #data_transformation_config = DataTransformationConfig()

    
     def initiate_data_transformation(self, data_path):
        """
        This function is responsible for removing null values and unnecessary columns
        """
        try:
            print(data_path)
            sp500 = pd.read_csv(data_path)
            print("The shape of our data is " + str(sp500.shape))

            logging.info("Data read successfully")
            logging.info("Columns: " + str(sp500.columns))

            # Delete unnecessary columns
            for i in list(sp500.columns):
                if i == 'Dividends':
                    del sp500['Dividends']
                    logging.info("Dividends deleted")                  
                if i == 'Stock Splits':
                    del sp500['Stock Splits']
                    logging.info("Stock Splits deleted")
            
            logging.info("Deleted Dividends and Stock Splits Columns")
            print(list(sp500.columns))

            # Create Tomorrow column
            sp500["Tomorrow"] = sp500["Close"].shift(-1)
            print(list(sp500.columns))

            sp500["Target"] = (sp500["Tomorrow"] > sp500["Close"]).astype(int)
            print(list(sp500.columns))

            logging.info("Created Target and Tomorrow Columns")
            logging.info("Removing Historical Data")

            # Removing hostorical data 
            sp500 = sp500.loc["1990-01-01":].copy()
            print("Columns include " + str(sp500.columns))
            print("The shape of our data is " + str(sp500.shape))
            logging.info("Columns: " + str(sp500.columns))

            # Setting the file path where the processed data is saved
            file_path = os.path.basename(data_path)
            data_transformation_path = DataTransformationConfig(file_path).processed_data_path

            os.makedirs(os.path.dirname(data_transformation_path),exist_ok=True)
            sp500.to_csv(data_transformation_path,index=False,header=True)

            logging.info("Data Transformation done and processed data saved")

            return(
                data_transformation_path
            )

        except:
            pass



if __name__ == "__main__":
    DataTransformation().initiate_data_transformation("artifacts/APO.csv")