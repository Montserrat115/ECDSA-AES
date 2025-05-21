from cryptography.fernet import Fernet
import os

# Ruta de la clave
KEY_FILE = "key.key"

# Genera y guarda una clave si no existe
def generar_clave():
    if not os.path.exists(KEY_FILE):
        clave = Fernet.generate_key()
        with open(KEY_FILE, "wb") as archivo:
            archivo.write(clave)

# Carga la clave desde el archivo
def cargar_clave():
    with open(KEY_FILE, "rb") as archivo:
        return archivo.read()

# Cifra un texto usando Fernet (AES)
def cifrar_texto(texto):
    generar_clave()
    fernet = Fernet(cargar_clave())
    return fernet.encrypt(texto.encode())

# Descifra un texto (opcional)
def descifrar_texto(texto_cifrado):
    fernet = Fernet(cargar_clave())
    return fernet.decrypt(texto_cifrado).decode()
