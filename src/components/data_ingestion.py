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


"""
This process is carried out on apple stock aapl
"""

@dataclass
class DataIngestionConfig:
    """
    The DataIngestionConfig class is used to specify the file path where the output of the data ingestion 
    process will be stored.
    """
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.data_path = os.path.join("artifacts", f"{ticker}.csv") 

    
    

class DataIngestion:
    """
    """
    def __init__(self, ticker:str):
        self.ticker = ticker
        self.ingestion_config = DataIngestionConfig(ticker=self.ticker)
        print(self.ticker)
        


    def initiate_data_ingestion(self):
        logging.info("Data Ingestion has started")
        try:
     
            sp500 = yf.Ticker(self.ticker)
            sp500 = sp500.history(period = "max")

            if sp500.empty:
                print("empty shii")
                raise TickerNotFoundError(self.ticker)
            
            logging.info("Index data for " + self.ticker +" acquired")
            print("Index data for " + self.ticker + " acquired")


            os.makedirs(os.path.dirname(self.ingestion_config.data_path),exist_ok=True)
            sp500.to_csv(self.ingestion_config.data_path,index=False,header=True)
            logging.info("Index data saved to csv")


            logging.info("Ingestion of the data is completed")
            print("Data Ingestion finished")

            return(
                self.ingestion_config.data_path
            )

        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    obj = DataIngestion("BALL")
    obj.initiate_data_ingestion()