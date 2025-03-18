from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig
from NetworkSecurity.entity.config_entity import DataValidationConfig
from NetworkSecurity.entity.config_entity import ModelTrainerConfig
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.model_trainer import ModelTraier

from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.entity.config_entity import DataTransformationConfig

import sys
import os

if __name__ =="__main__":
    try:
        logging.info("Entering try block for testing data ingestion")
        training_PipelineConfig = TrainingPipelineConfig()

        data_IngestionConfig = DataIngestionConfig(training_PipelineConfig)
        data_ingestion = DataIngestion(data_IngestionConfig)
        logging.info("data ingestion initiate")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("data initiation ompletes")
        logging.info("initiate datavalidation")

        data_validation_config = DataValidationConfig(training_pipeline_config=training_PipelineConfig)
        data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("data validation done")
        #data transformation
        data_transformation_config = DataTransformationConfig(training_PipelineConfig)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config,data_validation_artifact=data_validation_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("data transformation completed")

        logging.info("MOdel training phase started")
        model_trainer_config = ModelTrainerConfig(training_pipeline_config=training_PipelineConfig)
        model_trainer = ModelTraier(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        print('------------')
        print(data_ingestion_artifact)
        print('-----------')
        print(data_validation_artifact)
        print('-----------')
        print(data_transformation_artifact)
        print('-----------')
        print(model_trainer_artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

