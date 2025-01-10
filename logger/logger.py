import logging
import functools
import os
from flask import request

def get_logger(name, log_file, level=logging.INFO):
    log_directory = os.path.join(os.path.dirname(__file__), "logs")

    os.makedirs(log_directory, exist_ok=True)

    log_file_path = os.path.join(log_directory, log_file)

    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        handler = logging.FileHandler(log_file_path, mode='w')
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)

    return logger


def log_function_call(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                json_data = request.get_json(silent=True)
                logger.info(f"Call of {func.__name__}()  args={args}, kwargs={kwargs}, json_data={json_data}")
                logger.debug(f"{func.__name__}() json_data={json_data}")
            except Exception as e:
                logger.error(f"Error in {func.__name__}(): {str(e)}")
                raise

        return wrapper
    return decorator