from defaulter_prediction.entity.entity_config import DataIngestionConfig
from defaulter_prediction.entity.entity_artifact import DataIngestionArtifact
from defaulter_prediction.exception import Custom_Defaulter_Exception
from defaulter_prediction.logger import logging
from defaulter_prediction.util import read_yaml_file
from defaulter_prediction.constants.train_pipeline import SCHEMA_FILE_PATH, FILE_DOWNLOAD_URL, FILE_NAME

from sklearn.model_selection import StratifiedShuffleSplit
from six.moves import urllib
import pandas as pd
import sys
import os



class DataIngestion:
    """
    This class shall be used for 
    - Obtaining the data from source. 
    - Drop columns mentioned in schema file 
    - To split data as train and test sets for training.

    written by: Aparna T Parkala
    Version:1.0

    """
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise Custom_Defaulter_Exception(e,sys)

    def download_data(self,)->str:
        try:
            """
            This method obtains data from FILE_URL mentioned in constants/train_pipeline.py
            returns saved data file path.
            """
            download_dir_path = self.data_ingestion_config.downloaded_data_file_path

            os.makedirs(download_dir_path, exist_ok=True)
            logging.info(f"Downloading file from [{FILE_DOWNLOAD_URL}] to [{download_dir_path}]")
            urllib.request.urlretrieve(FILE_DOWNLOAD_URL, os.path.join(download_dir_path, FILE_NAME))
            logging.info(f"File downloaded Successfully")

        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)      


    def split_data_as_train_test(self, ) -> None:
        """
            This method accesses downloaded data, drops columns mentioned in data schema file and splits data file into train and test sets.
            Uses stratified shuffle split based on the problem statement.
            returns DataIngestionArtifact tuple which contains train and test file paths
        """

        try:
            #read file as a dataframe
            data_file_path = os.path.join(self.data_ingestion_config.downloaded_data_file_path, FILE_NAME)
            logging.info(f"Reading excel file:: {data_file_path}")
            dataframe = pd.read_excel(data_file_path, header=1)
            

            #drop unnecessary columns
            logging.info(f"Dropping unnecessary columns mentioned in {self._schema_config}")
            dataframe = dataframe.drop(self._schema_config["drop_columns"],axis=1)

            
            #split dataframe into train an test files
            logging.info("Splitting data into train and test sets")
            split = StratifiedShuffleSplit(n_splits=1, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=33)
            strat_train_set = None
            strat_test_set = None
            for train_idx, test_idx in split.split(dataframe, dataframe.iloc[:,-1]):
                strat_train_set = dataframe.loc[train_idx]
                strat_test_set = dataframe.loc[test_idx]
            

            logging.info("Performed Stratified Shuffle split on the dataframe")


            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path.")
            strat_train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            strat_test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info(f"Exported train and test file path.")

        except Exception as e:
            raise Custom_Defaulter_Exception(e,sys)
    

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.download_data()
            self.split_data_as_train_test()
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,
                                                                test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise Custom_Defaulter_Exception(e,sys)

