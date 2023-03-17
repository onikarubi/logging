from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logs.email_send_logger import EmailSendLogger
from user.application_user import ApplicationEmailUser
from user.password_encryption import PasswordEncryption
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

        application_email_user = EmailApplication.set_application_email_user(application_user_name, application_user_password)
        EmailApplication.control_sender(app_user=application_email_user)

    def set_application_email_user(username: str, password: str) -> ApplicationEmailUser:
        if username == '' or  password == '':
            raise ValueError('ユーザー名及びパスワードが空')

        return ApplicationEmailUser(username=username, password=password)

    def control_sender(app_user: ApplicationEmailUser) -> None:
        email_sender = EmailSender(app_user.username, app_user.password)
        email_sender.authentication_server()
        input_from = os.getenv('APPLICATION_EMAIL_USER')
        input_to = input('To >>> ')
        input_subject = input('Subject(タイトル) >>> ')
        input_msg_body = input('メールの内容 >>> ')
        attachment_files: bool = EmailApplication.is_attachment_files(input('ファイルを添付しますか？ Y/n >> '))

        email_sender.attachment_text(msg_body=input_msg_body, from_email=input_from, to_email= input_to, subject=input_subject)

        if attachment_files:
            file_path = input('ファイルのパス >> ')
            file_name = input('ファイル名 >> ')

            if file_name == '':
                raise ValueError('名前が空文字を指定しています')

            email_sender.attachment_file(file_path=file_path, file_name=file_name)

        email_sender.send_email()

    def is_attachment_files(input_selector: str) -> bool:
        while input_selector == 'Y' or input_selector == 'n':

            if input_selector == 'Y': return True
            if input_selector == 'n': return False

            print('Y/n で入力して下さい')

class EmailAuthenticateException(Exception):
    pass

class SendEmailException(Exception):
    pass


class EmailSender:
    SMTP_HOST_GMAIL = 'smtp.gmail.com'
    SMTP_PORT_GMAIL = 587

    def __init__(self, username, password, host = SMTP_HOST_GMAIL, port = SMTP_PORT_GMAIL) -> None:
        self.username = username
        self.password = password
        self.encrypt_password = PasswordEncryption(self.password)
        self.smtp_host = host
        self.smtp_port = port
        self.multipart = MIMEMultipart()
        self.email_logger = EmailSendLogger('send_email')
        self.smtp = SMTP(self.smtp_host, self.smtp_port)
        self._context = ssl.create_default_context()
        self._application_user = {
            "application_username": self.username, "application_password": self.encrypt_password.hash_password()}

        self.smtp.ehlo()
        self.smtp.starttls(context=self._context)

    @property
    def application_user(self): return self._application_user


    """
    メッセージ内容の編集、設定

    - 宛先、送信元、件名を登録
    - テキストメッセージを設定し、multipartに紐付けさせる
    """
    def attachment_text(self, msg_body, from_email, to_email, subject = None, subtype="plain") -> None:
        self.multipart['From'] = from_email
        self.multipart['To'] = to_email
        self.multipart['Subject'] = subject
        message = MIMEText(msg_body, subtype)
        self.multipart.attach(message)

    """
    添付ファイルの設定

    - 引数に指定された参照先のファイルパスから内容を読み込む
    - 第二引数から送信先に添付するファイル名を設定してmime_textのヘッダーに追加
    - 設定した添付ファイルの内容をmultipartに紐付ける
    """
    def attachment_file(self, file_path, file_name):
        with open(file_path, 'r') as f:
            attachment_file = MIMEText(f.read(), 'plain')
            attachment_file.add_header(
                'Content-Disposition',
                'attachment',
                filename=file_name
            )
            self.multipart.attach(attachment_file)

    """
    メールサーバーの認証

    - ssl通信で通信を暗号化する
    - gmailアプリケーションの認証を行う
    """

    def authentication_server(self):
        try:
            self.smtp.ehlo()
            self.smtp.login(self.username, self.password)
            self.email_logger.info_message(f'認証情報: {self.application_user}')

        except:
            msg = f'認証に失敗しました。{self.application_user}'
            self.email_logger.error_output(msg)
            raise EmailAuthenticateException(msg)


    """
    各設定を行なったmultipartをメールサーバーに送信

    - メールを送信する
    """
    def send_email(self) -> None:
        try:
            self.smtp.ehlo()
            self.smtp.send_message(self.multipart)
            success_msg = f""" \
                メールを送信しました。

                宛先: {self.multipart['To']}
                タイトル: {self.multipart['Subject']}"""

            print('メールを送信しました')
            self.email_logger.info_message(success_msg)

        except Exception as error:
            err_msg = f"""メールの送信に失敗しました """
            self.email_logger.error_output(err_msg)
            raise SendEmailException(err_msg, error)

        finally:
            self.email_logger.info_message('処理が終了しました')
            self.smtp.quit()


