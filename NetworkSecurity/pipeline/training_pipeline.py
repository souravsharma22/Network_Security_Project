import os
import sys

from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.model_trainer import ModelTraier

from NetworkSecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact,
    ModelTrainerArtifact
)

from NetworkSecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig
)

class TrainingPipeline:
    #initializing the common required variable training config
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()


    #funaction for data ingestion
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Startin data ingestion")
            data_ingestion = DataIngestion(data_ingestion_congig=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion Completed{data_ingestion_artifact}")
            return data_ingestion_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    ## function for starting data validation
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
            logging.info("data validation artifact started")
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info("data validation is donr")
            return data_validation_artifact 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    ## function for starting data_transformation
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_transformation_config=data_transformation_config,data_validation_artifact=data_validation_artifact)
            logging.info("data transformation started")
            data_transforamtion_artifact = data_transformation.initiate_data_transformation()
            logging.info("data transformmationn is completed")
            return data_transforamtion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    ## function for starting model training
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTraier(data_transformation_artifact=data_transformation_artifact,model_trainer_config=model_trainer_config)
            logging.info("model TRaining has datarted")
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("Model training is done")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    ## function for running all of these
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
