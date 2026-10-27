import os
import requests
from datetime import datetime

BREVO_API_KEY = os.environ.get("BREVO_API_KEY")

NOMBRE_RESTAURANTE = "Restaurante Sabor Local"
CORREO_REMITENTE = "adrianmonroy4023@gmail.com" 


def _construir_html_factura(nombre_cliente: str, item_menu: str) -> str:
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

    return f"""\
    <html>
      <body style="margin:0; padding:0; background-color:#f4f4f7; font-family: Arial, Helvetica, sans-serif;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f7; padding:30px 0;">
          <tr>
            <td align="center">
              <table role="presentation" width="480" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,0.08);">
                <tr>
                  <td style="background-color:#2f6f4e; padding:24px; text-align:center;">
                    <h1 style="color:#ffffff; margin:0; font-size:22px;">{NOMBRE_RESTAURANTE}</h1>
                    <p style="color:#dcefe3; margin:4px 0 0; font-size:13px;">Confirmación de pedido</p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:28px 32px;">
                    <p style="font-size:15px; color:#333333; margin:0 0 12px;">
                      ¡Hola, <strong>{nombre_cliente}</strong>!
                    </p>
                    <p style="font-size:14px; color:#555555; margin:0 0 20px;">
                      Gracias por tu compra. Hemos recibido tu pedido correctamente.
                      Aquí tienes el detalle de tu recibo:
                    </p>

                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e5e5e5; border-radius:6px; margin-bottom:20px;">
                      <tr style="background-color:#f9f9f9;">
                        <td style="padding:10px 14px; font-size:13px; color:#888888;">Ítem</td>
                        <td style="padding:10px 14px; font-size:13px; color:#888888; text-align:right;">Fecha</td>
                      </tr>
                      <tr>
                        <td style="padding:12px 14px; font-size:14px; color:#333333; border-top:1px solid #eeeeee;">
                          {item_menu}
                        </td>
                        <td style="padding:12px 14px; font-size:14px; color:#333333; border-top:1px solid #eeeeee; text-align:right;">
                          {fecha_actual}
                        </td>
                      </tr>
                    </table>

                    <p style="font-size:13px; color:#999999; margin:0 0 4px;">
                      Si tienes alguna pregunta sobre tu pedido, simplemente responde a este correo.
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """

def enviar_correo_confirmacion(correo_cliente: str, nombre_cliente: str, item_menu: str) -> bool:
    if not BREVO_API_KEY:
        print("Advertencia: BREVO_API_KEY no está configurada.")
        return False

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }
    
    payload = {
        "sender": {"name": NOMBRE_RESTAURANTE, "email": CORREO_REMITENTE},
        "to": [{"email": correo_cliente, "name": nombre_cliente}],
        "subject": f"✅ Confirmación de tu pedido en {NOMBRE_RESTAURANTE}",
        "htmlContent": _construir_html_factura(nombre_cliente, item_menu)
    }

    try:
        respuesta = requests.post(url, json=payload, headers=headers)
        if respuesta.status_code == 201:
            print("Correo enviado exitosamente a través de Brevo.")
            return True
        else:
            print(f"Error de Brevo: {respuesta.status_code} - {respuesta.text}")
            return False
    except Exception as e:
        print(f"Error de conexión con Brevo: {e}")
        return False
