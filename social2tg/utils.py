import logging
from importlib import import_module

import config


_LOGGER = None


def import_string(dotted_path):
    """
    Import provided string and return the object
    """
    module_path, class_name = dotted_path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, class_name)


def get_logger():
    """
    Setup logger and return its only instance
    """
    global _LOGGER

    if _LOGGER is None:

        log_format = f'%(asctime)s %(levelname)s: %(message)s'
        logging.basicConfig(format=log_format, level=logging.INFO)
        _LOGGER = logging.getLogger(__name__)

        if log_path := config.LOG_PATH:
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter(log_format))
            _LOGGER.addHandler(file_handler)

    return _LOGGER


def find_elem(soup, selector, index=0):
    """
    Find an element in the soup by the selector
    """
    if elements := soup.select(selector):
        return elements[index]
