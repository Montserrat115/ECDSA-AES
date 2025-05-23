import sqlite3
from datetime import datetime
import random

# Conexión a la base de datos
conn = sqlite3.connect("gimnasio.db")
cursor = conn.cursor()

def procesar_pagos_mensuales():
    hoy = datetime.today()

    # Seleccionamos clientes cuyo día de inscripción es hoy (por día, no mes/año)
    cursor.execute("""
        SELECT cedula, tarjeta_token, tarjeta_ultimos4, fecha_inscripcion
        FROM cliente
        WHERE strftime('%d', fecha_inscripcion) = ?
    """, (hoy.strftime("%d"),))

    clientes = cursor.fetchall()

    for cliente in clientes:
        cedula, token, ult4, fecha_inscripcion = cliente
        valor = 30000.00  # Valor fijo o dinámico según membresía

        if not token:
            print(f"[X] Cliente {cedula} no tiene tarjeta registrada.")
            continue

        # Simulamos cobro con el token (en sistemas reales, aquí va la API de Stripe/MercadoPago)
        print(f"[✓] Cobro simulado a tarjeta ****{ult4} del cliente {cedula}")

        # Registrar el pago en la base de datos
        cod_venta = random.randint(100000, 999999)  # En sistemas reales usar autoincremental o secuencia
        cursor.execute("""
            INSERT INTO pagoMensualidad (cod_venta, cedula_cliente, fecha_venta, valor_venta)
            VALUES (?, ?, ?, ?)
        """, (cod_venta, cedula, hoy.strftime("%Y-%m-%d"), valor))

        conn.commit()

        print(f"[+] Pago registrado: cod_venta={cod_venta}, cliente={cedula}, valor=${valor:.2f}")

procesar_pagos_mensuales()
