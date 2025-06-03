# services/intent_service.py
import re
import string

def parse_intent(transcribed_text):
    """
    Analiza el texto transcrito y devuelve un diccionario con:
    {
      "action": "consultar_stock" | "consultar_precio" | "descuento" | "precio_nuevo" | "low_stock" | "unknown",
      "product": "<nombre_producto>" | None,
      "value": <número>  # opcional, por ejemplo, porcentaje o nuevo precio
    }
    """
    text = transcribed_text.lower()

    # 1. Intento “¿Cuánto hay de X?” → consultar_stock
    match_stock = re.search(r"cuánto (hay|tiene).*(de )?(.+?)[\?\.]?$", text)
    if match_stock:
        product = match_stock.group(3).strip().strip(string.punctuation)
        return {"action": "consultar_stock", "product": product}

    # 2. Intento “¿Cuál es el precio (de)? X?” → consultar_precio
    match_price = re.search(r"precio (de )?(.+)\??", text)
    if match_price:
        product = match_price.group(2).strip().strip(string.punctuation)
        return {"action": "consultar_precio", "product": product}

    # 3. Intento “bájale el precio a X a Y” → precio_nuevo
    match_new_price = re.search(r"baj(a|arle).*(precio).*(a )?(.+?) a (\d+(\.\d+)?)", text)
    if match_new_price:
        product = match_new_price.group(4).strip().strip(string.punctuation)
        new_price = float(match_new_price.group(5))
        return {"action": "precio_nuevo", "product": product, "value": new_price}

    # 4. Intento “descuento X% a Y” → descuento
    match_discount = re.search(r"(\d+(\.\d+)?)\s*%\s*(descuento|rebaja).*(a )?(.+)", text)
    if match_discount:
        percentage = float(match_discount.group(1))
        product = match_discount.group(5).strip().strip(string.punctuation)
        return {"action": "descuento", "product": product, "value": percentage}

    # 5. Intento “qué productos (se están) acabando” → low_stock
    match_low_stock = re.search(r"(acabando|bajo stock|poco).*(productos|inventario)", text)
    if match_low_stock:
        return {"action": "low_stock", "product": None}

    # 6. No coincide con nada → acción desconocida
    return {"action": "unknown", "product": None}
