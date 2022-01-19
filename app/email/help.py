import smtplib
import os
from dotenv import dotenv_values, load_dotenv


def send_email(message):
    load_dotenv()
    password = os.getenv('PASSWORD')
    email = os.getenv('EMAIL')
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()