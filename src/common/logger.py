"""This module implements log handler for the system."""


import logging
import sys
import os
from datetime import datetime

from src.common.singleton import SingletonMeta
from src.common.config_manager import ConfigManager


LOG_FILE_PATH = ConfigManager().get_str('LOGGER', 'log_file_path')


def _initialize_log_directory():
    """Creates the log directory and all intermediate directories if not already existing."""
    if not os.path.exists(LOG_FILE_PATH):
        os.makedirs(LOG_FILE_PATH)


class LogHandler(metaclass=SingletonMeta):

    log_uniq_name = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
    log_file_name = os.path.join(LOG_FILE_PATH, "logs_" + log_uniq_name + ".log")
    log_level = ConfigManager().get_str('LOGGER', 'log_level', 'DEBUG')
    log_to_console = ConfigManager().get_bool('LOGGER', 'log_to_console', True)
    log_to_file = ConfigManager().get_bool('LOGGER', 'log_to_file', True)
    log_time_format = ConfigManager().get_str('LOGGER', 'log_time_format')
    log_format = ConfigManager().get_str('LOGGER', 'log_time_format',
                                         "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s")
    logger_name = ConfigManager().get_str('LOGGER', 'logger_name', 'HRS')

    def __init__(self):
        self.logger = logging.getLogger(self.logger_name)
        if not self.logger.handlers:
            self.logger.setLevel(self.log_level)
            formatter = logging.Formatter(self.log_format, datefmt=self.log_time_format)
            _initialize_log_directory()

            if self.log_to_file:
                self.file_handler = logging.FileHandler(self.log_file_name)
                self.file_handler.setFormatter(formatter)
                self.logger.addHandler(self.file_handler)

            if self.log_to_console:
                self.stream_handler = logging.StreamHandler(sys.stdout)
                self.stream_handler.setFormatter(formatter)
                self.logger.addHandler(self.stream_handler)

            self.logger.info(f"{type(self).__name__} module Initiated.")
