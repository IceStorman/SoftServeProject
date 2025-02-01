import logging
import functools
import os
from logging.handlers import RotatingFileHandler


class Logger:
    TRACE_LEVEL = 5
    _instance = None

    def __new__(cls, name, log_file, level=logging.INFO, max_size_mb=20, backup_count=1):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._init(name, log_file, level, max_size_mb, backup_count)
        return cls._instance

    def _init(self, name, log_file, level, max_size_mb, backup_count):
        self.name = name
        self.log_file = log_file
        self.level = level
        self.max_size = max_size_mb * 1024 * 1024
        self.backup_count = backup_count

        self.logger = self._create_logger()

    def _create_logger(self):
        log_directory = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(log_directory, exist_ok=True)
        log_file_path = os.path.join(log_directory, self.log_file)

        logger = logging.getLogger(self.name)

        if not logger.hasHandlers():
            handler = RotatingFileHandler(
                log_file_path,
                maxBytes=self.max_size,
                backupCount=self.backup_count
            )
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(self.level)

        return logger

    def log_function_call(self):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    self.trace(f"Call of {func.__name__}()  args={args}, kwargs={kwargs}")
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

    def trace(self, message):
        if self.logger.isEnabledFor(self.TRACE_LEVEL):
            self.logger._log(self.TRACE_LEVEL, message, ())