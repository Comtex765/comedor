import qrcode
import json


def generar_qr(nombre, id_reserva, menu, hora_reserva, fecha_reserva):
    # Datos JSON
    data = {
        "nombre": nombre,
        "id_reserva": id_reserva,
        "menu": menu,
        "hora_reserva": hora_reserva,
        "fecha_reserva": fecha_reserva,
    }

    # Convertir JSON a cadena
    json_data = json.dumps(data)

    # Generar código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(json_data)
    qr.make(fit=True)

    # Crear una imagen a partir de la instancia QR
    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar la imagen en un archivo
    filename = f"./api/img/{id_reserva}_qrcode.png"
    img.save(filename)

    print(f"Código QR generado y guardado como {filename}")
