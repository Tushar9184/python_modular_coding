from src.constants import *
from src.config.configuration import *
import os, sys
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import pandas as pd
import numpy as np

from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
from src.utils import save_object, evaluate_model

@dataclass
class ModelTrainConfig:
    train_model_file_path: str = MODEL_TRAINER_DIR


class ModelTrain:
    def __init__(self):
        self.train_model = ModelTrainConfig()

    def model_train_initiate(self, train_arr, test_arr):
        try:
            models = {
                "RandomForest": RandomForestRegressor(),
                "DecisionTree": DecisionTreeRegressor(),
                "XGBoost": XGBRegressor(),
                "GradientBoosting": GradientBoostingRegressor(),
                "svr":SVR
            }

            y_train = train_arr["Time_taken(min)"]
            X_train = train_arr.drop("Time_taken(min)", axis=1)

            y_test = test_arr["Time_taken(min)"]
            X_test = test_arr.drop("Time_taken(min)", axis=1)

            report = evaluate_model(X_train, y_train, X_test, y_test, models)
            best_model_score = max(report.values())
            best_model_name = [k for k, v in report.items() if v == best_model_score][0]
            best_model = models[best_model_name]
            logging.info(f"Best model found on both training and testing dataset is {best_model_name} with r2 score {best_model_score}")
            save_object(file_path=self.train_model.train_model_file_path, obj=best_model)
            
        except Exception as e:
            raise CustomException(e, sys)