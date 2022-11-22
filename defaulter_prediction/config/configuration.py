from defaulter_prediction.constants import *
from defaulter_prediction.entity.entity_config import TrainingPipelineConfig, DataIngestionConfig
from defaulter_prediction.exception import Custom_Defaulter_Exception
from defaulter_prediction.logger import logging
from defaulter_prediction.util import read_yaml_file
import sys
import os


class Configuration():

    def __init__(self, config_file_path:str=CONFIG_FILE_PATH,
                         current_time_stamp:str=CURRENT_TIME_STAMP)-> None:
        try:
            self.config_info = read_yaml_file(file_path=CONFIG_FILE_PATH)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.current_time_stamp = CURRENT_TIME_STAMP

        except Exception as e:
            raise Custom_Defaulter_Exception(e,sys)

    def get_data_ingestion_config(self,)->DataIngestionConfig:
        """
        Initialize and return a data ingestion config entity.

        //this activity is recorded in logs.
        """
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_ingestion_artifact_dir = os.path.join(artifact_dir, 
                                                        DATA_INGESTION_ARTIFACT_DIR, 
                                                        self.current_time_stamp)

            data_ingestion_config_info = self.config_info[DATA_INGESTION_CONFIG_KEY]

            download_url = data_ingestion_config_info[DATA_INGESTION_DATASET_DOWNLOAD_URL_KEY]

            data_dir = os.path.join(data_ingestion_artifact_dir, 
                                    data_ingestion_config_info[DATA_INGESTION_DATASET_DOWNLOAD_DIR_KEY])

            train_dir = os.path.join(data_ingestion_artifact_dir, 
                                    data_ingestion_config_info[DATA_INGESTION_TRAIN_DIR_KEY])

            test_dir = os.path.join(data_ingestion_artifact_dir, 
                                    data_ingestion_config_info[DATA_INGESTION_TEST_DIR_KEY])
            
            Data_Ingestion_Config = DataIngestionConfig(dataset_download_url=download_url,
                                                        dataset_download_dir=data_dir,
                                                        train_dir=train_dir,
                                                        test_dir=test_dir)

            logging.info(f"Data Ingestion Config: {Data_Ingestion_Config}")
            return Data_Ingestion_Config

        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)



    def get_training_pipeline_config(self,)->TrainingPipelineConfig:
        """
        reads training pipeline config key and establishes artifact directory path 
        returns training pipeline config entity

        //this activity is recorded in logs.
        """
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            pipeline_name = training_pipeline_config[TRAINING_PIPELINE_NAME_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
                                        training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
                                        )
            Training_Pipeline_Config = TrainingPipelineConfig(pipeline_name=pipeline_name, artifact_dir=artifact_dir)
            logging.info(f"Training Pipeline Started: {Training_Pipeline_Config}")
            return Training_Pipeline_Config

        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)