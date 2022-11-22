from datetime import datetime
import os


ROOT_DIR = os.getcwd()
CONFIG_FILE = "file_path_config.yaml"
CONFIG_DIR = "config_input"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILE )
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"

#TRAINING PIPELINE VARIABLES
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY =   "pipeline_name"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY =  "artifact_dir"

#DATA INGESTION RELATE VARIABLES
DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
DATA_INGESTION_DATASET_DOWNLOAD_URL_KEY = "dataset_download_url"
DATA_INGESTION_DATASET_DOWNLOAD_DIR_KEY = "dataset_download_dir"
DATA_INGESTION_TRAIN_DIR_KEY = "train_dir"
DATA_INGESTION_TEST_DIR_KEY = "test_dir"