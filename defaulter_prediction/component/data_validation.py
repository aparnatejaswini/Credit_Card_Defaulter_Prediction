from defaulter_prediction.entity.entity_artifact import DataValidationArtifact, DataIngestionArtifact
from defaulter_prediction.entity.entity_config import DataValidationConfig, TrainingPipelineConfig
from defaulter_prediction.logger import logging
from defaulter_prediction.exception import Custom_Defaulter_Exception
from defaulter_prediction.util import read_yaml_file
from defaulter_prediction.constants import CURRENT_TIME_STAMP, ROOT_DIR, TRAINING_PIPELINE_ARTIFACT_DIR_KEY

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

import json
import pandas as pd
import sys
import os
import re
import shutil

class DataValidation():
    """
    This class shall be used for handling all the validations done on raw training data.
    It takes input from DataIngestionArtifact, DataValidationConfig , TrainingPipelineConfig

    - checks if source file path exists
    - validates file name
    - validates Number of columns
    - validates column names
    - validates domain values of categorical variables
    - Checks for data drift
    
    upon successful completion of all above validation checks, file will be moved to good data folder
    else file will be moved to bad data folder
    
    -generates data drift report file
    -generates data drift report page
    -returns DataValidationArtifact



    written by: Aparna T Parkala
    Version:1.0
    """
    def __init__(self, data_validation_config: DataValidationConfig, 
                    data_ingestion_artifact: DataIngestionArtifact, 
                    train_pipeline_config: TrainingPipelineConfig) -> None:
        try:
            logging.info("{'='*20} Data Validation Started. {'='*20}")
            self.dv_config = data_validation_config
            self.di_artifact = data_ingestion_artifact
            self.tp_config = train_pipeline_config
            self.Data_Imbalance = False

        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)

    def check_if_train_test_file_exists(self, )->bool:
        """
        This method checks for presence of train and test files.
        If available, returns a boolean value, else raises exception
        """
        try:
            logging.info("Checking if train and test files exists....")
            is_train_exists = False
            is_test_exists = False

            train_file_path = self.di_artifact.train_file_path
            test_file_path = self.di_artifact.test_file_path

            is_train_exists = os.path.exists(train_file_path)
            is_test_exists = os.path.exists(test_file_path)
            
            is_available = is_train_exists and is_test_exists
            
            if is_available:
                msg = f"Train file at [{train_file_path}] and Test file at [{test_file_path}] are available."
                logging.info(msg)
            else:
                msg = f"Train file at [{train_file_path}] and Test file at [{test_file_path}] are not available."
                logging.info(msg)                

            return is_available

        except Exception as e:
            raise Custom_Defaulter_Exception(e,sys)

    def save_train_test_df(self, )->(pd.DataFrame):
        """
        returns train and test data frames
        """
        try:
            train_df = pd.read_csv(self.di_artifact.train_file_path)
            test_df = pd.read_csv(self.di_artifact.test_file_path)
            return train_df, test_df
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)


    def validate_file_name(self) ->bool:
        """
        returns a boolean value.
        True indicates file name validated successfully.
        False indicates file name validation unsuccessful.
        """
        try:
            file_name_validated = False
            pattern = re.compile(r"^creditCard[A-Za-z]{5}\_\d{8}\_\d{6}\.csv")
            if pattern.match(os.path.basename(self.di_artifact.train_file_path)):
                logging.info("File Name Validated Successfully.")
                file_name_validated = True
            else:
                logging.ingfo("File Name format is not validated. Moving file to Bad data Folder")
            return file_name_validated
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)


    def validate_dataset_schema(self,)->bool:
        """
        This method checks if given file has similar schema as given to us by data owner.
        - checks for file_name pattern
        - checks Number of columns
        - checks column names
        - checks domain values of columns
        - checks for data imbalance
        """
        try:
            validation_status=False

            fname_validated = self.validate_file_name()
            
            logging.info("Reading Values from schema....")
            ##reading data schema file
            schema_config = read_yaml_file(self.dv_config.schema_file_path)

            #Validate fie name
            file_name_validated = self.validate_file_name()

            #Validate No.of Columns
            num_cols_validated = False
            train_df,_ = self.save_train_test_df()
            if train_df.shape[1] == schema_config['NoOfColumns']:
                num_cols_validated=True
                logging.info("Number of columns validated.")
            else:
                logging.info(f"Number of columns in file does not match with schema, moving file to bad data folder\n\
                                columns in schema {schema_config['NoOfColumns']}\n\
                                columns in file {train_df.shape[1]}")

            #Validate column names
            col_names_validated = False
            if list(train_df.columns) == list(schema_config['ColumnNames'].keys()):
                col_names_validated = True
                logging.info("Column names validated successfully.")
            else:
                logging.info("Column names do not match with schema file, moving file to bad data folder")
            
            #check domain values
            cat_col_domain_value_validated = set()
            for key in schema_config['categorical_columns'].keys():
                if set(train_df[key].unique()).issubset(set(schema_config['domain_values'][key].keys())):
                    cat_col_domain_value_validated.add(True)
                    logging.info(f"Domain values of key {key} is validated successfully.")
                else:
                    cat_col_domain_value_validated.add(False)
                    logging.info(f"Domain values of key {key} is not validated.\n\
                        Domain values of key {key} in schema file is {schema_config['domain_values'][key].keys()}\n\
                        Domain values of key {key} in given file is {train_df[key].unique()}\n\
                            Moving file to bad data folder")
            if False in cat_col_domain_value_validated:
                domain_val_validated = False
            else:
                domain_val_validated = True
            
            domain_val_validated=True
            validation_status = file_name_validated and num_cols_validated and col_names_validated and domain_val_validated

            return validation_status

        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)
        
    def move_file_to_bad_data_dir(self, ):
        """
        moves data to a bad data directory and exits program
        """
        try:
            bad_file_path = self.tp_config.archived_bad_data_path
            os.makedirs(bad_file_path, exist_ok=True)
            source = self.di_artifact.train_file_path
            shutil.move(source, bad_file_path)
            logging.info(f"File moved to bad data dir at: [{bad_file_path}]. Exiting program...")
            sys.exit("Data Validation unsuccessful. File Moved to bad data folder. See logs for more information.")
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)

    def move_file_to_good_data_dir(self,):
        """
        moves file to good data directory for further use
        """
        try:
            source = self.di_artifact.train_file_path
            dest = self.dv_config.good_data_path
            os.makedirs(dest, exist_ok=True)
            shutil.move(source, dest)
            logging.info(f"File moved to good data dir at: [{dest}].")
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)


    def get_and_save_data_drift_report(self,):
        """
        Generate and save data drift report 
        returns report
        """
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
        """
        generate and save data drift html page report with visualizations.
        """
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

    def is_data_drift_found(self,)->bool:
        """
        checks if data drift exists
        returns boolean value
        """
        try:
            logging.info("Checking for DataDrift..")
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            report_path = self.dv_config.report_file_path
            with open(report_path) as jobj:
                jdict = json.load(jobj)
            return jdict["data_drift"]["data"]["metrics"]['dataset_drift']
            
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)

    def initiate_data_validation(self,)->DataValidationArtifact:
        
        try:
            if self.check_if_train_test_file_exists():
                if self.validate_dataset_schema():
                    if self.is_data_drift_found():
                        logging.info("Data Validation unsuccessful. Data Drift Found.. Exiting program....")
                        sys.exit("Data Validation unsuccessful.. Data Drift detected. Exiting... See logs for more information.")
                    else:
                        logging.info("Data Drift not detected. Data Drift check completed successfully.")
                    logging.info("Data set validations completed successfully.")

                else:
                    logging.info("Data Validation failed, moving file to bad data folder")
                    self.move_file_to_bad_data_dir()
                

            else:
                msg = f" Exiting the program... "
                logging.info(msg)
                sys.exit("Data Validation unsuccessful. Train and test files not found. See logs for more information.")
            self.move_file_to_good_data_dir()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.dv_config.schema_file_path,
                report_file_path=self.dv_config.report_file_path,
                good_data_path=self.dv_config.good_data_path,
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
    

    