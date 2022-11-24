from collections import namedtuple


TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", "pipeline_name\
                                                                archived_bad_data_path\
                                                                artifact_dir")

DataIngestionConfig = namedtuple("DataIngestionConfig", "dataset_download_url\
                                                         dataset_download_dir\
                                                         ingested_data_dir\
                                                         train_dir\
                                                         test_dir"
                                )

DataValidationConfig = namedtuple("DataValidationConfig", "schema_file_path\
                                                            good_data_path\
                                                            report_file_path\
                                                            report_page_file_path")

DataTransformationConfig = namedtuple("DataTransformationConfig", "transformed_train_dir\
                                                                    transformed_test_dir\
                                                                    preprocessed_object_file_path")