import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
BD_PASSWORD = os.getenv('BD_PASSWORD')
BD_USER = os.getenv('BD_USER')

MY_HIPS_EMAIL = os.getenv("MY_HIPS_EMAIL")
MY_HIPS_EMAIL_PASSWORD = os.getenv("MY_HIPS_EMAIL_PASSWORD")

MAIL_HIPS_ADMIN = os.getenv("MAIL_HIPS_ADMIN")

connection = smtplib.SMTP("smtp.gmail.com")
connection.starttls()


def enviar_mail_asunto_body(tipo_alerta,asunto, cuerpo):
    connection.login(user=MY_HIPS_EMAIL, password=MY_HIPS_EMAIL_PASSWORD)
    connection.sendmail(
        from_addr=MY_HIPS_EMAIL, 
        to_addrs=MAIL_HIPS_ADMIN, 
        msg=f"Subject:{tipo_alerta} {asunto}\n\n{cuerpo}"
    )
    connection.close()



