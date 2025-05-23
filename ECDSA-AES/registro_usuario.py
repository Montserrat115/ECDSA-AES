# pip install customtkinter Pillow cryptography
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import base64
import sqlite3
import random
from datetime import date
import cifrado_aes
import firma_ecdsa

# Conexión a la base de datos SQLite
conn = sqlite3.connect("gimnasio.db")
cursor = conn.cursor()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Registro de Usuario - Gimnasio")
ventana.geometry("800x700")

ruta_foto = None

def cargar_foto():
    global ruta_foto
    archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])
    if archivo:
        ruta_foto = archivo
        mostrar_foto(archivo)

def mostrar_foto(ruta):
    imagen = Image.open(ruta).resize((150, 150))
    foto_tk = ImageTk.PhotoImage(imagen)
    foto_label.configure(image=foto_tk, text="")
    foto_label.image = foto_tk

def registrar_usuario():
    global ruta_foto

    # Valores por defecto si están vacíos
    direccion = entry_direccion.get() or "N/A"
    correo = entry_correo.get() or "*@*.com"

    # Paso 1: Insertar con valores reales excepto la cédula personalizada
    cursor.execute("""
        INSERT INTO cliente (nombre, apellido_1, apellido_2, direccion, e_mail,
                             fecha_inscripcion, celular, huella_biometrica,
                             tarjeta_ultimos4, tarjeta_token, foto_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entry_nombre.get(),
        entry_apellido.get(),
        entry_apellido2.get(),
        direccion,
        correo,
        str(date.today()),
        int(entry_telefono.get()),
        base64.b64encode(b"biometrico_fake"),  # Simulación de biometría
        entry_tarjeta.get()[-4:] if entry_tarjeta.get() else None,
        "token_fake",
        ruta_foto or ""
    ))

    conn.commit()

    # Paso 2: Obtener el ID autogenerado
    cursor.execute("SELECT last_insert_rowid()")
    nuevo_id = cursor.fetchone()[0]

    # Paso 3: Crear cédula personalizada y actualizar
    nombre = entry_nombre.get().strip().lower()
    cedula_personalizada = f"{nombre[:3]}{nuevo_id:03d}{random.randint(100,999)}"

    cursor.execute("UPDATE cliente SET cedula = ? WHERE rowid = ?", (cedula_personalizada, nuevo_id))
    conn.commit()

    # Paso 4: Cifrado y firma
    datos = {
        "cedula": cedula_personalizada,
        "nombre": entry_nombre.get(),
        "apellido_1": entry_apellido.get(),
        "apellido_2": entry_apellido2.get(),
        "direccion": direccion,
        "e_mail": correo,
        "fecha_inscripcion": str(date.today()),
        "celular": entry_telefono.get(),
        "huella_biometrica": "biometrico_fake",
        "tarjeta_ultimos4": entry_tarjeta.get()[-4:] if entry_tarjeta.get() else "",
        "foto_url": ruta_foto or ""
    }

    texto = "\n".join(f"{k}: {v}" for k, v in datos.items())
    texto_cifrado = cifrado_aes.cifrar_texto(texto)
    firma = firma_ecdsa.firmar_datos(texto_cifrado)

    with open("usuarios.txt", "ab") as archivo:
        archivo.write(firma + b"\n")
        archivo.write(texto_cifrado + b"\n")
        archivo.write(b"---\n")

    print(f"Usuario registrado con cédula generada: {cedula_personalizada}")

# ----- INTERFAZ -----
titulo = ctk.CTkLabel(ventana, text="Registro de Usuario", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=10)

frame_contenedor = ctk.CTkFrame(ventana)
frame_contenedor.pack(padx=20, pady=10)
frame_contenedor.grid_columnconfigure((0, 1), weight=1)

frame_izquierda = ctk.CTkFrame(frame_contenedor)
frame_izquierda.grid(row=0, column=0, padx=40, pady=10)

foto_label = ctk.CTkLabel(frame_izquierda, text="Cargando...", width=150, height=150)
foto_label.pack(pady=10)

boton_foto = ctk.CTkButton(frame_izquierda, text="Cargar Foto", command=cargar_foto)
boton_foto.pack(pady=5)

frame_derecha = ctk.CTkFrame(frame_contenedor)
frame_derecha.grid(row=0, column=1, padx=40, pady=10)

entry_nombre = ctk.CTkEntry(frame_derecha, placeholder_text="Nombre")
entry_apellido = ctk.CTkEntry(frame_derecha, placeholder_text="Primer Apellido")
entry_apellido2 = ctk.CTkEntry(frame_derecha, placeholder_text="Segundo Apellido")
entry_direccion = ctk.CTkEntry(frame_derecha, placeholder_text="Dirección")
entry_correo = ctk.CTkEntry(frame_derecha, placeholder_text="Correo Electrónico")
entry_telefono = ctk.CTkEntry(frame_derecha, placeholder_text="Celular")
entry_tarjeta = ctk.CTkEntry(frame_derecha, placeholder_text="Tarjeta (últimos 4)")

for widget in [entry_nombre, entry_apellido, entry_apellido2,
               entry_direccion, entry_correo, entry_telefono, entry_tarjeta]:
    widget.pack(pady=5)

boton_registro = ctk.CTkButton(ventana, text="Registrar Usuario", command=registrar_usuario)
boton_registro.pack(pady=20)

ventana.mainloop()
