-- Migración: Agregar campos fecha_inicio y fecha_fin a la tabla sesiones
-- Fecha: 2025-11-10
-- Descripción: Agrega campos para rastrear el inicio y fin de las sesiones

-- Agregar columna fecha_inicio
ALTER TABLE sesiones 
ADD COLUMN fecha_inicio DATETIME NULL 
COMMENT 'Fecha y hora de inicio de la sesión';

-- Agregar columna fecha_fin
ALTER TABLE sesiones 
ADD COLUMN fecha_fin DATETIME NULL 
COMMENT 'Fecha y hora de fin de la sesión';

-- Actualizar sesiones existentes con estado activo para tener fecha_inicio
UPDATE sesiones 
SET fecha_inicio = fecha_creacion 
WHERE estado = 'ACTIVO' AND fecha_inicio IS NULL;
