import logging
import os
from defaulter_prediction.constants import CURRENT_TIME_STAMP

def get_log_file_name()->str:
    return f"log_{CURRENT_TIME_STAMP}.log"

LOG_FILE_NAME = get_log_file_name()
LOG_DIR = "Logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)
FORMAT = '[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s'


logging.basicConfig(filename=LOG_FILE_PATH,
                    filemode="w",
                    level=logging.INFO,
                    format=FORMAT
                    )


