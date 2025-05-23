# pip install customtkinter
import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import firma_ecdsa  # Módulo que ya tienes implementado

# ------------------ Configuración ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.geometry("500x420")
ventana.title("Registrar Venta - Instructor")

# ------------------ Conexión a la BD ------------------
conn = sqlite3.connect("gimnasio.db")
cursor = conn.cursor()

def obtener_instructores():
    cursor.execute("SELECT cod_instructor, nombre || ' ' || apellido_1 || ' ' || apellido_2 FROM instructores")
    return cursor.fetchall()

instructores = obtener_instructores()
opciones = [f"{cod} - {nombre}" for cod, nombre in instructores]

# ------------------ Función para registrar y firmar ------------------
def registrar_venta():
    try:
        seleccion = combo_instructores.get()
        if not seleccion:
            raise ValueError("Debe seleccionar un instructor.")

        cod_instructor = int(seleccion.split(" - ")[0])
        cod_venta = int(entry_cod_venta.get())
        valor = float(entry_valor.get())

        # Generar texto para firma
        texto = f"cod_venta: {cod_venta}\ncod_instructor: {cod_instructor}\nvalor_venta: {valor}"
        firma = firma_ecdsa.firmar_datos(texto.encode())  # Firma en binario o base64

        # Insertar en la base de datos
        cursor.execute("""
            INSERT INTO ventasInstructores (cod_venta, cod_instructor, valor_venta)
            VALUES (?, ?, ?)
        """, (cod_venta, cod_instructor, valor))
        conn.commit()

        # Guardar la firma en archivo
        with open("firmas_ventas_instructores.txt", "ab") as archivo:
            archivo.write(firma + b"\n")
            archivo.write(texto.encode() + b"\n")
            archivo.write(b"---\n")

        messagebox.showinfo("Éxito", f"Venta registrada y firmada correctamente para instructor {cod_instructor}.")
        entry_cod_venta.delete(0, 'end')
        entry_valor.delete(0, 'end')

    except ValueError as e:
        messagebox.showerror("Error de entrada", str(e))
    except sqlite3.IntegrityError as e:
        messagebox.showerror("Error en BD", f"Error al insertar: {e}")

# ------------------ Interfaz ------------------
titulo = ctk.CTkLabel(ventana, text="Registrar Venta para Instructor", font=ctk.CTkFont(size=20, weight="bold"))
titulo.pack(pady=20)

combo_instructores = ctk.CTkComboBox(ventana, values=opciones, width=300)
combo_instructores.pack(pady=10)

entry_cod_venta = ctk.CTkEntry(ventana, placeholder_text="Código de Venta (único)")
entry_valor = ctk.CTkEntry(ventana, placeholder_text="Valor de la Venta (ej. 50000.00)")

entry_cod_venta.pack(pady=10)
entry_valor.pack(pady=10)

boton_guardar = ctk.CTkButton(ventana, text="Registrar Venta", command=registrar_venta)
boton_guardar.pack(pady=20)

ventana.mainloop()
