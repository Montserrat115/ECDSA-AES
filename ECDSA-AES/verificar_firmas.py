import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
import firma_ecdsa  # tu módulo con verificar_firma()
import base64

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def cargar_y_verificar():
    archivo = filedialog.askopenfilename(title="Abrir archivo de firmas",
                                         filetypes=[("Archivos de texto", "*.txt")])
    if not archivo:
        return

    try:
        with open(archivo, "rb") as f:
            contenido = f.read().split(b"---\n")

        resultados = []
        for bloque in contenido:
            if not bloque.strip():
                continue
            lineas = bloque.strip().split(b"\n")
            firma = lineas[0]
            datos = b"\n".join(lineas[1:])

            es_valida = firma_ecdsa.verificar_firma(firma, datos)
            estado = "✅ Firma válida" if es_valida else "❌ Firma NO válida"

            texto_mostrar = datos.decode() + "\n" + estado + "\n" + "-"*40
            resultados.append(texto_mostrar)

        text_area.delete("1.0", ctk.END)
        text_area.insert(ctk.END, "\n".join(resultados))

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo verificar: {e}")

# Interfaz principal
ventana = ctk.CTk()
ventana.title("Verificar Firmas de Ventas")
ventana.geometry("600x500")

titulo = ctk.CTkLabel(ventana, text="Verificar Firmas de Ventas de Instructores", font=ctk.CTkFont(size=20, weight="bold"))
titulo.pack(pady=15)

btn_cargar = ctk.CTkButton(ventana, text="Cargar archivo de firmas y verificar", command=cargar_y_verificar)
btn_cargar.pack(pady=10)

text_area = ctk.CTkTextbox(ventana, width=560, height=350)
text_area.pack(padx=10, pady=10)

ventana.mainloop()
