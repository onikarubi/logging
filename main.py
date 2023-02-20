from emails.file_manager import FileManager
from emails.send_email import EmailManager
# from logs.email_send_logger import EmailSendLogger
from dotenv import load_dotenv
import os


if __name__ == '__main__':
    load_dotenv('./.env')
    username = os.getenv('user')
    password = os.getenv('pass')
    to_email = os.getenv('to_email')
    from_email = f'{username}@gmail.com'

    send_message_file = FileManager('./emails/msg.txt')
    msg = send_message_file.read_file()

    gmail_manager = EmailManager(username, password)
    field_transfer = gmail_manager.field_transfer(msg, from_email, to_email)
    gmail_manager.send_email(field_transfer)





