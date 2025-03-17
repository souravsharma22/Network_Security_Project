from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from NetworkSecurity.entity.config_entity import DataValidationConfig
from NetworkSecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from NetworkSecurity.utils.main_utils.utils import read_yaml_file
from NetworkSecurity.utils.main_utils.utils import write_yaml_file

from scipy.stats import ks_2samp
import pandas as pd
import os 
import sys

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                data_validation_config:DataValidationArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def validate_no_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"required no of columns{number_of_columns}")
            logging.info(f"dataframe has no of columns{len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def detect_dataset_drift(self,base_df,current_df,theresold = 0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_sample_dist = ks_2samp(d1,d2)
                if theresold<=is_sample_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column:{
                    'p_value':float(is_sample_dist.pvalue),
                    'drift_status':is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            #creating direcctory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(drift_report_file_path,content=report)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            #reading data
            train_dataFrame = DataValidation.read_data(train_file_path)
            test_dataFrame = DataValidation.read_data(test_file_path)

            # validatin no of column
            status = self.validate_no_of_columns(train_dataFrame)
            if not status:
                error_msg = f"train dataset does not contains all the column\n"
            status1 = self.validate_no_of_columns(test_dataFrame)
            if not status1:
                error_msg = f"test data does not contains all the column\n"

            ## validating numerical columns


            ### checking data drift
            status = self.detect_dataset_drift(train_dataFrame,test_dataFrame)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataFrame.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_dataFrame.to_csv(self.data_validation_config.valid_test_file_path, index=False,header=False)
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)