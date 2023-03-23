from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logs.email_send_logger import EmailSendLogger
from user.password_encryption import PasswordEncryption
from smtplib import SMTP
import ssl

class EmailAuthenticateException(Exception):
    pass

class SendEmailException(Exception):
    pass


class EmailSender:

    def __init__(self, username, password, host=None, port=None, is_attachment_file: bool = False, smtp=None) -> None:
        self._username = username
        self._password = password
        self.encrypt_password = PasswordEncryption(self.password)
        self._smtp_host = host
        self._smtp_port = port
        self.multipart = MIMEMultipart()
        self.email_logger = EmailSendLogger('send_email')
        self._is_attachment_file = is_attachment_file
        self._smtp = smtp
        self._application_user = {
            "application_username": self.username, "application_password": self.encrypt_password.hash_password()}

    @property
    def username(self): return self._username
    @property
    def password(self): return self._password
    @property
    def smtp_host(self): return self._smtp_host
    @property
    def smtp_port(self): return self._smtp_port
    @property
    def application_user(self): return self._application_user
    @property
    def smtp(self) -> SMTP: return self._smtp
    @property
    def is_attachment_file(self) -> bool: return self._is_attachment_file

    @is_attachment_file.setter
    def change_attachment_file_flag(self, flag: bool = None):
        self._is_attachment_file = flag

    @smtp_host.setter
    def smtp_host(self, host_name: str) -> str:
        if host_name == '' or host_name == None:
            return

        self._smtp_host = host_name

    @smtp_port.setter
    def smtp_port(self, port_num: int) -> int:
        if port_num == None:
            return

        self._smtp_port = port_num

    @smtp.setter
    def smtp(self, smtp: SMTP):
        self._smtp = smtp
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
        if not self._is_attachment_file:
            return

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
            context = ssl.create_default_context()
            self.smtp.ehlo()
            self.smtp.starttls(context=context)
            self.smtp.login(self.username, self.password)
            self.email_logger.info_message('認証しました。')
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
            self.smtp.send_message(self.multipart)
            success_msg = f" メールを送信しました。\n"\
                f"宛先: {self.multipart['To']} \n"\
                f"タイトル: {self.multipart['Subject']}"

            self.email_logger.info_message(success_msg)

        except Exception as error:
            err_msg = f"""メールの送信に失敗しました """
            self.email_logger.error_output(err_msg)
            raise SendEmailException(err_msg, error)

        finally:
            self.email_logger.info_message('処理が終了しました')
            self.smtp.quit()



class GmailSender(EmailSender):
    GMAIL_APPLICATION_HOST = 'smtp.gmail.com'
    GMAIL_APPLICATION_PORT = 587

    def __init__(self, username, password, host=None, port=None, smtp=None) -> None:
        super().__init__(username, password, host, port, smtp)
        self.smtp_host = host or self.GMAIL_APPLICATION_HOST
        self.smtp_port = port or self.GMAIL_APPLICATION_PORT
        self.smtp = SMTP(self.smtp_host, self.smtp_port)



