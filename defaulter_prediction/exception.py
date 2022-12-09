import os
import sys
import logging


class Custom_Defaulter_Exception(Exception):

    def __init__(self, error_msg:str, sys=sys) -> str:
        super().__init__(error_msg)
        self.error_msg = self.get_detailed_error_msg(error_msg, sys)

    def get_detailed_error_msg(self, error_msg:Exception, sys:sys)->Exception:
        """
        returns  error msg, line no, file name in which exception occured.
        """
        f_name = error_msg.__traceback__.tb_frame.f_code.co_filename
        line_num = error_msg.__traceback__.tb_lineno

        error_message = f"Error message: {error_msg} occured at line [{line_num}] in file: {f_name}\n"
        logging.info(f"{error_message}")
        return error_message

    def __repr__(self) -> str:
        return Custom_Defaulter_Exception.__name__()

    def __str__(self) -> str:
        return self.error_msg
