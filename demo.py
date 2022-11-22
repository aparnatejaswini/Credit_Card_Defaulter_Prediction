from defaulter_prediction.pipeline.pipeline import Pipeline
from defaulter_prediction.config.configuration import Configuration
from defaulter_prediction.constants import CONFIG_FILE_PATH, CURRENT_TIME_STAMP
from defaulter_prediction.exception import Custom_Defaulter_Exception
import sys


def main():
    try:
        pipeline = Pipeline(Configuration(config_file_path=CONFIG_FILE_PATH,current_time_stamp=CURRENT_TIME_STAMP))
        pipeline.run_pipeline()
    except Exception as e:
        raise Custom_Defaulter_Exception(e, sys)
if __name__=="__main__":
    main()
