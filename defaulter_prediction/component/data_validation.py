from defaulter_prediction.entity.entity_artifact import DataValidationArtifact, DataIngestionArtifact
from defaulter_prediction.entity.entity_config import DataValidationConfig
from defaulter_prediction.logger import logging
from defaulter_prediction.exception import Custom_Defaulter_Exception

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

import json
import pandas as pd
import sys
import os

class DataValidation():

    def __init__(self, data_validation_config: DataValidationConfig, 
                    data_ingestion_artifact: DataIngestionArtifact) -> None:
        try:
            logging.info("{'='*20} Data Validation Started. {'='*20}")
            self.dv_config = data_validation_config
            self.di_artifact = data_ingestion_artifact

        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)

    def check_if_train_test_file_exists(self, )->bool:
        try:
            logging.info("Checking if train and test files exists....")
            is_train_exists = False
            is_test_exists = False

            train_file_path = self.di_artifact.train_file_path
            test_file_path = self.di_artifact.test_file_path

            is_train_exists = os.path.exists(train_file_path)
            is_test_exists = os.path.exists(test_file_path)
            
            is_available = is_train_exists and is_test_exists

            logging.info(f"Train and test files are available? --> {is_available}")

            if not is_available:
                msg = f"Train file at [{train_file_path}] and Test file at [{test_file_path}] are not available."
                logging.info(msg)
                raise Exception(msg)

            return is_available

        except Exception as e:
            raise Custom_Defaulter_Exception(e,sys)

    def save_train_test_df(self, ):
        """
        returns train_df and test_df
        """
        try:
            train_df = pd.read_csv(self.di_artifact.train_file_path)
            test_df = pd.read_csv(self.di_artifact.test_file_path)
            return train_df, test_df
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)

    def validate_dataset_schema(self,):
        try:
            validation_status=False
            #validate file name,
            #no.of columns
            #domain values
            #column names
            validation_status=True
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)
        

    def get_and_save_data_drift_report(self,):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df, test_df = self.save_train_test_df()
            profile.calculate(train_df, test_df)
            report = json.loads(profile.json())
            report_file_path = self.dv_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir, exist_ok=True)

            with open(report_file_path, "w") as report_file:
                json.dump(report, report_file, indent=6)
            return report
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)

    def save_data_drift_report_page(self,):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df, test_df = self.save_train_test_df()
            dashboard.calculate(train_df, test_df)

            report_page_file_path = self.dv_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir, exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)

    def is_data_drift_found(self,):
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)

    def initiate_data_validation(self,):
        try:
            self.check_if_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.dv_config.schema_file_path,
                report_file_path=self.dv_config.report_file_path,
                report_page_file_path=self.dv_config.report_page_file_path,
                is_validated=True,
                msg="Data Validation performed successully."
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise Custom_Defaulter_Exception(e,sys) from e


    def __del__(self):
        logging.info(f"{'=='*30}Data Valdaition log completed.{'=='*30} \n\n")
    

    