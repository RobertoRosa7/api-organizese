import smtplib
from email.mime.text import MIMEText
import os

API_EMAIL = os.environ.get('email')
API_PASSWORD = os.environ.get('password')

class SendEmail(object):

  def send_verify_email(self, template, email):
    message_cont = template
    message = MIMEText(message_cont, 'html')

    message['From'] = API_EMAIL
    message['To'] = email
    message['Subject'] = 'Verificação de cadastro'
    msg_full = message.as_string()
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(API_EMAIL, API_PASSWORD)
    server.sendmail(message['From'], message['To'], msg_full)
    server.quit()

    print('Email de verificação enviado')
