"""This module implements config manager for the system."""

import os
from configparser import ConfigParser, ExtendedInterpolation

from src.common.singleton import SingletonMeta
from src import BASE_DIR


CONF_FILE_NAME = "hrs.conf.ini"


# TODO: move all security related configs to .env file

class ConfigManager(metaclass=SingletonMeta):
    def __init__(self):
        conf_file_path = os.path.join(BASE_DIR, 'conf', CONF_FILE_NAME)
        self.__app_config = ConfigParser(interpolation=ExtendedInterpolation())
        self.__app_config.read(conf_file_path)

    def get_str(self, section, key, fallback=None):
        if fallback is None:
            return self.__app_config.get(section, key)
        else:
            return self.__app_config.get(section, key, fallback=fallback)

    def get_int(self, section, key, fallback=None):
        if fallback is None:
            return self.__app_config.getint(section, key)
        else:
            return self.__app_config.getint(section, key, fallback=fallback)

    def get_bool(self, section, key, fallback=None):
        if fallback is None:
            return self.__app_config.getboolean(section, key)
        else:
            return self.__app_config.getboolean(section, key, fallback=fallback)
