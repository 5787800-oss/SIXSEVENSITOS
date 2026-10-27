import os
import mysql.connector
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


def obtener_conexion():
    """Crea y retorna la conexión a la base de datos MySQL local."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Coloca tu contraseña de MySQL si configuraste una
        database="sixsevensitos",
        port=3306,
    )


def crear_base_datos() -> None:
    """Crea la tabla 'pedidos' si no existe en MySQL."""
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pedidos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Nombre VARCHAR(255) NOT NULL,
                correo_cliente VARCHAR(255) NOT NULL,
                Item_menu VARCHAR(255) NOT NULL,
                Cantidad INT NOT NULL DEFAULT 1,
                total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                Fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Tabla 'pedidos' verificada/creada correctamente.")
    except mysql.connector.Error as e:
        print(f"Error al crear la tabla: {e}")


def guardar_pedido(
    nombre_cliente: str,
    correo_cliente: str,
    item_menu: str,
    cantidad: int,
    total: float = 0.0,
) -> Optional[int]:
    """Inserta un nuevo pedido en MySQL y retorna su ID."""
    conn = None
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = """
            INSERT INTO pedidos (Nombre, correo_cliente, Item_menu, Cantidad, total)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre_cliente, correo_cliente, item_menu, cantidad, total)
        cursor.execute(sql, valores)
        conn.commit()
        
        # En MySQL obtenemos el ID recién generado con lastrowid
        pedido_id = cursor.lastrowid
        cursor.close()
        return pedido_id
    except mysql.connector.Error as e:
        print(f"Error al guardar el pedido: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    crear_base_datos()

    nuevo_id = guardar_pedido(
        nombre_cliente="Juan Pérez",
        correo_cliente="juan.perez@example.com",
        item_menu="Iced Caramel Macchiato",
        cantidad=2,
        total=12.50,
    )

    if nuevo_id is not None:
        print(f"Pedido guardado exitosamente con id: {nuevo_id}")
    else:
        print("No se pudo guardar el pedido.")