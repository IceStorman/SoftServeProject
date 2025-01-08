import logging
import functools
from flask import request


def get_logger(name, log_file, level=logging.INFO):
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        handler = logging.FileHandler(log_file)
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
                logger.info(f"Call of {func.__name__}() з args={args}, kwargs={kwargs}, json_data={json_data}")

                result = func(*args, **kwargs)

                logger.info(f"Result of {func.__name__}() = {result}")
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}(): {str(e)}")
                raise

        return wrapper
    return decorator