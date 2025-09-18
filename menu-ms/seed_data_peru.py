#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de prueba típicos de Perú.
Incluye platos, bebidas e ingredientes tradicionales peruanos.
"""

from decimal import Decimal
from domain.entities import Plato, Bebida, Ingrediente
from domain.entities.enums import EtiquetaItem, EtiquetaIngrediente, EtiquetaPlato
from infrastructure.db import get_db, create_tables
from infrastructure.repositories import (
    ItemRepositoryImpl, PlatoRepositoryImpl, BebidaRepositoryImpl,
    IngredienteRepositoryImpl
)
from application.services import ItemService, IngredienteService


def create_peruvian_ingredients():
    """Crea ingredientes típicos peruanos."""
    print("🥬 Creando ingredientes peruanos...")
    
    ingredientes = [
        # Verduras peruanas
        Ingrediente(
            nombre="Ají Amarillo",
            stock=Decimal('15.0'),
            peso=Decimal('0.05'),
            tipo=EtiquetaIngrediente.VERDURA
        ),
        Ingrediente(
            nombre="Rocoto",
            stock=Decimal('8.0'),
            peso=Decimal('0.03'),
            tipo=EtiquetaIngrediente.VERDURA
        ),
        Ingrediente(
            nombre="Cebolla Morada",
            stock=Decimal('20.0'),
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.VERDURA
        ),
        Ingrediente(
            nombre="Culantro",
            stock=Decimal('12.0'),
            peso=Decimal('0.01'),
            tipo=EtiquetaIngrediente.VERDURA
        ),
        Ingrediente(
            nombre="Huacatay",
            stock=Decimal('5.0'),
            peso=Decimal('0.01'),
            tipo=EtiquetaIngrediente.VERDURA
        ),
        Ingrediente(
            nombre="Papa Amarilla",
            stock=Decimal('30.0'),
            peso=Decimal('0.3'),
            tipo=EtiquetaIngrediente.VERDURA
        ),
        Ingrediente(
            nombre="Camote",
            stock=Decimal('25.0'),
            peso=Decimal('0.4'),
            tipo=EtiquetaIngrediente.VERDURA
        ),
        Ingrediente(
            nombre="Yuca",
            stock=Decimal('18.0'),
            peso=Decimal('0.5'),
            tipo=EtiquetaIngrediente.VERDURA
        ),
        
        # Carnes peruanas
        Ingrediente(
            nombre="Cuy",
            stock=Decimal('6.0'),
            peso=Decimal('0.8'),
            tipo=EtiquetaIngrediente.CARNE
        ),
        Ingrediente(
            nombre="Alpaca",
            stock=Decimal('4.0'),
            peso=Decimal('1.0'),
            tipo=EtiquetaIngrediente.CARNE
        ),
        Ingrediente(
            nombre="Pollo Criollo",
            stock=Decimal('15.0'),
            peso=Decimal('1.2'),
            tipo=EtiquetaIngrediente.CARNE
        ),
        Ingrediente(
            nombre="Pescado de Mar",
            stock=Decimal('12.0'),
            peso=Decimal('0.6'),
            tipo=EtiquetaIngrediente.CARNE
        ),
        Ingrediente(
            nombre="Cerdo",
            stock=Decimal('10.0'),
            peso=Decimal('0.8'),
            tipo=EtiquetaIngrediente.CARNE
        ),
        
        # Frutas peruanas
        Ingrediente(
            nombre="Lúcuma",
            stock=Decimal('8.0'),
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.FRUTA
        ),
        Ingrediente(
            nombre="Chirimoya",
            stock=Decimal('6.0'),
            peso=Decimal('0.3'),
            tipo=EtiquetaIngrediente.FRUTA
        ),
        Ingrediente(
            nombre="Granadilla",
            stock=Decimal('10.0'),
            peso=Decimal('0.1'),
            tipo=EtiquetaIngrediente.FRUTA
        ),
        Ingrediente(
            nombre="Aguaymanto",
            stock=Decimal('5.0'),
            peso=Decimal('0.02'),
            tipo=EtiquetaIngrediente.FRUTA
        ),
        Ingrediente(
            nombre="Maracuyá",
            stock=Decimal('7.0'),
            peso=Decimal('0.15'),
            tipo=EtiquetaIngrediente.FRUTA
        ),
        Ingrediente(
            nombre="Plátano de la Isla",
            stock=Decimal('20.0'),
            peso=Decimal('0.25'),
            tipo=EtiquetaIngrediente.FRUTA
        ),
    ]
    
    return ingredientes


def create_peruvian_platos():
    """Crea platos típicos peruanos."""
    print("🍽️ Creando platos peruanos...")
    
    platos = [
        # Entradas
        Plato(
            descripcion="Causa Limeña de Pollo",
            precio=Decimal('18.50'),
            peso=Decimal('250.0'),
            tipo=EtiquetaPlato.ENTRADA,
            valor_nutricional="Rica en carbohidratos, proteínas y vitaminas A y C",
            tiempo_preparacion=Decimal('30.0'),
            comentarios="Plato tradicional de la gastronomía peruana",
            receta="Cocinar papa amarilla, hacer puré, mezclar con ají amarillo, rellenar con pollo deshilachado",
            disponible=True,
            unidades_disponibles=12,
            num_ingredientes=6,
            kcal=320,
            calorias=Decimal('320.0'),
            proteinas=Decimal('18.0'),
            azucares=Decimal('8.0'),
            etiquetas=[EtiquetaItem.FRIO, EtiquetaItem.SIN_GLUTEN]
        ),
        
        Plato(
            descripcion="Anticuchos de Corazón",
            precio=Decimal('22.00'),
            peso=Decimal('200.0'),
            tipo=EtiquetaPlato.ENTRADA,
            valor_nutricional="Alto en proteínas y hierro",
            tiempo_preparacion=Decimal('45.0'),
            comentarios="Brochetas de corazón de res marinadas en ají panca",
            receta="Marinar corazón en ají panca, vinagre y especias, asar a la parrilla",
            disponible=True,
            unidades_disponibles=8,
            num_ingredientes=5,
            kcal=280,
            calorias=Decimal('280.0'),
            proteinas=Decimal('25.0'),
            azucares=Decimal('3.0'),
            etiquetas=[EtiquetaItem.CALIENTE, EtiquetaItem.PICANTE]
        ),
        
        # Platos principales
        Plato(
            descripcion="Ceviche de Pescado",
            precio=Decimal('28.00'),
            peso=Decimal('300.0'),
            tipo=EtiquetaPlato.FONDO,
            valor_nutricional="Rico en proteínas, omega-3 y vitamina C",
            tiempo_preparacion=Decimal('20.0'),
            comentarios="Plato bandera del Perú, pescado fresco marinado en leche de tigre",
            receta="Cortar pescado fresco, marinar en limón, ají, cebolla morada y culantro",
            disponible=True,
            unidades_disponibles=15,
            num_ingredientes=7,
            kcal=250,
            calorias=Decimal('250.0'),
            proteinas=Decimal('30.0'),
            azucares=Decimal('5.0'),
            etiquetas=[EtiquetaItem.FRIO, EtiquetaItem.ACIDO, EtiquetaItem.SIN_GLUTEN]
        ),
        
        Plato(
            descripcion="Lomo Saltado",
            precio=Decimal('32.50'),
            peso=Decimal('350.0'),
            tipo=EtiquetaPlato.FONDO,
            valor_nutricional="Alto en proteínas, carbohidratos y vitaminas",
            tiempo_preparacion=Decimal('25.0'),
            comentarios="Fusión peruano-china, lomo de res salteado con verduras",
            receta="Saltear lomo con cebolla, tomate, ají amarillo, servir con papas fritas y arroz",
            disponible=True,
            unidades_disponibles=10,
            num_ingredientes=8,
            kcal=580,
            calorias=Decimal('580.0'),
            proteinas=Decimal('35.0'),
            azucares=Decimal('12.0'),
            etiquetas=[EtiquetaItem.CALIENTE, EtiquetaItem.CON_GLUTEN]
        ),
        
        Plato(
            descripcion="Aji de Gallina",
            precio=Decimal('26.00'),
            peso=Decimal('320.0'),
            tipo=EtiquetaPlato.FONDO,
            valor_nutricional="Rico en proteínas y carbohidratos",
            tiempo_preparacion=Decimal('40.0'),
            comentarios="Pollo deshilachado en crema de ají amarillo",
            receta="Cocinar pollo, deshilachar, preparar crema con ají amarillo, leche y pan",
            disponible=True,
            unidades_disponibles=12,
            num_ingredientes=6,
            kcal=450,
            calorias=Decimal('450.0'),
            proteinas=Decimal('28.0'),
            azucares=Decimal('8.0'),
            etiquetas=[EtiquetaItem.CALIENTE, EtiquetaItem.PICANTE, EtiquetaItem.CON_GLUTEN]
        ),
        
        Plato(
            descripcion="Pachamanca",
            precio=Decimal('45.00'),
            peso=Decimal('500.0'),
            tipo=EtiquetaPlato.FONDO,
            valor_nutricional="Completo en proteínas, carbohidratos y minerales",
            tiempo_preparacion=Decimal('120.0'),
            comentarios="Cocción tradicional en piedras calientes bajo tierra",
            receta="Cocinar carnes, papas, camotes y habas en piedras calientes bajo tierra",
            disponible=True,
            unidades_disponibles=6,
            num_ingredientes=10,
            kcal=650,
            calorias=Decimal('650.0'),
            proteinas=Decimal('40.0'),
            azucares=Decimal('15.0'),
            etiquetas=[EtiquetaItem.CALIENTE, EtiquetaItem.SIN_GLUTEN]
        ),
        
        Plato(
            descripcion="Arroz con Pollo",
            precio=Decimal('24.00'),
            peso=Decimal('380.0'),
            tipo=EtiquetaPlato.FONDO,
            valor_nutricional="Balanceado en carbohidratos y proteínas",
            tiempo_preparacion=Decimal('35.0'),
            comentarios="Arroz verde con pollo, típico de la costa peruana",
            receta="Cocinar arroz con culantro, agregar pollo, arvejas y zanahoria",
            disponible=True,
            unidades_disponibles=14,
            num_ingredientes=7,
            kcal=520,
            calorias=Decimal('520.0'),
            proteinas=Decimal('32.0'),
            azucares=Decimal('10.0'),
            etiquetas=[EtiquetaItem.CALIENTE, EtiquetaItem.CON_GLUTEN]
        ),
        
        # Postres
        Plato(
            descripcion="Suspiro a la Limeña",
            precio=Decimal('12.00'),
            peso=Decimal('150.0'),
            tipo=EtiquetaPlato.POSTRE,
            valor_nutricional="Rico en azúcares y grasas",
            tiempo_preparacion=Decimal('30.0'),
            comentarios="Postre tradicional de Lima, manjar blanco con merengue",
            receta="Preparar manjar blanco, cubrir con merengue italiano, espolvorear canela",
            disponible=True,
            unidades_disponibles=10,
            num_ingredientes=5,
            kcal=380,
            calorias=Decimal('380.0'),
            proteinas=Decimal('8.0'),
            azucares=Decimal('45.0'),
            etiquetas=[EtiquetaItem.FRIO, EtiquetaItem.CON_GLUTEN]
        ),
        
        Plato(
            descripcion="Mazamorra Morada",
            precio=Decimal('8.50'),
            peso=Decimal('200.0'),
            tipo=EtiquetaPlato.POSTRE,
            valor_nutricional="Rica en antioxidantes y fibra",
            tiempo_preparacion=Decimal('45.0'),
            comentarios="Postre de maíz morado con frutas",
            receta="Cocinar maíz morado con canela, agregar frutas y azúcar",
            disponible=True,
            unidades_disponibles=15,
            num_ingredientes=6,
            kcal=250,
            calorias=Decimal('250.0'),
            proteinas=Decimal('3.0'),
            azucares=Decimal('35.0'),
            etiquetas=[EtiquetaItem.FRIO, EtiquetaItem.SIN_GLUTEN]
        ),
        
        Plato(
            descripcion="Picarones",
            precio=Decimal('10.00'),
            peso=Decimal('180.0'),
            tipo=EtiquetaPlato.POSTRE,
            valor_nutricional="Alto en carbohidratos y grasas",
            tiempo_preparacion=Decimal('25.0'),
            comentarios="Donas peruanas de camote con miel de chancaca",
            receta="Preparar masa con camote y harina, freír, bañar con miel de chancaca",
            disponible=True,
            unidades_disponibles=12,
            num_ingredientes=4,
            kcal=320,
            calorias=Decimal('320.0'),
            proteinas=Decimal('4.0'),
            azucares=Decimal('40.0'),
            etiquetas=[EtiquetaItem.CALIENTE, EtiquetaItem.CON_GLUTEN]
        ),
    ]
    
    return platos


def create_peruvian_bebidas():
    """Crea bebidas típicas peruanas."""
    print("🥤 Creando bebidas peruanas...")
    
    bebidas = [
        # Bebidas no alcohólicas
        Bebida(
            descripcion="Chicha Morada",
            precio=Decimal('6.50'),
            litros=Decimal('0.5'),
            alcoholico=False,
            valor_nutricional="Rica en antioxidantes y vitamina C",
            tiempo_preparacion=Decimal('15.0'),
            comentarios="Bebida tradicional de maíz morado",
            receta="Cocinar maíz morado con canela y clavo, endulzar y servir frío",
            disponible=True,
            unidades_disponibles=25,
            num_ingredientes=3,
            kcal=120,
            calorias=Decimal('120.0'),
            proteinas=Decimal('1.0'),
            azucares=Decimal('28.0'),
            etiquetas=[EtiquetaItem.FRIO, EtiquetaItem.SIN_GLUTEN]
        ),
        
        Bebida(
            descripcion="Jugo de Lúcuma",
            precio=Decimal('8.00'),
            litros=Decimal('0.4'),
            alcoholico=False,
            valor_nutricional="Rico en vitaminas A y C, fibra",
            tiempo_preparacion=Decimal('10.0'),
            comentarios="Jugo de la fruta nacional del Perú",
            receta="Licuar lúcuma con leche y azúcar, servir frío",
            disponible=True,
            unidades_disponibles=20,
            num_ingredientes=3,
            kcal=180,
            calorias=Decimal('180.0'),
            proteinas=Decimal('4.0'),
            azucares=Decimal('35.0'),
            etiquetas=[EtiquetaItem.FRIO, EtiquetaItem.SIN_GLUTEN]
        ),
        
        Bebida(
            descripcion="Jugo de Maracuyá",
            precio=Decimal('7.50'),
            litros=Decimal('0.4'),
            alcoholico=False,
            valor_nutricional="Alto en vitamina C y antioxidantes",
            tiempo_preparacion=Decimal('8.0'),
            comentarios="Jugo ácido y refrescante",
            receta="Extraer pulpa de maracuyá, mezclar con agua y azúcar",
            disponible=True,
            unidades_disponibles=18,
            num_ingredientes=3,
            kcal=90,
            calorias=Decimal('90.0'),
            proteinas=Decimal('1.5'),
            azucares=Decimal('20.0'),
            etiquetas=[EtiquetaItem.FRIO, EtiquetaItem.ACIDO, EtiquetaItem.SIN_GLUTEN]
        ),
        
        Bebida(
            descripcion="Inca Kola",
            precio=Decimal('4.50'),
            litros=Decimal('0.5'),
            alcoholico=False,
            valor_nutricional="Bebida gaseosa con sabor a hierba luisa",
            tiempo_preparacion=Decimal('0.0'),
            comentarios="La bebida nacional del Perú",
            receta="Servir fría",
            disponible=True,
            unidades_disponibles=30,
            num_ingredientes=1,
            kcal=150,
            calorias=Decimal('150.0'),
            proteinas=Decimal('0.0'),
            azucares=Decimal('35.0'),
            etiquetas=[EtiquetaItem.FRIO]
        ),
        
        Bebida(
            descripcion="Agua de Hierba Luisa",
            precio=Decimal('3.00'),
            litros=Decimal('0.5'),
            alcoholico=False,
            valor_nutricional="Infusión digestiva y relajante",
            tiempo_preparacion=Decimal('5.0'),
            comentarios="Infusión tradicional peruana",
            receta="Infusionar hojas de hierba luisa en agua caliente, endulzar",
            disponible=True,
            unidades_disponibles=20,
            num_ingredientes=2,
            kcal=5,
            calorias=Decimal('5.0'),
            proteinas=Decimal('0.0'),
            azucares=Decimal('1.0'),
            etiquetas=[EtiquetaItem.CALIENTE, EtiquetaItem.SIN_GLUTEN]
        ),
        
        # Bebidas alcohólicas
        Bebida(
            descripcion="Pisco Sour",
            precio=Decimal('18.00'),
            litros=Decimal('0.2'),
            alcoholico=True,
            valor_nutricional="Cóctel nacional del Perú",
            tiempo_preparacion=Decimal('8.0'),
            comentarios="Cóctel emblemático con pisco, limón y clara de huevo",
            receta="Mezclar pisco, jugo de limón, jarabe de goma y clara de huevo, batir con hielo",
            disponible=True,
            unidades_disponibles=15,
            num_ingredientes=5,
            kcal=200,
            calorias=Decimal('200.0'),
            proteinas=Decimal('2.0'),
            azucares=Decimal('8.0'),
            etiquetas=[EtiquetaItem.FRIO, EtiquetaItem.ACIDO]
        ),
        
        Bebida(
            descripcion="Chilcano de Pisco",
            precio=Decimal('15.00'),
            litros=Decimal('0.3'),
            alcoholico=True,
            valor_nutricional="Cóctel refrescante con pisco",
            tiempo_preparacion=Decimal('5.0'),
            comentarios="Cóctel simple con pisco, ginger ale y limón",
            receta="Mezclar pisco con ginger ale, agregar hielo y limón",
            disponible=True,
            unidades_disponibles=12,
            num_ingredientes=4,
            kcal=150,
            calorias=Decimal('150.0'),
            proteinas=Decimal('0.5'),
            azucares=Decimal('12.0'),
            etiquetas=[EtiquetaItem.FRIO]
        ),
        
        Bebida(
            descripcion="Chicha de Jora",
            precio=Decimal('12.00'),
            litros=Decimal('0.5'),
            alcoholico=True,
            valor_nutricional="Bebida ancestral de maíz fermentado",
            tiempo_preparacion=Decimal('0.0'),
            comentarios="Bebida tradicional andina fermentada",
            receta="Fermentar maíz jora con agua, endulzar y servir",
            disponible=True,
            unidades_disponibles=10,
            num_ingredientes=2,
            kcal=120,
            calorias=Decimal('120.0'),
            proteinas=Decimal('2.0'),
            azucares=Decimal('15.0'),
            etiquetas=[EtiquetaItem.FRIO, EtiquetaItem.SIN_GLUTEN]
        ),
        
        Bebida(
            descripcion="Cerveza Cusqueña",
            precio=Decimal('8.50'),
            litros=Decimal('0.33'),
            alcoholico=True,
            valor_nutricional="Cerveza peruana premium",
            tiempo_preparacion=Decimal('0.0'),
            comentarios="Cerveza artesanal de la ciudad imperial",
            receta="Servir fría",
            disponible=True,
            unidades_disponibles=20,
            num_ingredientes=1,
            kcal=140,
            calorias=Decimal('140.0'),
            proteinas=Decimal('1.5'),
            azucares=Decimal('3.0'),
            etiquetas=[EtiquetaItem.FRIO]
        ),
    ]
    
    return bebidas


def seed_database():
    """Pobla la base de datos con datos de prueba peruanos."""
    print("🇵🇪 Poblando base de datos con datos peruanos...")
    print("=" * 60)
    
    # Crear tablas
    create_tables()
    print("✅ Tablas creadas")
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Crear servicios
        item_repository = ItemRepositoryImpl(db)
        plato_repository = PlatoRepositoryImpl(db)
        bebida_repository = BebidaRepositoryImpl(db)
        ingrediente_repository = IngredienteRepositoryImpl(db)
        
        item_service = ItemService(item_repository, plato_repository, bebida_repository)
        ingrediente_service = IngredienteService(ingrediente_repository)
        
        # Crear ingredientes
        ingredientes = create_peruvian_ingredients()
        for ingrediente in ingredientes:
            ingrediente_service.create_ingrediente(ingrediente)
        print(f"✅ {len(ingredientes)} ingredientes creados")
        
        # Crear platos
        platos = create_peruvian_platos()
        for plato in platos:
            item_service.create_item(plato)
        print(f"✅ {len(platos)} platos creados")
        
        # Crear bebidas
        bebidas = create_peruvian_bebidas()
        for bebida in bebidas:
            item_service.create_item(bebida)
        print(f"✅ {len(bebidas)} bebidas creadas")
        
        print("\n" + "=" * 60)
        print("🎉 ¡Base de datos poblada exitosamente con datos peruanos!")
        print(f"📊 Resumen: {len(ingredientes)} ingredientes, {len(platos)} platos, {len(bebidas)} bebidas")
        print("\n🌐 Puedes consumir los datos desde el frontend en:")
        print("   - GET /items/ - Todos los ítems")
        print("   - GET /ingredientes/ - Todos los ingredientes")
        print("   - GET /items/platos/entradas - Entradas peruanas")
        print("   - GET /items/platos/principales - Platos principales")
        print("   - GET /items/platos/postres - Postres peruanos")
        print("   - GET /items/bebidas/alcoholicas - Bebidas alcohólicas")
        print("   - GET /items/bebidas/no-alcoholicas - Bebidas no alcohólicas")
        print("   - GET /docs - Documentación de la API")
        
    except Exception as e:
        print(f"❌ Error al poblar la base de datos: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
