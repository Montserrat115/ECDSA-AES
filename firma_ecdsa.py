import base64
import hashlib
import os
from ecdsa import SigningKey

PRIVATE_KEY_FILE = "private_key.pem"

def firmar_datos(datos_bytes):
    if not os.path.exists(PRIVATE_KEY_FILE):
        raise FileNotFoundError("No se encontró la llave privada")
    with open(PRIVATE_KEY_FILE, 'rb') as f:
        sk = SigningKey.from_pem(f.read())
    signature = sk.sign(datos_bytes, hashfunc=hashlib.sha256)
    return base64.b64encode(signature)  # firma en base64