from emails.file_manager import FileManager
from emails.send_email import EmailManager
from dotenv import load_dotenv
import os


if __name__ == '__main__':
    load_dotenv('./.env')
    username = os.getenv('user')
    password = os.getenv('pass')
    to_email = os.getenv('to_email')
    from_email = f'{username}@gmail.com'

    msg_file_path = './emails/msg.txt'
    text_file = FileManager(msg_file_path)
    message_file = text_file.read_file()

    gmail_manager = EmailManager(username, password)
    gmail_manager.attachment_text(message_file, from_email=from_email, to_email=to_email, subject='test タイトル')
    gmail_manager.attachment_file(msg_file_path, 'hogehoge.txt')
    gmail_manager.send_email()



