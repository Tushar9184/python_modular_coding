import os,sys
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_tranformation import DataTransformation,DataTransformationConfig
from src.components.model_training import ModelTrain
class Train:
    def __init__(self):
        self.c=0
    def main(self):
        try:
            data_ingestion=DataIngestion()
            train_data,test_data=data_ingestion.initiate_data_ingestion()   
            data_transformation=DataTransformation()
            train_arr,test_arr,preprocessor_path=data_transformation.initiate_data_transformation(train_data,test_data)
            model_train=ModelTrain()
            model_train.model_train_initiate(train_arr,test_arr)
        except Exception as e:
            raise CustomException(e,sys)
        