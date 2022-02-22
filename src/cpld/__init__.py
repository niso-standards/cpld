import tomli
import os
from types import SimpleNamespace
import logging


def recurse_namespaces(dictionary):
    """Utility function to recursively change dictionary to a nested SimpleNamespace object"""
    if isinstance(dictionary, dict):
        for k in dictionary.keys():
            dictionary[k] = recurse_namespaces(dictionary[k])
        
        return SimpleNamespace(**dictionary)
    else:
        return dictionary


FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(FILE_PATH, "config.toml")

with open(CONFIG_PATH, "rb") as f:
    config_dictionary = tomli.load(f)
    CONFIG = recurse_namespaces(config_dictionary)
    

handler = logging.FileHandler(filename=CONFIG.log.filename, encoding="utf-8")
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
if CONFIG.log.level == "DEBUG":
    handler.setLevel(logging.DEBUG)
