from emails.send_email import EmailApplication, EmailSender
import os


APPLICATION_EMAIL_USER = os.getenv('APPLICATION_EMAIL_USER')
APPLICATION_EMAIL_PASSWORD = os.getenv('APPLICATION_EMAIL_PASSWORD')

if __name__ == '__main__':
    EmailApplication.application_controller_prompt()



