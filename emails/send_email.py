from email.mime.text import MIMEText
from logs.email_send_logger import EmailSendLogger
import ssl
import smtplib

class EmailSendError(Exception):
    pass


class EmailManager:
    SMTP_HOST_GMAIL = 'smtp.gmail.com'
    SMTP_PORT_GMAIL = 587

    def __init__(self, username, password, host = SMTP_HOST_GMAIL, port = SMTP_PORT_GMAIL) -> None:
        self.username = username
        self.password = password
        self.smtp_host = host
        self.smtp_port = port
        self.email_logger = EmailSendLogger('send_email')

    def field_transfer(self, msg, from_email, to_email, subject = None) -> MIMEText:
        message = MIMEText(msg)
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject

        return message

    def send_email(self, mime_text: MIMEText) -> None:
        context = ssl.create_default_context()

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as smtp:
                smtp.ehlo()
                smtp.starttls(context=context)
                smtp.ehlo()
                smtp.login(self.username, self.password)
                smtp.send_message(mime_text)
                self.email_logger.info_message('メールを送信しました。宛先: {}'.format(mime_text['To']))

        except:
            raise EmailSendError('メールの送信に失敗')

        finally:
            self.email_logger.info_message('処理が完了しました')



