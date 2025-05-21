import base64
import os
from ecdsa import VerifyingKey
import hashlib
import firma_ecdsa  # si está en el mismo directorio y necesitas usar firmar/verificar juntos

PUBLIC_KEY_FILE = "public_key.pem"

def verificar_firma(datos_bytes, firma_b64):
    if not os.path.exists(PUBLIC_KEY_FILE):
        raise FileNotFoundError("No se encontró la llave pública")
    with open(PUBLIC_KEY_FILE, 'rb') as f:
        vk = VerifyingKey.from_pem(f.read())
    signature = base64.b64decode(firma_b64)
    try:
        return vk.verify(signature, datos_bytes, hashfunc=hashlib.sha256)
    except:
        return False

def verificar_archivo(ruta):
    with open(ruta, "rb") as f:
        contenido = f.read()

    bloques = contenido.split(b"---\n")
    for i, bloque in enumerate(bloques):
        if not bloque.strip():
            continue
        lineas = bloque.strip().split(b"\n")
        if len(lineas) < 2:
            print(f"[Bloque {i+1}] Incompleto")
            continue

        firma_b64 = lineas[0]
        datos_cifrados = lineas[1]

        es_valida = verificar_firma(datos_cifrados, firma_b64)
        if es_valida:
            print(f"[Bloque {i+1}] ✅ Firma válida")
        else:
            print(f"[Bloque {i+1}] ❌ Firma inválida o datos modificados")

# Ejecutar verificación (puedes comentar esta parte si importas desde otro script)
if __name__ == "__main__":
    verificar_archivo("usuarios.txt")
