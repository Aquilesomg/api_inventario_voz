-- sql/create_db.sql

-- 1. Crear base de datos
CREATE DATABASE IF NOT EXISTS inventario CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE inventario;

-- 2. Crear tabla productos
DROP TABLE IF EXISTS productos;
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    cantidad INT NOT NULL DEFAULT 0,
    precio DECIMAL(10,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Insertar datos de ejemplo
INSERT INTO productos (nombre, cantidad, precio) VALUES
  ('atún', 42, 1.50),
  ('arroz', 23, 0.99),
  ('leche entera', 2, 1.20),
  ('harina', 3, 0.80),
  ('queso', 10, 2.50);
