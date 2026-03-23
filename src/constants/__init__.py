import os,sys
from datetime import datetime

def get_current_time_stamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

CURRENT_TIME_STAMP = get_current_time_stamp()
ROOT_DIR_KEY=os.getcwd()
DATA_DIR="data"
DATA_DIR_KEY="raw.csv"

ARTIFACT_DIR_KEY="artifact"
DATA_INGESTION_KEY="data_ingestion"
DATA_INGESTION_RAW_DATA_DIR="raw_data_dir"
DATA_INGESTION_INGESTED_DATA_DIR_KEY="ingested_dir"
DATA_INGESTION_DIR_KEY=os.path.join(ARTIFACT_DIR_KEY,DATA_INGESTION_KEY)
RAW_DATA_DIR_KEY="r.csv"
TRAIN_DATA_DIR_KEY="train.csv"
TEST_DATA_DIR_KEY="test.csv"

#data transformation related variable 
DATA_TRANSFORMATION_ARTIFACT="data_transformation"
DATA_PREPROCCED_DIR="procceor"
DATA_TRANSFORMATION_PROCESSING_OBJ="processor.pkl"
DATA_TRANSFORMATION_DIR="transformation"
TRANSFORMED_TRAIN_DIR="train.csv"
TRANSFORMED_TEST_DIR="test.csv"

#model trainer related variable
MODEL_TRAINER_KEY="model_trainer" 
MODEL_OBJECT="model.pkl"
