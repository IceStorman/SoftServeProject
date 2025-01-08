import logging

def setup_logger(log_file="api_routes.log", level=logging.INFO):
    logging.basicConfig(
        filename=log_file,
        level=level,
        format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
    )