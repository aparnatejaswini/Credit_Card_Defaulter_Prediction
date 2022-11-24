from defaulter_prediction.logger import logging
from defaulter_prediction.exception import Custom_Defaulter_Exception
from defaulter_prediction.entity.entity_config import DataTransformationConfig
from defaulter_prediction.entity.entity_artifact import DataIngestionArtifact,DataValidationArtifact, DataTransformationArtifact

import sys


class DataTransformation():
    def __init__(self, config:DataTransformationConfig, 
                        di_artifact: DataIngestionArtifact, 
                            dv_artifact:DataValidationArtifact ):
        try:
            logging.info(f"{'='*20} Data Transformation log started. {'='*20}")
            self.config = config
            self.di_artifact = di_artifact
            self.di_artifact = di_artifact

        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)

    def __del__(self, ) -> None:
            logging.info(f"{'='*20} Data Transformation log completed successfully. {'='*20}")
