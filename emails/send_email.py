from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
        self.msg = MIMEMultipart()
        self.email_logger = EmailSendLogger('send_email')

    def attachment_text(self, msg, from_email, to_email, subject = None, subtype="plain") -> None:
        self.msg['From'] = from_email
        self.msg['To'] = to_email
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(msg, subtype))

    def attachment_file(self, file_path, file_name):
        with open(file_path, 'r') as f:
            attachment_file = MIMEText(f.read(), 'plain')
            attachment_file.add_header(
                'Content-Disposition',
                'attachment',
                filename=file_name
            )
            self.msg.attach(attachment_file)

    def send_email(self) -> None:
        context = ssl.create_default_context()

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as smtp:
                smtp.ehlo()
                smtp.starttls(context=context)
                smtp.ehlo()
                smtp.login(self.username, self.password)
                print(type(self.msg))
                smtp.send_message(self.msg)
                self.email_logger.info_message('メールを送信しました。宛先: {}'.format(self.msg['To']))

        except Exception as error:
            raise EmailSendError('メールの送信に失敗', error)

        finally:
            self.email_logger.info_message('処理が完了しました')



