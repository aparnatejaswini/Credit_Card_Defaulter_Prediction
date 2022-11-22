from defaulter_prediction.component.data_ingestion import DataIngestion
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


    def run_pipeline(self, ):
        self.start_data_ingestion()