import mysql.connector
from typing import Optional

# Configura los datos de tu conexión Ngrok / MySQL Local aquí:
NGROK_HOST = "0.tcp.ngrok.io"  # <-- Cambia esto por tu host de Ngrok
NGROK_PORT = 12345             # <-- Cambia esto por tu puerto de 5 dígitos de Ngrok
MYSQL_USER = "root"            # <-- Tu usuario de MySQL en XAMPP
MYSQL_PASSWORD = ""            # <-- Tu contraseña (déjala vacía "" si no usas)
MYSQL_DB = "tu_base_de_datos"  # <-- Pon el nombre EXACTO de tu BD en phpMyAdmin


def obtener_conexion():
    return mysql.connector.connect(
        host=NGROK_HOST,
        port=NGROK_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )


def crear_base_datos() -> None:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pedidos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_cliente VARCHAR(100) NOT NULL,
                correo_cliente VARCHAR(100) NOT NULL,
                item_menu VARCHAR(100) NOT NULL,
                cantidad INT NOT NULL DEFAULT 1,
                fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conexion.commit()
        cursor.close()
    finally:
        conexion.close()


def guardar_pedido(
    nombre_cliente: str,
    correo_cliente: str,
    item_menu: str,
    cantidad: int,
) -> Optional[int]:
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO pedidos (nombre_cliente, correo_cliente, item_menu, cantidad)
            VALUES (%s, %s, %s, %s)
            """,
            (nombre_cliente, correo_cliente, item_menu, cantidad),
        )
        conexion.commit()
        pedido_id = cursor.lastrowid
        cursor.close()
        conexion.close()
        return pedido_id
    except mysql.connector.Error as e:
        print(f"Error al guardar el pedido en MySQL: {e}")
        return None


if __name__ == "__main__":
    crear_base_datos()

    nuevo_id = guardar_pedido(
        nombre_cliente="Juan Pérez",
        correo_cliente="juan.perez@example.com",
        item_menu="Iced Caramel Macchiato",
        cantidad=2,
    )

    if nuevo_id is not None:
        print(f"Pedido guardado exitosamente con id: {nuevo_id}")
    else:
        print("No se pudo guardar el pedido.")
