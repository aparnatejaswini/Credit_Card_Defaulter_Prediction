import os
import sys
import logging


class Defaulter_Exception(Exception):

    def __init__(self, error_msg:str, sys=sys) -> None:
        super().__init__(error_msg)
        return self.get_detailed_error_msg(error_msg, sys)

    def get_detailed_error_msg(error_msg:Exception, sys:sys)->Exception:
        """
        returns  error msg, line no, file name in which exception occured.
        """
        f_name = error_msg.__traceback__.tb_frame.f_code.co_filename
        line_num = error_msg.__traceback__.tb_lineno

        error_message = f"Error message: {error_msg} occured at line [{line_num}] in file: {f_name}\n"

        return error_message

    def __repr__(self) -> str:
        return Defaulter_Exception.__name__()

    def __str__(self) -> str:
        return self.error_msg
