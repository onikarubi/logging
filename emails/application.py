from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logs.email_send_logger import EmailSendLogger
from user.application_user import ApplicationEmailUser
from .send_email import GmailSender
from smtplib import SMTP
import os
import ssl


class EmailApplication:
    @staticmethod
    def application_controller_prompt() -> None:
        selector = int(
            input('認証設定: 1 -> 環境変数からデフォルトでログイン: 2 -> プロンプトの入力からログイン \n'))

        while selector <= 0 or selector > 2:
            print('0 < n <= 2 の範囲で入力して下さい \n')
            selector = int(
                input('認証設定: 1 -> 環境変数からデフォルトでログイン  2 -> プロンプトの入力からログイン \n'))

        if selector == 1:
            application_user_name = f"{os.getenv('APPLICATION_EMAIL_USER')}@gmail.com"
            application_user_password = os.getenv('APPLICATION_EMAIL_PASSWORD')

        elif selector == 2:
            application_user_name = input('emailアプリケーションユーザー名: ')
            application_user_password = input('emailアプリケーションパスワード: ')

        application_email_user = EmailApplication.set_application_email_user(
            application_user_name, application_user_password)
        EmailApplication.control_sender(app_user=application_email_user)

    def set_application_email_user(username: str, password: str) -> ApplicationEmailUser:
        if username == '' or password == '':
            raise ValueError('ユーザー名及びパスワードが空')

        return ApplicationEmailUser(username=username, password=password)

    def control_sender(app_user: ApplicationEmailUser) -> None:
        email_sender = GmailSender(app_user.username, app_user.password)
        email_sender.authentication_server()
        input_from = os.getenv('APPLICATION_EMAIL_USER')
        input_to = input('To >>> ')
        input_subject = input('Subject(タイトル) >>> ')
        input_msg_body = input('メールの内容 >>> ')
        attachment_files: bool = EmailApplication.is_attachment_files(
            input('ファイルを添付しますか？ Y/n >> '))

        email_sender.attachment_text(
            msg_body=input_msg_body, from_email=input_from, to_email=input_to, subject=input_subject)

        if attachment_files:
            file_path = input('ファイルのパス >> ')
            file_name = input('ファイル名 >> ')

            if file_name == '':
                raise ValueError('名前が空文字を指定しています')

            email_sender.attachment_file(
                file_path=file_path, file_name=file_name)

        email_sender.send_email()

    def is_attachment_files(input_selector: str) -> bool:
        while input_selector == 'Y' or input_selector == 'n':

            if input_selector == 'Y':
                return True
            if input_selector == 'n':
                return False

            print('Y/n で入力して下さい')
