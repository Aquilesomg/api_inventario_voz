# controllers/product_controller.py
import os
from flask import request, jsonify, send_file
from models.db import get_product_by_name, get_low_stock, update_product_price
from services.voice_service import voice_service  # ✅ correcto
from services.intent_service import parse_intent

# 1. Endpoint: /api/consultar-audio (método POST)
def handle_audio_query():
    """
    Recibe un archivo de audio, lo transcribe, analiza la intención,
    consulta la base de datos y genera respuesta de texto y audio.
    """
    if "audio" not in request.files:
        return jsonify({"error": "No se encontró el campo 'audio' en la petición"}), 400

    # 2. Guardamos el archivo en carpeta uploads
    audio_file = request.files["audio"]
    file_path = os.path.join("uploads", audio_file.filename)
    audio_file.save(file_path)

    # 3. Transcribimos el audio usando Whisper
    transcribed_text = voice_service.transcribe_audio(file_path)

    # 4. Analizamos la intención con nuestro servicio
    intent_data = parse_intent(transcribed_text)

    # Inicializamos respuesta por defecto
    response_text = ""
    audio_response_path = None

    # 5. Según la acción, ejecutamos distintas funciones
    action = intent_data["action"]
    product_name = intent_data.get("product")
    value = intent_data.get("value")

    # 5.a. Si quieren consultar stock
    if action == "consultar_stock":
        product = get_product_by_name(product_name)
        if product:
            response_text = f"El stock de {product['nombre']} es {product['cantidad']} unidades."
        else:
            response_text = f"No encontré el producto '{product_name}'."

    # 5.b. Si quieren consultar precio
    elif action == "consultar_precio":
        product = get_product_by_name(product_name)
        if product:
            response_text = f"El precio de {product['nombre']} es ${product['precio']:.2f}."
        else:
            response_text = f"No encontré el producto '{product_name}'."

    # 5.c. Si quieren actualizar precio directamente
    elif action == "precio_nuevo":
        product = get_product_by_name(product_name)
        if product:
            update_product_price(product["id"], value)
            response_text = f"Precio de {product['nombre']} actualizado a ${value:.2f}."
        else:
            response_text = f"No encontré el producto '{product_name}'."

    # 5.d. Si quieren aplicar descuento
    elif action == "descuento":
        product = get_product_by_name(product_name)
        if product:
            nuevo_precio = product["precio"] * (1 - value / 100)
            update_product_price(product["id"], round(nuevo_precio, 2))
            response_text = f"Se aplicó un {value:.0f}% de descuento a {product['nombre']}. Nuevo precio: ${nuevo_precio:.2f}."
        else:
            response_text = f"No encontré el producto '{product_name}'."

    # 5.e. Si quieren ver productos con bajo stock
    elif action == "low_stock":
        low_products = get_low_stock()
        if low_products:
            lista = ", ".join([f"{p['nombre']} ({p['cantidad']} unidades)" for p in low_products])
            response_text = f"Productos con bajo stock: {lista}."
        else:
            response_text = "No hay productos con stock bajo."

    # 5.f. Acción desconocida
    else:
        response_text = "Lo siento, no entendí tu solicitud."

    # 6. Generamos el audio de respuesta con gTTS
    audio_response_path = voice_service.text_to_speech(response_text, lang="es")

    # 7. Borramos el archivo de audio original (opcional)
    try:
        os.remove(file_path)
    except Exception:
        pass

    # 8. Enviamos JSON con texto y file_id para descargar audio
    #    Devolvemos el texto y la ruta al audio para que el cliente lo reproduzca
    return jsonify({
        "transcripcion": transcribed_text,
        "respuesta_texto": response_text,
        "audio_path": audio_response_path  # El cliente puede hacer send_file contra esta ruta
    }), 200

# 9. Endpoint: /api/producto/<nombre> (método GET)
def handle_text_query(nombre):
    """
    Recibe una consulta en texto (ej. GET /api/producto/arroz) y devuelve
    stock y precio del producto (por texto).
    """
    product = get_product_by_name(nombre)
    if product:
        return jsonify({
            "nombre": product["nombre"],
            "cantidad": product["cantidad"],
            "precio": float(product["precio"])
        }), 200
    else:
        return jsonify({"error": f"No encontré el producto '{nombre}'"}), 404
