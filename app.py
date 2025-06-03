# app.py
import subprocess

# Verificamos si FFmpeg está instalado
try:
    subprocess.run(
        ["ffmpeg", "-version"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
except FileNotFoundError:
    print("\nERROR: FFmpeg no está instalado o no está en el PATH")
    print("Descarga FFmpeg desde: https://ffmpeg.org/download.html")
    print("Guía de instalación: https://windowsloop.com/install-ffmpeg-windows-10/")
    exit(1)

import os
from flask import Flask
from dotenv import load_dotenv

# 1. Cargamos variables de entorno desde .env
load_dotenv()

# 2. Creamos la aplicación Flask
app = Flask(__name__)

# 3. Importamos rutas (deben ir después de crear 'app' para evitar bucles de import)
from routes.product_routes import product_bp

# 4. Registramos el Blueprint de productos en la app
app.register_blueprint(product_bp, url_prefix="/api")

# 5. Punto de ejecución
if __name__ == "__main__":
    # Obtenemos el puerto de entorno o usamos 5000 por defecto
    port = int(os.getenv("PORT", 5000))
    # Ejecutamos la app en modo debug para desarrollo
    app.run(host="0.0.0.0", port=port, debug=True)
