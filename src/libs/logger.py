from datetime import datetime
import logging
import os


class Console():


    def __init__(self, process_name):
        self.process_name = process_name
        log_level = os.environ.get("LOG_LEVEL", "INFO")
        custom_format = '%(asctime)s | %(levelname)-8s | %(module)s %(message)s'
        logging.basicConfig(level=log_level, format=custom_format)

    def get_datetime(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def critical(self, message):
        logging.critical(f"{self.process_name} - {message}")

    def error(self, message):
        logging.error( f"{self.process_name} - {message}")

    def warning(self, message):
        logging.warning(f"{self.process_name} - {message}")

    def info(self, message):
        logging.info( f"{self.process_name} - {message}")

    def debug(self, message):
        logging.debug( f"{self.process_name} - {message}")
