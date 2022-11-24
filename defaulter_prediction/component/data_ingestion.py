from defaulter_prediction.entity.entity_config import DataIngestionConfig
from defaulter_prediction.entity.entity_artifact import DataIngestionArtifact
from defaulter_prediction.exception import Custom_Defaulter_Exception
from defaulter_prediction.logger import logging
from defaulter_prediction.constants import CURRENT_TIME_STAMP
#from zipfile import ZipFile
#import tarfile

from sklearn.model_selection import StratifiedShuffleSplit
from six.moves import urllib
import pandas as pd
import sys
import os


class DataIngestion():

    """
    This class shall be used for 
    - Obtaining the data from source. 
    - To split data as train and test sets for training.

    written by: Aparna T Parkala
    Version:1.0

    """
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20} Data Ingestion log Started {'='*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)

    
    def download_data(self,)->str:
        try:
            """
            This method obtains data from web url mentioned in file 'file_path_config.yaml'
            returns saved data file path.
            """
            di_config = self.data_ingestion_config
            download_url= di_config.dataset_download_url
            download_dir = di_config.dataset_download_dir
            saved_dir_path = os.path.join(download_dir, 
                                            "CreditCard.xls")
            os.makedirs(download_dir, exist_ok=True)
            logging.info(f"Downloading file from [{download_url}] to [{saved_dir_path}]")
            urllib.request.urlretrieve(download_url, saved_dir_path)
            logging.info(f"File downloaded Successfully")
            return saved_dir_path
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)      

    """
    def extract_zip_data(self, zip_path:str)->str:
        try:
            di_config=self.data_ingestion_config
            extracted_data_dir = di_config.extracted_data_dir
            os.makedirs(extracted_data_dir, exist_ok=True)
            with ZipFile(zip_path) as zipObj:
                zipObj.extractall(path=extracted_data_dir)
            logging.info(f"Data extracted from {zip_path} to {extracted_data_dir}")

        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys) 

    def extract_tgz_file(self, path:str)->str:
        try:
            di_config=self.data_ingestion_config
            extracted_data_dir = di_config.extracted_data_dir
            os.makedirs(extracted_data_dir, exist_ok=True)
            with tarfile.open(path) as zipObj:
                zipObj.extractall(path=extracted_data_dir)
            logging.info(f"Data extracted from {path} to {extracted_data_dir}")

        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys) 
    """     


    def split_data_as_train_test_data(self,)->DataIngestionArtifact:
        """
        This method accesses downloaded data and splits data file into train and test sets.
        Uses stratified shuffle split based on the problem statement.
        returns DataIngestionArtifact tuple which contains train and test file paths
        """
        try:
            di_config = self.data_ingestion_config
            data_dir = di_config.dataset_download_dir
            data_file_name = os.listdir(data_dir)[0]
            data_file_path = os.path.join(data_dir, data_file_name)
            logging.info(f"Reading excel file:: {data_file_path}")
            df = pd.read_excel(data_file_path, header=1)
            logging.info("Splitting data into train and test sets")

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=33)
            strat_train_set = None
            strat_test_set = None
            for train_idx, test_idx in split.split(df, df.iloc[:,-1]):
                strat_train_set = df.loc[train_idx]
                strat_test_set = df.loc[test_idx]

            train_file_path = os.path.join(di_config.train_dir, f"creditCardTrain_{CURRENT_TIME_STAMP}.csv")
            test_file_path = os.path.join(di_config.test_dir, f"creditCardfTest_{CURRENT_TIME_STAMP}.csv")
            

            if strat_train_set is not None:
                os.makedirs(di_config.train_dir, exist_ok=True)
                logging.info(f"Writing train data : [{train_file_path}]")
                strat_train_set.to_csv(train_file_path, index=False)

            if strat_test_set is not None:
                os.makedirs(di_config.test_dir, exist_ok=True)
                logging.info(f"Writing test data: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested=True,
                                                            msg="Data Ingestion completed.")

            logging.info(f"Data Ingestion artifact : {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)


    def initiate_data_ingestion(self,):
        """
        calls download_data() and split_data_as_train_test_data()
        returns DataIngestionArtifact named tuple
        """
        try:
            self.download_data()
            return self.split_data_as_train_test_data()
        except Exception as e:
            raise Custom_Defaulter_Exception(e, sys)

    def __del__(self,):
        logging.info(f"{'='*20} Data Ingestion log completed successfully. {'='*20}")