import logging
import functools
import os
from flask import request
from logging.handlers import RotatingFileHandler
class Logger:
    def __init__(self, name, log_file, level=logging.INFO, max_size_mb=20):
        self.name = name
        self.log_file = log_file
        self.level = level
        self.max_size = max_size_mb * 1024 * 1024
        self.logger = self._create_logger()

    def _create_logger(self):
        log_directory = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(log_directory, exist_ok=True)
        log_file_path = os.path.join(log_directory, self.log_file)

        logger = logging.getLogger(self.name)

        if not logger.hasHandlers():
            handler = logging.FileHandler(log_file_path, mode='a')
            handler.addFilter(self.SizeFilter(log_file_path, self.max_size))
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(self.level)

        return logger

    class SizeFilter(logging.Filter):
        def __init__(self, log_file_path, max_size):
            self.log_file_path = log_file_path
            self.max_size = max_size

        def filter(self, record):
            if os.path.exists(self.log_file_path):
                if os.path.getsize(self.log_file_path) >= self.max_size:
                    os.remove(self.log_file_path)
            return True

    def log_function_call(self):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    self.logger.info(f"Call of {func.__name__}()  args={args}, kwargs={kwargs}")
                    return func(*args, **kwargs)
                except Exception as e:
                    self.logger.error(f"Error in {func.__name__}(): {str(e)}")
                    raise
            return wrapper
        return decorator

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
