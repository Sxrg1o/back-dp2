#!/usr/bin/env python3
"""
Script de migración para agregar fecha_inicio y fecha_fin a sesiones
"""
import sqlite3
import os
from pathlib import Path

# Ruta de la base de datos
DB_PATH = Path(__file__).parent.parent / "restaurant.db"

def run_migration():
    """Ejecuta la migración para agregar las columnas."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Agregar fecha_inicio
        try:
            cursor.execute("ALTER TABLE sesiones ADD COLUMN fecha_inicio DATETIME NULL")
            print("✓ Columna fecha_inicio agregada")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("⚠ Columna fecha_inicio ya existe")
            else:
                raise
        
        # Agregar fecha_fin
        try:
            cursor.execute("ALTER TABLE sesiones ADD COLUMN fecha_fin DATETIME NULL")
            print("✓ Columna fecha_fin agregada")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("⚠ Columna fecha_fin ya existe")
            else:
                raise
        
        # Actualizar sesiones existentes
        cursor.execute("""
            UPDATE sesiones 
            SET fecha_inicio = fecha_creacion 
            WHERE estado = 'ACTIVO' AND fecha_inicio IS NULL
        """)
        rows_updated = cursor.rowcount
        print(f"✓ {rows_updated} sesiones activas actualizadas con fecha_inicio")
        
        conn.commit()
        conn.close()
        print("\n✓ Migración completada exitosamente")
        return 0
        
    except Exception as e:
        print(f"\n✗ Error en migración: {e}")
        return 1

if __name__ == "__main__":
    exit(run_migration())
