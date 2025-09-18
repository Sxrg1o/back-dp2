#!/usr/bin/env python3
"""
Script para diagnosticar problemas de base de datos en el microservicio de menú.
"""

import sqlite3
import os
import sys
from pathlib import Path

def check_database_file():
    """Verifica si el archivo de base de datos existe y es válido."""
    db_path = "menu.db"
    
    print("🗄️ DIAGNÓSTICO DE BASE DE DATOS")
    print("="*50)
    
    # Verificar si el archivo existe
    if not os.path.exists(db_path):
        print(f"❌ Archivo de base de datos no encontrado: {db_path}")
        print("💡 Solución: Ejecutar el microservicio para crear la base de datos")
        return False
    
    # Verificar tamaño del archivo
    file_size = os.path.getsize(db_path)
    print(f"📁 Archivo encontrado: {db_path}")
    print(f"📏 Tamaño: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    
    if file_size == 0:
        print("❌ Archivo de base de datos está vacío")
        return False
    
    return True

def check_database_structure():
    """Verifica la estructura de la base de datos."""
    db_path = "menu.db"
    
    print(f"\n🏗️ ESTRUCTURA DE LA BASE DE DATOS")
    print("="*50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener lista de tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📋 Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"   • {table[0]}")
        
        # Verificar tablas específicas
        expected_tables = ['items', 'ingredientes', 'platos', 'bebidas', 'item_etiquetas', 'item_ingrediente']
        missing_tables = []
        
        table_names = [table[0] for table in tables]
        for expected in expected_tables:
            if expected not in table_names:
                missing_tables.append(expected)
        
        if missing_tables:
            print(f"\n❌ Tablas faltantes: {', '.join(missing_tables)}")
            print("💡 Solución: Ejecutar el microservicio para crear las tablas")
        else:
            print(f"\n✅ Todas las tablas esperadas están presentes")
        
        return len(missing_tables) == 0
        
    except sqlite3.Error as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def check_data_content():
    """Verifica el contenido de datos en la base de datos."""
    db_path = "menu.db"
    
    print(f"\n📊 CONTENIDO DE DATOS")
    print("="*50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Contar registros en cada tabla
        tables_to_check = [
            ('items', 'Ítems del menú'),
            ('ingredientes', 'Ingredientes'),
            ('platos', 'Platos'),
            ('bebidas', 'Bebidas'),
            ('item_etiquetas', 'Etiquetas de ítems'),
            ('item_ingrediente', 'Relaciones ítem-ingrediente')
        ]
        
        total_records = 0
        for table, description in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   {description}: {count:,} registros")
                total_records += count
            except sqlite3.Error as e:
                print(f"   {description}: ❌ Error - {e}")
        
        print(f"\n📈 Total de registros: {total_records:,}")
        
        if total_records == 0:
            print("⚠️ La base de datos está vacía")
            print("💡 Solución: Ejecutar el script de datos de prueba")
            return False
        else:
            print("✅ La base de datos contiene datos")
            return True
            
    except sqlite3.Error as e:
        print(f"❌ Error al verificar datos: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def check_specific_data():
    """Verifica datos específicos importantes."""
    db_path = "menu.db"
    
    print(f"\n🔍 VERIFICACIÓN DE DATOS ESPECÍFICOS")
    print("="*50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar ítems con ingredientes
        cursor.execute("""
            SELECT i.id, i.descripcion, COUNT(ii.ingrediente_id) as ingredientes_count
            FROM items i
            LEFT JOIN item_ingrediente ii ON i.id = ii.item_id
            GROUP BY i.id, i.descripcion
            ORDER BY ingredientes_count DESC
            LIMIT 5
        """)
        
        items_with_ingredients = cursor.fetchall()
        
        print("🍽️ Ítems con más ingredientes:")
        for item_id, desc, count in items_with_ingredients:
            print(f"   • {desc} (ID: {item_id}) - {count} ingredientes")
        
        # Verificar ingredientes más usados
        cursor.execute("""
            SELECT ing.nombre, COUNT(ii.item_id) as items_count
            FROM ingredientes ing
            LEFT JOIN item_ingrediente ii ON ing.id = ii.ingrediente_id
            GROUP BY ing.id, ing.nombre
            ORDER BY items_count DESC
            LIMIT 5
        """)
        
        popular_ingredients = cursor.fetchall()
        
        print("\n🥬 Ingredientes más populares:")
        for nombre, count in popular_ingredients:
            print(f"   • {nombre} - usado en {count} ítems")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error al verificar datos específicos: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def suggest_solutions():
    """Sugiere soluciones basadas en los problemas encontrados."""
    print(f"\n💡 SOLUCIONES RECOMENDADAS")
    print("="*50)
    
    print("1. 🚀 Iniciar el microservicio:")
    print("   python main.py")
    print("   # o")
    print("   uvicorn main:app --host 0.0.0.0 --port 8002")
    
    print("\n2. 🌱 Cargar datos de prueba:")
    print("   python create_peru_data_simple.py")
    print("   # o")
    print("   curl -X POST http://localhost:8002/seed-data")
    
    print("\n3. 🧪 Probar endpoints:")
    print("   python quick_test.py")
    print("   # o")
    print("   python test_all_endpoints.py")
    
    print("\n4. 📚 Ver documentación:")
    print("   http://localhost:8002/docs")

def main():
    """Función principal de diagnóstico."""
    print("🔧 DIAGNÓSTICO DE BASE DE DATOS - MICROSERVICIO DE MENÚ")
    print("="*70)
    
    # Cambiar al directorio del microservicio
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print(f"📁 Directorio de trabajo: {os.getcwd()}")
    
    # Ejecutar diagnósticos
    file_ok = check_database_file()
    if not file_ok:
        suggest_solutions()
        return
    
    structure_ok = check_database_structure()
    if not structure_ok:
        suggest_solutions()
        return
    
    data_ok = check_data_content()
    if not data_ok:
        suggest_solutions()
        return
    
    check_specific_data()
    
    print(f"\n✅ DIAGNÓSTICO COMPLETADO")
    print("="*50)
    print("🎉 La base de datos parece estar funcionando correctamente")
    print("💡 Si los endpoints siguen fallando, verifica que el microservicio esté ejecutándose")

if __name__ == "__main__":
    main()
