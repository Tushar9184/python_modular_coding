import pandas as pd
import numpy as np
import os, sys
from src.logger import logging
from src.exception import CustomException
from src.config.configuration import *
from dataclasses import dataclass
from src.components.data_tranformation import DataTransformation
@dataclass
class DataIngestionConfig:
    train_data_dir: str = TRAIN_DATA_DIR
    test_data_dir: str = TEST_DATA_DIR
    raw_data_dir: str = RAW_DATA_DIR

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            data_path = DATASET_PATH
            df = pd.read_csv(data_path)

            from sklearn.model_selection import train_test_split
            train_data, test_data = train_test_split(
                df, test_size=0.25, random_state=42
            )

            # create directories
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_dir), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.train_data_dir), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.test_data_dir), exist_ok=True)

            # save data
            df.to_csv(self.data_ingestion_config.raw_data_dir, index=False)
            train_data.to_csv(self.data_ingestion_config.train_data_dir, index=False)
            test_data.to_csv(self.data_ingestion_config.test_data_dir, index=False)

            return (
                self.data_ingestion_config.train_data_dir,
                self.data_ingestion_config.test_data_dir
            )

        except Exception as e:
            raise CustomException(e, sys)
if __name__ == "__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    data_transformation=DataTransformation()
    train_arr,test_arr,preprocessor_path=data_transformation.initiate_data_transformation(train_data,test_data)