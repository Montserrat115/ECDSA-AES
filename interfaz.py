# pip install customtkinter Pillow
# pip install cryptography

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import cifrado_aes      # <--- Importamos el cifrado
import firma_ecdsa      # <--- Importamos la firma

# ------------------ Interfaz ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Registro de Usuario - Gimnasio")
ventana.geometry("800x600")

def cargar_foto():
    archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])
    if archivo:
        mostrar_foto(archivo)

def mostrar_foto(ruta):
    imagen = Image.open(ruta).resize((150, 150))
    foto_tk = ImageTk.PhotoImage(imagen)
    foto_label.configure(image=foto_tk, text="")
    foto_label.image = foto_tk

def registrar_usuario():
    datos = {
        "nombre": entry_nombre.get(),
        "apellido": entry_apellido.get(),
        "direccion": entry_direccion.get(),
        "telefono": entry_telefono.get(),
        "correo": entry_correo.get(),
        "usuario": entry_usuario.get(),
        "contrasena": entry_contrasena.get()
    }

    texto = "\n".join(f"{k}: {v}" for k, v in datos.items())
    texto_cifrado = cifrado_aes.cifrar_texto(texto)

    firma = firma_ecdsa.firmar_datos(texto_cifrado)
    
    with open("usuarios.txt", "ab") as archivo:
        archivo.write(firma + b"\n")           # firma en base64
        archivo.write(texto_cifrado + b"\n")   # datos cifrados
        archivo.write(b"---\n")

    print("Usuario registrado (datos cifrados).")

titulo = ctk.CTkLabel(ventana, text="Registro de Usuario", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=10)

frame_contenedor = ctk.CTkFrame(ventana)
frame_contenedor.pack(padx=20, pady=10)
frame_contenedor.grid_columnconfigure((0, 1), weight=1)

frame_izquierda = ctk.CTkFrame(frame_contenedor)
frame_izquierda.grid(row=0, column=0, padx=40, pady=10)

foto_label = ctk.CTkLabel(frame_izquierda, text="Cargando...", width=150, height=150)
foto_label.pack(pady=10)

boton_foto = ctk.CTkButton(frame_izquierda, text="Tomar Foto", command=cargar_foto)
boton_foto.pack(pady=5)

ruta_default = "imag1.png"
if os.path.exists(ruta_default):
    mostrar_foto(ruta_default)
else:
    foto_label.configure(text="Imagen no encontrada")

frame_derecha = ctk.CTkFrame(frame_contenedor)
frame_derecha.grid(row=0, column=1, padx=40, pady=10)

entry_nombre = ctk.CTkEntry(frame_derecha, placeholder_text="Nombre")
entry_apellido = ctk.CTkEntry(frame_derecha, placeholder_text="Apellido")
entry_direccion = ctk.CTkEntry(frame_derecha, placeholder_text="Dirección")
entry_telefono = ctk.CTkEntry(frame_derecha, placeholder_text="Teléfono")
entry_correo = ctk.CTkEntry(frame_derecha, placeholder_text="Correo Electrónico")
entry_usuario = ctk.CTkEntry(frame_derecha, placeholder_text="Nombre de Usuario")
entry_contrasena = ctk.CTkEntry(frame_derecha, placeholder_text="Contraseña", show="*")

for widget in [entry_nombre, entry_apellido, entry_direccion, entry_telefono,
               entry_correo, entry_usuario, entry_contrasena]:
    widget.pack(pady=5)

boton_registro = ctk.CTkButton(ventana, text="Registrar Usuario", command=registrar_usuario)
boton_registro.pack(pady=20)

ventana.mainloop()
