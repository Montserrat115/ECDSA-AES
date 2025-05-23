-- Organizacion Sugerida
/proyecto_gimnasio/
│
<<<<<<< HEAD
├── menu_principal.py       ← Este archivo
├── registro_usuario.py     ← Ya hecho
├── venta_instructor.py     ← Ya hecho
├── verificar_firmas.py     ← Ya hecho
=======
├── menu_principal.py ← Este archivo
├── registro_usuario.py ← Ya hecho
├── venta_instructor.py ← Ya hecho
├── verificar_firmas.py ← Ya hecho
>>>>>>> 4216198 (Hola)
├── firma_ecdsa.py
├── cifrado_aes.py
├── gimnasio.db
└── firmas_ventas_instructores.txt

<<<<<<< HEAD
Para almacenar la huella digital y los datos de la tarjeta de crédito o débito de un cliente, debes tener en cuenta tanto el diseño de la 
=======
Para almacenar la huella digital y los datos de la tarjeta de crédito o débito de un cliente, debes tener en cuenta tanto el diseño de la
>>>>>>> 4216198 (Hola)
base de datos como los aspectos legales y de seguridad (como el cumplimiento de normativas como PCI DSS para tarjetas y protección de datos biométricos).

🔒 Consideraciones de Seguridad (antes del SQL)
Huella digital: Nunca se debe almacenar la imagen cruda de la huella, sino una plantilla biométrica cifrada generada por el lector.

<<<<<<< HEAD
Tarjeta: No almacenes directamente el número completo, CVV o la fecha de expiración sin cifrado. 
Idealmente almacenas un token (si usas un proveedor de pagos) o los últimos 4 dígitos para referencia.

---
=======
Tarjeta: No almacenes directamente el número completo, CVV o la fecha de expiración sin cifrado.
Idealmente almacenas un token (si usas un proveedor de pagos) o los últimos 4 dígitos para referencia.

---

>>>>>>> 4216198 (Hola)
El archivo firmas_ventas_instructores.txt contiene:
<firma en base64 o binario>
cod_venta: 123456
cod_instructor: 1
valor_venta: 50000.0
<<<<<<< HEAD
---

=======

---
>>>>>>> 4216198 (Hola)

Verificar la firma digital asegura que los datos no fueron alterados desde que se firmaron. Usamos el mismo módulo firma_ecdsa (que debe tener una función verificar_firma(firma, datos)).
<firma base64>
cod_venta: 123
cod_instructor: 1
valor_venta: 50000.0
<<<<<<< HEAD
---

=======

---
>>>>>>> 4216198 (Hola)
