import sys
import os 
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from NetworkSecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from NetworkSecurity.entity.config_entity import DataTransformationConfig
from NetworkSecurity.constant.training_pipeline import TARGET_COLUMN
from NetworkSecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            logging.info("data Transformation class function is created")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
    def get_data_transformer_object(cls)->Pipeline:
        try:
            '''returns a pipeline object for transforming data'''
            logging.info("ENtered in the data_transformer_object function")
            imputer:KNNImputer =KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Created KNNImputer with params {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor:Pipeline = Pipeline([('imputer',imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("The data transformation has been initiated")
            train_df  = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            #training dataFrame
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            #testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            ## Preprocessing n the data 
            preProcessor= self.get_data_transformer_object()
            preProcessor_obj = preProcessor.fit(input_feature_train_df)
            transformed_input_train_feature = preProcessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature = preProcessor_obj.transform(input_feature_test_df)
            logging.info("Preprocessing on the data has been done")

            train_arr = np.c_[ transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[ transformed_input_test_feature,np.array(target_feature_test_df)]

            logging.info("data is converted to arrays")

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preProcessor_obj)

            logging.info("datas have been saved as numpy array")

            data_transformation_artifact=  DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path= self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path= self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)