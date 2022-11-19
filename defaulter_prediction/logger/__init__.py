import logging
from defaulter_prediction.constants import CURRENT_TIME_STAMP

FORMAT = '[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s'

def get_file_name()->str:
    return f"log_{CURRENT_TIME_STAMP}"


logging.basicConfig(filename=get_file_name(),
                    filemode="W",
                    level=logging.INFO,
                    format=FORMAT,
                    )


