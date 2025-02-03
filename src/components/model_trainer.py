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

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score

@dataclass
class ModelTrainerConfig:
    model_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self, data_path):
        self.data_path = data_path
        pass

    def model_trainer(self):

        sp500 = pd.read_csv(self.data_path)
        logging.info("Data read successfully, Model Training Initiated")
        logging.info("Columns: " + str(sp500.columns))

        # Ensure Target is properly defined
        if "Target" not in sp500.columns:
            logging.error("Target column is missing from the dataset!")
            return


        model = RandomForestClassifier(n_estimators = 100, min_samples_split = 100, random_state = 1)

        # Split last 100 rows into test set and everything else into train.
        # Cross Validation is not used due to avoid data leakage
        train = sp500.iloc[:-100]
        test = sp500.iloc[-100:]

        
        # print(test["Target"].value_counts())
        # print(train["Target"].value_counts())

        predictors = ["Close", "Volume", "Open", "High", "Low"]
        model.fit(train[predictors], train["Target"])
        preds = model.predict(test[predictors])
        preds = pd.Series(preds, index = test.index)

        score = precision_score(test["Target"], preds)
        print("Precision score is " + str(score))
        logging.info("Precision score is " + str(score))




if __name__ == "__main__":
    ModelTrainer("artifacts/preprocessed/AAPL.csv").model_trainer()