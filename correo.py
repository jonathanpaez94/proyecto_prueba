import os
from dotenv import load_dotenv
import ssl
import smtplib
from email.message import EmailMessage

load_dotenv()

correo_envio = os.getenv("C")
correo_recibe = os.getenv("C")
correo_p = os.getenv("P")


subject = "Camara Seguridad"

em = EmailMessage()
em["From"] = correo_envio
em["To"] = correo_recibe
em["Subject"] = subject

def enviar_correo(cuerpo:str):
    em.set_content(cuerpo)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
        smtp.login(correo_envio,correo_p)
        smtp.sendmail(correo_envio,correo_recibe,em.as_string())