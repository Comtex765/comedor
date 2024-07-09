from api.schemas.sch_dinings import ReservationWhole as sch_dining
from api.utils.qr_generator import eliminar_archivo, generar_qr
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from colorama import Fore, Style
from dotenv import load_dotenv

import smtplib
import os

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
IVA = float(os.getenv("IVA"))


def send_email(reservation: sch_dining):
    nombre = (
        reservation["user"]["user"]["user_name"]
        + " "
        + reservation["user"]["user"]["user_last_name"]
    )
    reservation_date = reservation["reservation"]["reservation_date"]
    reservation_hour = reservation["reservation"]["reservation_hour"]
    percent_discount = reservation["user"]["type"]["percent_discount"]
    fecha_creacion = reservation["reservation"]["created_date"]
    menu_type = reservation["menu"]["menu_type"]["menu_type"]
    meal_time = reservation["menu"]["meal_time"]["meal_time"]
    id_factura = reservation["reservation"]["id_reservation"]
    email_receiver = reservation["user"]["user"]["email"]
    reservation_hour = reservation_hour.strftime("%H:%M")
    menu = reservation["menu"]["menu"]["menu_title"]
    total = reservation["reservation"]["total_cost"]
    price = reservation["menu"]["menu"]["price"]

    generar_qr(nombre, id_factura, menu, reservation_hour, str(reservation_date))

    # Calculando el total con descuento
    discount = (price * percent_discount) / 100
    discount = "{:.2f}".format(discount)

    iva = "{:.2f}".format(price * IVA)

    subtotal = "{:.2f}".format(price)

    price *= 1 - IVA
    price = "{:.2f}".format(price)

    msg = MIMEMultipart("related")
    msg["From"] = EMAIL_SENDER
    msg["To"] = email_receiver
    msg["Subject"] = "Reserva Realizada"

    body = f"""
    <html>
    <head>
        <style>
            body {{
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }}
            .ticket {{
                max-width: 400px;
                margin: 0 auto 20px;
                background: #fff;
                padding: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }}
            .ticket h1 {{
                text-align: center;
                font-size: 24px;
                margin-bottom: 10px;
            }}
            .ticket h2 {{
                text-align: center;
                font-size: 20px;
                margin: 0;
                color: #666;
            }}
            .ticket p {{
                font-size: 16px;
                margin: 5px 0;
            }}
            .ticket .details {{
                border-top: 1px solid #ccc;
                margin: 10px 0;
                padding-top: 10px;
            }}
            .ticket .details p {{
                font-size: 14px;
            }}
            .ticket .items {{
                border-top: 1px solid #ccc;
                margin: 10px 0;
                padding-top: 10px;
            }}
            .ticket .items .item {{
                display: flex;
                justify-content: space-between;
                margin: 5px 0;
            }}
            .ticket .items #precio {{
                padding-left: 200px;
            }}
            .ticket .total {{
                border-top: 1px solid #ccc;
                margin: 10px 0;
                padding-top: 10px;
                font-size: 18px;
                text-align: right;
            }}
            .ticket .footer {{
                text-align: center;
                margin-top: 10px;
                font-size: 12px;
                color: #666;
            }}
            .ticket-small {{
                max-width: 300px;
                margin: 0 auto;
                background: #fff;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }}
            .ticket-small h1 {{
                text-align: center;
                font-size: 20px;
                margin-bottom: 10px;
            }}
            .ticket-small p {{
                font-size: 14px;
                margin: 5px 0;
            }}
            .ticket-small .details {{
                border-top: 1px solid #ccc;
                margin: 10px 0;
                padding-top: 10px;
            }}
            .ticket-small .details p {{
                font-size: 14px;
            }}
            .ticket-small .footer {{
                text-align: center;
                margin-top: 10px;
                font-size: 12px;
                color: #666;
            }}
        </style>
    </head>
    <header>
        <center>
            <h1>¡Hola!</h1>
        </center>
        <p>
            Bienvenido/a <b style="color: coral;">{nombre}</b>
        </p>
        <p>
            Te informamos que se ha concretado exitosamente tu reserva en Comedor ESPOCH.
            <br><br>
            A continuación te mostramos tu factura electrónica junto a los detalles de tu reserva.
            <br>
            <p style="font-style: italic; font-size: 20px;">¡Provecho!</p>
        </p>
    </header>
    <body>
        <div class="ticket">
            <h1>Factura de Compra</h1>
            <h2>Comedor ESPOCH</h2>
            <p><b>Dirección:</b> Panamericana Sur km 1 1/2</p>
            <p><b>Teléfono:</b> 593(03) 2998-200</p>
            <p><b>Email:</b> info@espoch.edu.ec</p>
            <div class="details">
                <p><strong>Fecha:</strong> {fecha_creacion}</p>
                <p><strong>Número de Factura:</strong> {id_factura}</p>
                <p><strong>Cliente:</strong> {nombre}</p>
            </div>
            <div class="items">
                <div class="item">
                    <span>{menu}</span>
                    <span id="precio">${price}</span>
                </div>
            </div>
            <div class="total" style="font-size: 18px;">
                <p><strong>IVA {int(IVA * 100)}%:</strong> ${iva}</p>
                <p><strong>Subotal:</strong> ${subtotal}</p>
                <p><strong>Descuento {int(percent_discount)}%:</strong> ${discount}</p>
                <p><strong>Total:</strong> ${total}</p>
            </div>
            <div class="footer" style="font-style: italic;">
                <p>¡Gracias por su compra!</p>
            </div>
        </div>
        <div class="ticket-small">
            <h1>Ticket de Reserva</h1>
            <div class="details">
                <p><strong>Fecha de Reserva:</strong> {reservation_date}</p>
                <p><strong>Hora de Reserva:</strong> {reservation_hour}</p>
                <p><strong>Menú Reservado:</strong> {menu}</p>
                <p><strong>Tipo de Menú:</strong> {meal_time} - {menu_type}</p>
                <p style="border-top: 1px solid #ccc; margin-top: 20px;">
                    <center style="margin-top:20px; margin-bottom: 0;">
                        <h3 style="margin: 0;">Código QR</h3>
                    </center>
                    <img src="cid:qr_code" style="max-width: 300px;">
                </p>
            </div>
        </div>
    </body>
    <footer style="font-size: 10px;">
        <br>
        Saludos,
        <br>
        El equipo DTIC
    </footer>
    </html>
    """
    mime_text = MIMEText(body, "html")
    msg.attach(mime_text)

    # Adjuntar la imagen del código QR
    with open(f"./api/img/{id_factura}_qrcode.png", "rb") as qr_file:
        img = MIMEImage(qr_file.read())
        img.add_header("Content-ID", "<qr_code>")
        img.add_header(
            "Content-Disposition", "inline", filename=f"{id_factura}_qrcode.png"
        )
        msg.attach(img)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, email_receiver, msg.as_string())

        print(
            f"\n{Fore.CYAN}INFO:{Style.RESET_ALL}     ❤️  Correo enviado correctamente a {email_receiver}  ❤️"
        )

        eliminar_archivo(f"./api/img/{id_factura}_qrcode.png")
    except Exception as e:
        print(
            f"\n{Fore.RED}ERROR:{Style.RESET_ALL}     💔  Error al enviar el correo a {email_receiver}: {str(e)}  💔"
        )
    finally:
        server.quit()
