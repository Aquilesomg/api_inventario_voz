# models/db.py
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# 1. Cargamos variables de entorno
load_dotenv()

# 2. Función para crear una conexión a la base de datos
def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        return conn
    except Error as e:
        print("Error al conectar a MySQL:", e)
        return None

# 3. Función para obtener un producto por nombre (busca coincidencias parciales)
def get_product_by_name(product_name):
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor(dictionary=True)
    # Consulta parametrizada para evitar inyección
    query = "SELECT id, nombre, cantidad, precio FROM productos WHERE nombre LIKE %s LIMIT 1"
    cursor.execute(query, ("%" + product_name + "%",))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# 4. Función para obtener productos con stock bajo (< umbral)
def get_low_stock(threshold=5):
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, nombre, cantidad, precio FROM productos WHERE cantidad < %s"
    cursor.execute(query, (threshold,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# 5. Función para actualizar el precio de un producto dado su id
def update_product_price(product_id, new_price):
    conn = get_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    query = "UPDATE productos SET precio = %s WHERE id = %s"
    cursor.execute(query, (new_price, product_id))
    conn.commit()
    cursor.close()
    conn.close()
    return True

# 6. Función para agregar cantidad al stock de un producto
def update_product_stock(product_id, new_stock):
    conn = get_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    query = "UPDATE productos SET cantidad = %s WHERE id = %s"
    cursor.execute(query, (new_stock, product_id))
    conn.commit()
    cursor.close()
    conn.close()
    return True
