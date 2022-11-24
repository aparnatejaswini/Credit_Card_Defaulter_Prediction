from defaulter_prediction.component.data_ingestion import DataIngestion
from defaulter_prediction.component.data_validation import DataValidation
from defaulter_prediction.exception import Custom_Defaulter_Exception
from defaulter_prediction.logger import logging
from defaulter_prediction.entity.entity_config import DataIngestionConfig
from defaulter_prediction.entity.entity_artifact import DataIngestionArtifact
from defaulter_prediction.config.configuration import Configuration
from defaulter_prediction.constants import CONFIG_FILE_PATH, CURRENT_TIME_STAMP
import sys


class Pipeline():
    def __init__(self, conf:Configuration()) -> None:
        self.conf = Configuration(CONFIG_FILE_PATH, CURRENT_TIME_STAMP)

    def start_data_ingestion(self, ):
        try:
            logging.info("Starting data ingestion")
            di_conf = self.conf.get_data_ingestion_config()
            return DataIngestion(di_conf).initiate_data_ingestion()
        except Exception as e:
            raise Custom_Defaulter_Exception(e,sys)

    def start_data_validation(self, data_ingestion_artifact, tp_config):
        try:
            logging.info("Starting data_validation")
            dv_conf = self.conf.get_data_validation_config()
            return DataValidation(dv_conf, data_ingestion_artifact=data_ingestion_artifact, 
                                    train_pipeline_config=tp_config).initiate_data_validation()
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)


    def run_pipeline(self, ):
        logging.info(f"{'='*20} Training Pipeline Started {'='*20}")
        di_artifact = self.start_data_ingestion()
        tp_config = self.conf.get_training_pipeline_config()
        self.start_data_validation(di_artifact, tp_config)