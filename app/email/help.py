import smtplib
import os
from dotenv import load_dotenv



def send_email(message):
    load_dotenv()
    password = os.getenv('PASSWORD')
    email = os.getenv('EMAIL')
    try:
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
    except ConnectionAbortedError:
        print("Проверьте подключение к интернету")
    except smtplib.SMTPAuthenticationError:
        print("Неверный пароль или почта")
    except smtplib.SMTP_SSL:
        print("Что то пошло не так")
    except smtplib.SMTPConnectError:
        print("Проверьте подключение к интернету")
    except smtplib.SMTPSenderRefused:
        print("Почта получателя отказала в отправке письма")
    except smtplib.SMTPRecipientsRefused:
        print("Почта получателя отказала в отправке письма")
    except smtplib.SMTPServerDisconnected:
        print("Возникла проблема при подключении к серверу. Воможно сервер отключён.")
    # except smtplib.SMTPResponseException:
    #     print("")

