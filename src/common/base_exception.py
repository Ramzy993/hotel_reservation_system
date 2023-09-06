"""This module implements the system base exception."""

import os
import sys


class HRSBaseException(Exception):
    def __init__(self, message):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        super().__init__(f"\n- Error type: {exc_type}.\n- Error in file: {file_name}, line: {exc_tb.tb_lineno}.\n"
                         f"- Message: {message}.")
