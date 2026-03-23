from src.constants import *
import os, sys
from src.logger import logging
from src.exception import CustomException
from src.config.configuration import *
from dataclasses import dataclass
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder,OrdinalEncoder
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from src.utils import save_object
class Feature_Engineering(BaseEstimator, TransformerMixin):
    def __init__(self):
        logging.info("Entered the feature engineering class")
        pass
    def distance_numpy(self, df,lat1, lon1, lat2, lon2):
        p=np.pi/180
        a=0.5-np.cos((df[lat2]-df[lat1])*p)/2 +np.cos(df[lat1]*p)*np.cos(df[lat2]*p)*(1-np.cos((df[lon2])))
        df["distance"]=12742*np.arccos(np.sqrt(a))

    
    def transform_data(self,df):
            logging.info("Entered the transform data method of feature engineering class")
            try:
                df.drop(["ID"],axis=1,inplace=True)
                self.distance_numpy(df,"Restaurant_latitude","Restaurant_longitude","Delivery_location_latitude","Delivery_location_longitude")
                df.drop(["Restaurant_latitude","Restaurant_longitude","Delivery_location_latitude","Delivery_location_longitude","Delivery_person_ID","Time_Orderd","Time_Order_picked"],axis=1,inplace=True)

                return df
            except Exception as e:
                raise CustomException(e,sys)
    def transform(self, X, y=None):
        logging.info("Entered the transform method of feature engineering class")
        try:
            transformed_data=self.transform_data(X)
            return transformed_data
            return transformed_data
        except Exception as e:
            raise CustomException(e,sys)         
@dataclass        
class DataTransformationConfig:
    preprocessor_obj_file_path=PREPROCESING_OBJ_FILE
    transformed_train_dir=TRANSFORMED_TRAIN_DIR
    transformed_test_dir=TRANSFORMED_TEST_DIR
    feature_engg_obj_file_path=FEATURE_ENGG_OBJ_FILE_PATH
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    def get_data_transformer_object(self):
        logging.info("Entered the get_data_transformer_object method of data transformation class")
        try:
            Road_traffic_density=["Low","Medium","High","jam"]
            Weather_conditions=["Fog","Stormy","Sandstorms","Windy","Cloudy","Sunny"]
            categorical_cols=["Type_of_vehicle","Type_of_order","Type_of_vehicle","Festival","City"]
            ordinal_cols=["Road_traffic_density","Weather_conditions"]
            numeric_cols=["distance","Vehicle_condition","multiple_deliveries"]
            numeric_pipeline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="constant",fill_value=0)),
                ("scaler",StandardScaler())
            ])
            categorical_pipeline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("onehotencoder",OneHotEncoder(handle_unknown="ignore")),
                ("scaler",StandardScaler(with_mean=False))
            ])
            ordinal_pipeline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),    
                ("ordinalencoder",OrdinalEncoder(categories=[Road_traffic_density,Weather_conditions])),
                ("scaler",StandardScaler(with_mean=False))  
            ])
            
            preprocessor=ColumnTransformer([
                ("numeric_pipeline",numeric_pipeline,numeric_cols),
                ("categorical_pipeline",categorical_pipeline,categorical_cols),
                ("ordinal_pipeline",ordinal_pipeline,ordinal_cols)
            ])
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
    def get_feature_engg_object(self):
        logging.info("Entered the get_feature_engg_object method of data transformation class")
        try:
            feature_engg=Pipeline(steps=[
                ("feature_engg",Feature_Engineering())
            ])
            return feature_engg
        except Exception as e:
            raise CustomException(e,sys)
    def initiate_data_transformation(self,train_path,test_path):
        logging.info("Entered the initiate_data_transformation method of data transformation class")
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("Read the train and test data completed")
            feature_engg_obj=self.get_feature_engg_object()
            preprocessor_obj=self.get_data_transformer_object()
            logging.info("Obtained the preprocessor and feature engineering object")
            feature_engg_obj.fit(train_df)
            transformed_train_df=feature_engg_obj.transform(train_df)
            transformed_test_df=feature_engg_obj.transform(test_df)
            transformed_train_df.to_csv("transformed_train_df.csv",index=False)
            transformed_test_df.to_csv("transformed_test_df.csv",index=False)
            logging.info("Applied feature engineering object on train and test data")
            target_col="Time_taken(min)"
            transformed_train_arr=preprocessor_obj.fit_transform(transformed_train_df.drop(target_col,axis=1))
            transformed_test_arr=preprocessor_obj.transform(transformed_test_df.drop(target_col,axis=1))
            transformed_train_arr=np.c_[transformed_train_arr,transformed_train_df[target_col].values]
            transformed_test_arr=np.c_[transformed_test_arr,transformed_test_df[target_col].values]
            transformed_train_arr=pd.DataFrame(transformed_train_arr)
            transformed_test_arr=pd.DataFrame(transformed_test_arr)
            logging.info("Applied preprocessor object on train and test data")
            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_train_dir),exist_ok=True)
            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_test_dir),exist_ok=True)
            transformed_train_arr.to_csv(self.data_transformation_config.transformed_train_dir,index=False)
            transformed_test_arr.to_csv(self.data_transformation_config.transformed_test_dir,index=False)
            save_object(file_path=self.data_transformation_config.preprocessor_obj_file_path,obj=preprocessor_obj)
            save_object(file_path=self.data_transformation_config.feature_engg_obj_file_path,obj=feature_engg_obj)
            logging.info("Saved the preprocessor and feature engineering object")
            return (transformed_train_arr,transformed_test_arr,self.data_transformation_config.preprocessor_obj_file_path)
        except Exception as e:
            raise CustomException(e,sys)