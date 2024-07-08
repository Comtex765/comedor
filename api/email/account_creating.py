from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from colorama import Fore, Style
from dotenv import load_dotenv

import smtplib
import os

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(email_receiver, user):
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_SENDER
    msg["To"] = email_receiver
    msg["Subject"] = "Usuario Creado"

    body = f"""
    <html>
    <body>
    <center>
        <h1>¡Hola!</h1>
    </center>

    <p>
        Bienvenido/a

        <b style="color: coral;">{user}</b>
    </p>

    <p>
        Te informamos que se ha creado exitosamente tu cuenta en Comedor ESPOCH.

        <br>
        Recuerda que tu usuario será tu correo:

        <b style="color: coral;">{email_receiver}</b>

        <br>
        <br>
        Junto a la contraseña ingresada en el registro

        <br>

        <h4 style="font-style: italic; font-size: 22px; text-decoration: underline; color: rgb(255, 92, 80);">
            Nunca compartas tus credenciales
        </h4>
    </p>

    <p>Te esperamos.</p>
    </body>

    <footer style="font-size: 10px;">
        Saludos,

        <br>
        El equipo DTIC
    </footer>
    </html>
    """
    # Crear el objeto MIMEText con el contenido HTML
    mime_text = MIMEText(body, "html")

    # Adjuntar el contenido HTML al mensaje
    msg.attach(mime_text)

    # Conectar al servidor SMTP de Gmail
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        # Enviar el correo
        server.sendmail(EMAIL_SENDER, email_receiver, msg.as_string())
        print(
            f"\n{Fore.CYAN}INFO:{Style.RESET_ALL}     ❤️  Correo enviado correctamente a {email_receiver}  ❤️"
        )

    except Exception as e:
        print(
            f"\n{Fore.RED}ERROR:{Style.RESET_ALL}     💔  Error al enviar el correo a {email_receiver}: {str(e)}  💔"
        )

    finally:
        server.quit()
