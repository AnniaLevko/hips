import smtplib

MY_HIPS_EMAIL = "erikanniahipsserver1@gmail.com"
MY_HIPS_EMAIL_PASSWORD = "erikannia7"

MAIL_HIPS_ADMIN = "jefehips2021@gmail.com"

connection = smtplib.SMTP("smtp.gmail.com")
connection.starttls()




def enviar_mail_asunto_body(asunto, cuerpo):
    connection.login(user=MY_HIPS_EMAIL, password=MY_HIPS_EMAIL_PASSWORD)
    connection.sendmail(
        from_addr=MAIL_HIPS_ADMIN, 
        to_addrs=MAIL_HIPS_ADMIN, 
        msg=f"Subject:{asunto}\n\n{cuerpo}"
    )
    connection.close()



