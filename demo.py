from defaulter_prediction.pipeline.pipeline import TrainPipeline
from defaulter_prediction.exception import Custom_Defaulter_Exception
import sys


def main():
    try:
        pipeline = TrainPipeline()
        pipeline.run_pipeline()
    except Exception as e:
        raise Custom_Defaulter_Exception(e, sys)
if __name__=="__main__":
    main()
