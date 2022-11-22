from collections import namedtuple


TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", "pipeline_name\
                                                                artifact_dir")

DataIngestionConfig = namedtuple("DataIngestionConfig", "dataset_download_url\
                                                         dataset_download_dir\
                                                         ingested_data_dir\
                                                         train_dir\
                                                         test_dir"
                                )

DataValidationConfig = namedtuple("DataValidationConfig", "schema_file_path\
                                                            report_file_path\
                                                            report_page_file_path")

DataTransformationConfig = namedtuple("DataTransformationConfig", "")