# routes/product_routes.py
from flask import Blueprint, send_file
from controllers.product_controller import handle_audio_query, handle_text_query

# 1. Definimos un Blueprint para agrupar rutas de productos
product_bp = Blueprint("product_bp", __name__)

# 2. Ruta: POST /api/consultar-audio
@product_bp.route("/consultar-audio", methods=["POST"])
def consultar_audio():
    return handle_audio_query()

# 3. Para servir el archivo de audio generado (GET /api/audio?n=file_path)
@product_bp.route("/audio", methods=["GET"])
def get_audio():
    """
    Recibe query param ?n=<ruta_audio> y devuelve el archivo MP3 para reproducirlo.
    Ejemplo: /api/audio?n=uploads/respuesta123.mp3
    """
    from flask import request
    audio_path = request.args.get("n")
    if not audio_path:
        return {"error": "No se proporcionó la ruta del audio"}, 400
    try:
        return send_file(audio_path, mimetype="audio/mpeg", as_attachment=False)
    except Exception:
        return {"error": "No se encontró el archivo de audio"}, 404

# 4. Ruta: GET /api/producto/<nombre>
@product_bp.route("/producto/<nombre>", methods=["GET"])
def producto_texto(nombre):
    return handle_text_query(nombre)
