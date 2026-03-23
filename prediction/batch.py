from src.constants import *
import os, sys
from src.logger import logging
from src.exception import CustomException
from src.config.configuration import *
from dataclasses import dataclass
import pandas as pd
import numpy as np
import pickle
from sklearn.pipeline import Pipeline
PREDICTION_FOLDER="batch_prediction"
PREDICTION_CSV="predictions_csv"
PREDICTION_FILE="predictions.csv"
FEATURE_ENGG_DIR="feature_engg"
ROOT_DIR=os.getcwd()
PREDICTION_DIR=os.path.join(ROOT_DIR,PREDICTION_FOLDER,PREDICTION_CSV)
FEATURE_ENG=os.path.join(ROOT_DIR,PREDICTION_FOLDER,FEATURE_ENGG_DIR)

class batch_prediction:
    def __init__(self,input_file_path,model_file_path,transformer_file_path,feature_engineering_file_path)->None:
        self.input_file_path=input_file_path
        self.model_file_path=model_file_path
        self.transformer_file_path=transformer_file_path
        self.feature_engineering_file_path=feature_engineering_file_path
    def start_batch_prediction(self):
        try:
            with open(self.feature_engineering_file_path,"rb") as f:
                feature_engineering=pickle.load(f)
            with open(self.transformer_file_path,"rb") as f:
                transformer=pickle.load(f)
            with open(self.model_file_path,"rb") as f:
                model=pickle.load(f)
            feature_engg_pipeline=Pipeline(steps=[("feature_engineering",feature_engineering)])
            df=pd.read_csv(self.input_file_path)
            feature_engg_data=feature_engg_pipeline.fit_transform(df)
            transformed_data=transformer.transform(feature_engg_data)
            predictions=model.predict(transformed_data)
            df["predictions"]=predictions   
            os.makedirs(PREDICTION_DIR,exist_ok=True)
            df.to_csv(os.path.join(PREDICTION_DIR,PREDICTION_FILE),index=False)
        except Exception as e:
            raise CustomException(e,sys)
# if __name__=="__main__":

            

        