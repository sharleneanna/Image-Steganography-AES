# -*- coding: utf-8 -*-
"""stg.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19JQXqyTGbB5tks2cDSU6alXDk6oxn36r
"""

import cv2
import gradio as gr
import numpy as np
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import os

def encrypt_message(secret_msg, password):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = kdf.derive(password.encode())

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padded_msg = secret_msg + ' ' * (16 - len(secret_msg) % 16)
    encrypted_msg = encryptor.update(padded_msg.encode()) + encryptor.finalize()

    return base64.b64encode(salt + iv + encrypted_msg).decode()

def decrypt_message(encrypted_msg, password):
    try:
        encrypted_msg = base64.b64decode(encrypted_msg)
        salt, iv, encrypted_data = encrypted_msg[:16], encrypted_msg[16:32], encrypted_msg[32:]

        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
        key = kdf.derive(password.encode())

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_msg = decryptor.update(encrypted_data) + decryptor.finalize()

        return decrypted_msg.decode().strip()
    except:
        return "Decryption Failed! Incorrect Password."

def encode_message(image, msg, password):
    img = cv2.imread(image.name)
    h, w, _ = img.shape

    encrypted_msg = encrypt_message(msg, password)
    msg_ascii = [ord(c) for c in encrypted_msg]

    if len(msg_ascii) + 2 > h * w:
        return "Error: Message too long for this image!"

    img[0, 0, 0] = len(msg_ascii)

    index = 1
    for i, char in enumerate(msg_ascii):
        img[0, index, 1] = char
        index += 1

    encrypted_image_path = "encrypted_image.png"
    cv2.imwrite(encrypted_image_path, img)

    return encrypted_image_path

def decode_message(image, password_input):
    img = cv2.imread(image.name)
    h, w, _ = img.shape

    msg_length = img[0, 0, 0]
    encrypted_msg = "".join(chr(img[0, i + 1, 1]) for i in range(msg_length))

    decrypted_msg = decrypt_message(encrypted_msg, password_input)

    if decrypted_msg.startswith("Decryption Failed"):
        return decrypted_msg
    return f"Decryption Successful! Message: {decrypted_msg}"

encrypt_interface = gr.Interface(
    fn=encode_message,
    inputs=["file", "text", "text"],
    outputs="file",
    title="AES-Powered Image Steganography",
    description="Upload an image, enter a secret message & password. The message is AES-encrypted and hidden inside the image."
)

decrypt_interface = gr.Interface(
    fn=decode_message,
    inputs=["file", "text"],
    outputs="text",
    title="Decrypt AES-Encrypted Message",
    description="Upload the encrypted image & enter the correct password to retrieve your AES-encrypted message."
)

gr.TabbedInterface([encrypt_interface, decrypt_interface], ["Encrypt", "Decrypt"]).launch()