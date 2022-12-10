import os
from datetime import datetime


SAVED_MODEL_DIR =os.path.join("saved_models")
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# defining common constant variable for training pipeline
TARGET_COLUMN = "default payment next month"
PIPELINE_NAME: str = "cc_defaulter_prediction"
ARTIFACT_DIR: str = "artifact"
FILE_DOWNLOAD_URL: str = "https://archive.ics.uci.edu/ml/machine-learning-databases/00350/default%20of%20credit%20card%20clients.xls"
FILE_NAME = f'CreditCardFraud_{CURRENT_TIME_STAMP}.csv'

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
MODEL_FILE_NAME = "model.pkl"
SCHEMA_FILE_PATH = os.path.join("config_input", "schema_file_path.yaml")
SCHEMA_DROP_COLS = "drop_columns"


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "cc_default"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_DOWNLOADED_DATA_DIR: str = "downloaded_data"
DATA_INGESTION_INGESTED_DIR: str = "ingested_data"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.3

"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated_data"
DATA_VALIDATION_INVALID_DIR: str = "invalid_data"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "data_drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

"""
Data Transformation ralated constant start with DATA_TRANSFORMATION VAR NAME
"""

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed_data"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

"""
Model Trainer ralated constant start with MODE TRAINER VAR NAME
"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.05


"""
Model Evaluation ralated constant start with MODE EVALUATION VAR NAME
"""
MODEL_EVALUATION_DIR_NAME: str = "model_evaluation"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_EVALUATION_REPORT_NAME= "report.yaml"


"""
Model Deploy related constants
"""
MODEL_DEPLOY_DIR_NAME = "model_deploy"
MODEL_DEPLOY_SAVED_MODEL_DIR = SAVED_MODEL_DIR