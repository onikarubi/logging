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


    def info_message(self, msg: any) -> None:
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        self.logger.info(msg)

    def output_debug(self, dbg_msg: any) -> None:
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        self.logger.debug(dbg_msg)

    def error_output(self, msg):
        self.logger.setLevel(logging.ERROR)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        self.logger.error(msg)



