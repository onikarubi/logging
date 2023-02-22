import logging
import os

class EmailSendLogger:
    def __init__(self, filename) -> None:
        self.file_path = os.path.join("logs", f'{filename}.log')
        self.file_handler = logging.FileHandler(self.file_path)
        self.console_handler = logging.StreamHandler()
        self.format = logging.Formatter('%(levelname)s: %(message)s')
        self.file_handler.setFormatter(self.format)
        self.console_handler.setFormatter(self.format)
        self.logger = logging.getLogger(__name__)


    def info_message(self, msg: str):
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        self.logger.info(msg)




