import smtplib
from email.mime.text import MIMEText

class SendEmail(object):

  def send_verify_email(self, template, email):
    message_cont = template
    message = MIMEText(message_cont, 'html')

    message['From'] = 'kakashi.kisura7@gmail.com'
    message['To'] = email
    message['Subject'] = 'Verificação de cadastro'

    msg_full = message.as_string()

    # server = smtplib.SMTP('smtp.gamail.com:587')
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    # server.login('apprendafixa@rendafixa.rocks', '281178')
    # server.login('roberto.rosa7@gmail.com', 'Tnzro&ilyvigl2602')
    server.login('kakashi.kisura7@gmail.com', 'Tnzro&ilyvigl2602')
    server.sendmail(message['From'], message['To'], msg_full)
    server.quit()

    print('Email de verificação enviado')
