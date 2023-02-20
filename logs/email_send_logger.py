import logging

class EmailSendLogger:
    def __init__(self, filename) -> None:
        self.file_path = f"logs/{filename}.log"
        self.basic_level = logging.INFO
        self.format = '%(levelname)s: %(message)s'
        self.logger = logging.getLogger(__name__)

        logging.basicConfig(filename=f'{self.file_path}', level=self.basic_level, format=self.format)

    def info_message(self, msg: str):
        self.logger.setLevel(logging.INFO)
        self.logger.info(msg)




