import os 
from flask import Flask, request, jsonify
from flask_cors import CORS

from restaurante_db import crear_base_datos, guardar_pedido
from enviar_correo import enviar_correo_confirmacion

app = Flask(__name__)
CORS(app)

crear_base_datos()


@app.route("/pedidos", methods=["POST"])
def crear_pedido():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser un JSON válido."}), 400

    nombre = (data.get("nombre") or "").strip()
    correo = (data.get("correo") or "").strip()
    item = (data.get("item") or "").strip()
    cantidad_raw = data.get("cantidad")

    campos_faltantes = []
    if not nombre:
        campos_faltantes.append("nombre")
    if not correo:
        campos_faltantes.append("correo")
    if not item:
        campos_faltantes.append("item")
    if cantidad_raw is None:
        campos_faltantes.append("cantidad")

    if campos_faltantes:
        return (
            jsonify(
                {
                    "error": "Faltan campos requeridos o están vacíos.",
                    "campos_faltantes": campos_faltantes,
                }
            ),
            400,
        )

    try:
        cantidad = int(cantidad_raw)
        if cantidad < 1:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "La cantidad debe ser un número entero válido mayor a 0."}), 400

    pedido_id = guardar_pedido(
        nombre_cliente=nombre,
        correo_cliente=correo,
        item_menu=item,
        cantidad=cantidad
    )

    if pedido_id is None:
        return jsonify({"error": "Ocurrió un error al guardar el pedido."}), 500

    item_con_cantidad = f"{cantidad}x {item}"

    try:
        correo_enviado = enviar_correo_confirmacion(
            correo_cliente=correo,
            nombre_cliente=nombre,
            item_menu=item_con_cantidad,
        )
    except Exception as e:
        print(f"Advertencia: Falló el envío de correo, pero el pedido se guardó. Detalle: {e}")
        correo_enviado = False

    return (
        jsonify(
            {
                "mensaje": "Pedido creado exitosamente.",
                "id": pedido_id,
                "correo_confirmacion_enviado": correo_enviado,
            }
        ),
        201,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
