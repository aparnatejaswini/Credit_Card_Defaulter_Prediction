import os
from defaulter_prediction.constants  import train_pipeline


class TrainingPipelineConfig:
    def __init__(self):
        self.pipeline_name: str = train_pipeline.PIPELINE_NAME
        self.artifact_dir: str = os.path.join(train_pipeline.ARTIFACT_DIR, train_pipeline.CURRENT_TIME_STAMP)
        self.timestamp: str = train_pipeline.CURRENT_TIME_STAMP



class DataIngestionConfig:
        def __init__(self,train_pipeline_config:TrainingPipelineConfig):
            self.data_ingestion_dir: str = os.path.join(train_pipeline_config.artifact_dir, train_pipeline.DATA_INGESTION_DIR_NAME)
            self.downloaded_data_file_path: str = os.path.join(self.data_ingestion_dir, 
                                                             train_pipeline.DATA_INGESTION_DOWNLOADED_DATA_DIR
                                                             )
            self.training_file_path: str = os.path.join(self.data_ingestion_dir, 
                                                        train_pipeline.DATA_INGESTION_INGESTED_DIR, 
                                                        train_pipeline.TRAIN_FILE_NAME
                                                        )
            self.testing_file_path: str = os.path.join(self.data_ingestion_dir, 
                                                        train_pipeline.DATA_INGESTION_INGESTED_DIR, 
                                                        train_pipeline.TEST_FILE_NAME
                                                        )
            self.train_test_split_ratio: float = train_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
            #self.collection_name: str = train_pipeline.DATA_INGESTION_COLLECTION_NAME



class DataValidationConfig:
    def __init__(self,train_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join( train_pipeline_config.artifact_dir, train_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, train_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir, train_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, train_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, train_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, train_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, train_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path: str = os.path.join(self.data_validation_dir,
                                                        train_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                                                        train_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
                                                    )



class DataTransformationConfig:
    def __init__(self,train_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(train_pipeline_config.artifact_dir, train_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path: str = os.path.join(self.data_transformation_dir, 
                                                             train_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                             train_pipeline.TRAIN_FILE_NAME.replace("csv", "npy")
                                                            )
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,  
                                                            train_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                            train_pipeline.TEST_FILE_NAME.replace("csv", "npy"))
        self.transformed_object_file_path: str = os.path.join(self.data_transformation_dir, 
                                                              train_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                              train_pipeline.PREPROCSSING_OBJECT_FILE_NAME)



class ModelTrainerConfig:
    def __init__(self,train_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(train_pipeline_config.artifact_dir, train_pipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path: str = os.path.join(self.model_trainer_dir, 
                                                         train_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR, 
                                                         train_pipeline.MODEL_FILE_NAME
                                                        )
        self.expected_accuracy: float = train_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold = train_pipeline.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD


class ModelEvaluationConfig:
    def __init__(self,train_pipeline_config:TrainingPipelineConfig):
        self.model_evaluation_dir: str = os.path.join(train_pipeline_config.artifact_dir, train_pipeline.MODEL_EVALUATION_DIR_NAME)
        self.report_file_path = os.path.join(self.model_evaluation_dir,train_pipeline.MODEL_EVALUATION_REPORT_NAME)
        self.change_threshold = train_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE


class ModelDeployConfig:
    def __init__(self,train_pipeline_config:TrainingPipelineConfig):
        self.model_evaluation_dir: str = os.path.join(train_pipeline_config.artifact_dir, train_pipeline.MODEL_DEPLOY_DIR_NAME)
        self.model_file_path = os.path.join(self.model_evaluation_dir,train_pipeline.MODEL_FILE_NAME)
        self.saved_model_path=os.path.join(train_pipeline.SAVED_MODEL_DIR,
                                            f"{train_pipeline.CURRENT_TIME_STAMP}",
                                            train_pipeline.MODEL_FILE_NAME)