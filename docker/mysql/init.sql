-- Initial database setup for Restaurant Backend
-- This script runs when the MySQL container starts for the first time

USE restaurant_db;

-- Create default roles
INSERT IGNORE INTO rol (id, nombre, descripcion, created_at, updated_at) VALUES
(1, 'admin', 'Administrator with full access', NOW(), NOW()),
(2, 'mesero', 'Waiter/Server role', NOW(), NOW()),
(3, 'cocina', 'Kitchen staff role', NOW(), NOW()),
(4, 'cliente', 'Customer role', NOW(), NOW());

-- Create default admin user (password: admin123)
-- Hash generated with bcrypt for 'admin123'
INSERT IGNORE INTO usuario (id, id_rol, email, password_hash, nombre, activo, created_at, updated_at) VALUES
(1, 1, 'admin@restaurant.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/jGGJNjj5w9gJKQ5ZO', 'Administrator', 1, NOW(), NOW());

-- Create sample categories
INSERT IGNORE INTO categoria (id, nombre, descripcion, orden, activo, created_at, updated_at) VALUES
(1, 'Entradas', 'Aperitivos y entradas', 1, 1, NOW(), NOW()),
(2, 'Platos Principales', 'Platos principales del menú', 2, 1, NOW(), NOW()),
(3, 'Postres', 'Postres y dulces', 3, 1, NOW(), NOW()),
(4, 'Bebidas', 'Bebidas frías y calientes', 4, 1, NOW(), NOW());

-- Create sample allergens
INSERT IGNORE INTO alergeno (id, nombre, descripcion, nivel_riesgo, activo, orden, created_at, updated_at) VALUES
(1, 'Gluten', 'Proteína presente en trigo, cebada y centeno', 'alto', 1, 1, NOW(), NOW()),
(2, 'Lácteos', 'Leche y productos derivados', 'medio', 1, 2, NOW(), NOW()),
(3, 'Frutos Secos', 'Nueces, almendras, avellanas, etc.', 'alto', 1, 3, NOW(), NOW()),
(4, 'Mariscos', 'Crustáceos y moluscos', 'critico', 1, 4, NOW(), NOW()),
(5, 'Huevos', 'Huevos y productos que los contengan', 'medio', 1, 5, NOW(), NOW());

-- Create sample tables
INSERT IGNORE INTO mesa (id, numero, capacidad, zona, qr_code, estado, activa, created_at, updated_at) VALUES
(1, 'M01', 4, 'Salon Principal', 'QR_MESA_01', 'disponible', 1, NOW(), NOW()),
(2, 'M02', 2, 'Salon Principal', 'QR_MESA_02', 'disponible', 1, NOW(), NOW()),
(3, 'M03', 6, 'Terraza', 'QR_MESA_03', 'disponible', 1, NOW(), NOW()),
(4, 'M04', 4, 'Terraza', 'QR_MESA_04', 'disponible', 1, NOW(), NOW()),
(5, 'M05', 8, 'Salon VIP', 'QR_MESA_05', 'disponible', 1, NOW(), NOW());