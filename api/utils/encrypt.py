from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes

import os
import base64


# Función para generar una clave a partir de una contraseña
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = kdf.derive(password.encode())
    return key


# Función para encriptar un mensaje
def encrypt(message, password):
    salt = os.urandom(16)
    iv = os.urandom(16)

    key = generate_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()

    padded_data = padder.update(message.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(salt + iv + ciphertext).decode("utf-8")


# Función para desencriptar un mensaje
def decrypt(encrypted_message, password):
    encrypted_data = base64.b64decode(encrypted_message)

    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]

    ciphertext = encrypted_data[32:]

    key = generate_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()

    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data.decode("utf-8")


# Ejemplo de uso
password = "mi_contraseña_segura"
mensaje = "Este es un mensaje secreto"

# Encriptar el mensaje
mensaje_encriptado = encrypt(mensaje, password)
print(f"Mensaje encriptado: {mensaje_encriptado}")

# Desencriptar el mensaje
mensaje_desencriptado = decrypt(mensaje_encriptado, password)
print(f"Mensaje desencriptado: {mensaje_desencriptado}")
