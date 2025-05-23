import customtkinter as ctk
from tkinter import messagebox
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sistema de Gestión - Gimnasio")
app.geometry("500x400")

# ---------------- Funciones para lanzar scripts externos ----------------
def abrir_registro_usuario():
    try:
        subprocess.Popen(["python", "registro_usuario.py"])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el registro: {e}")

def abrir_venta_instructor():
    try:
        subprocess.Popen(["python", "venta_instructor.py"])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir venta de instructor: {e}")

def abrir_verificacion():
    try:
        subprocess.Popen(["python", "verificar_firmas.py"])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir verificación: {e}")

# ---------------- UI Principal ----------------
titulo = ctk.CTkLabel(app, text="Menú Principal del Gimnasio", font=ctk.CTkFont(size=22, weight="bold"))
titulo.pack(pady=40)

btn_registro = ctk.CTkButton(app, text="📋 Registrar Usuario", width=250, command=abrir_registro_usuario)
btn_venta = ctk.CTkButton(app, text="💰 Registrar Venta a Instructor", width=250, command=abrir_venta_instructor)
btn_verificar = ctk.CTkButton(app, text="✅ Verificar Firmas de Ventas", width=250, command=abrir_verificacion)

btn_registro.pack(pady=15)
btn_venta.pack(pady=15)
btn_verificar.pack(pady=15)

app.mainloop()
