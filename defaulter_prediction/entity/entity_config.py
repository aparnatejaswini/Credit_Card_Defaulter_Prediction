from collections import namedtuple


TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", "pipeline_name\
                                                                artifact_dir")

DataIngestionConfig = namedtuple("DataIngestionConfig", "dataset_download_url\
                                                         dataset_download_dir\
                                                         train_dir\
                                                         test_dir"
                                )
