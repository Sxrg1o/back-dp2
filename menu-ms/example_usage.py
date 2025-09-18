"""
Ejemplo de uso del microservicio de Menú y Carta.
Este script demuestra cómo utilizar las funcionalidades principales.
"""

from decimal import Decimal
from domain.entities import Plato, Bebida, Ingrediente
from domain.entities.enums import EtiquetaItem, EtiquetaIngrediente, EtiquetaPlato


def ejemplo_crear_platos():
    """Ejemplo de creación de platos."""
    print("🍽️ Creando platos de ejemplo...")
    
    # Entrada
    ensalada_cesar = Plato(
        descripcion="Ensalada César con lechuga romana, crutones y aderezo especial",
        precio=Decimal('8.50'),
        peso=Decimal('200.0'),
        tipo=EtiquetaPlato.ENTRADA,
        valor_nutricional="Rica en vitaminas A y C, fibra y proteínas",
        tiempo_preparacion=Decimal('10.0'),
        comentarios="Plato fresco y saludable",
        receta="Cortar lechuga, agregar crutones, aderezar y servir",
        disponible=True,
        unidades_disponibles=15,
        num_ingredientes=4,
        kcal=250,
        calorias=Decimal('250.0'),
        proteinas=Decimal('12.0'),
        azucares=Decimal('3.0'),
        etiquetas=[EtiquetaItem.FRIO, EtiquetaItem.SIN_GLUTEN]
    )
    
    # Plato principal
    pasta_carbonara = Plato(
        descripcion="Pasta Carbonara tradicional con panceta, huevos y queso parmesano",
        precio=Decimal('15.50'),
        peso=Decimal('300.0'),
        tipo=EtiquetaPlato.FONDO,
        valor_nutricional="Alto en carbohidratos y proteínas",
        tiempo_preparacion=Decimal('20.0'),
        comentarios="Plato tradicional italiano",
        receta="Cocer pasta, preparar salsa con huevos y panceta, mezclar y servir",
        disponible=True,
        unidades_disponibles=10,
        num_ingredientes=5,
        kcal=600,
        calorias=Decimal('600.0'),
        proteinas=Decimal('25.0'),
        azucares=Decimal('5.0'),
        etiquetas=[EtiquetaItem.CON_GLUTEN, EtiquetaItem.CALIENTE]
    )
    
    # Postre
    tiramisu = Plato(
        descripcion="Tiramisú clásico con café, mascarpone y cacao",
        precio=Decimal('6.00'),
        peso=Decimal('150.0'),
        tipo=EtiquetaPlato.POSTRE,
        valor_nutricional="Rico en grasas y azúcares",
        tiempo_preparacion=Decimal('30.0'),
        comentarios="Postre italiano tradicional",
        receta="Preparar crema de mascarpone, empapar bizcochos en café, montar en capas",
        disponible=True,
        unidades_disponibles=8,
        num_ingredientes=6,
        kcal=400,
        calorias=Decimal('400.0'),
        proteinas=Decimal('8.0'),
        azucares=Decimal('35.0'),
        etiquetas=[EtiquetaItem.FRIO, EtiquetaItem.CON_GLUTEN]
    )
    
    print(f"✅ {ensalada_cesar.descripcion} - ${ensalada_cesar.precio}")
    print(f"✅ {pasta_carbonara.descripcion} - ${pasta_carbonara.precio}")
    print(f"✅ {tiramisu.descripcion} - ${tiramisu.precio}")
    
    return [ensalada_cesar, pasta_carbonara, tiramisu]


def ejemplo_crear_bebidas():
    """Ejemplo de creación de bebidas."""
    print("\n🥤 Creando bebidas de ejemplo...")
    
    # Bebida no alcohólica
    coca_cola = Bebida(
        descripcion="Coca Cola clásica 500ml",
        precio=Decimal('3.50'),
        litros=Decimal('0.5'),
        alcoholico=False,
        valor_nutricional="Alto en azúcares y cafeína",
        tiempo_preparacion=Decimal('0.0'),
        comentarios="Bebida refrescante",
        receta="Servir fría",
        disponible=True,
        unidades_disponibles=50,
        num_ingredientes=1,
        kcal=200,
        calorias=Decimal('200.0'),
        proteinas=Decimal('0.0'),
        azucares=Decimal('50.0'),
        etiquetas=[EtiquetaItem.FRIO]
    )
    
    # Bebida alcohólica
    cerveza_corona = Bebida(
        descripcion="Cerveza Corona Extra 330ml",
        precio=Decimal('4.50'),
        litros=Decimal('0.33'),
        alcoholico=True,
        valor_nutricional="Contiene alcohol, moderado en calorías",
        tiempo_preparacion=Decimal('0.0'),
        comentarios="Cerveza mexicana refrescante",
        receta="Servir muy fría con limón",
        disponible=True,
        unidades_disponibles=30,
        num_ingredientes=1,
        kcal=150,
        calorias=Decimal('150.0'),
        proteinas=Decimal('1.5'),
        azucares=Decimal('2.0'),
        etiquetas=[EtiquetaItem.FRIO]
    )
    
    # Bebida no alcohólica
    agua_mineral = Bebida(
        descripcion="Agua mineral natural 500ml",
        precio=Decimal('2.00'),
        litros=Decimal('0.5'),
        alcoholico=False,
        valor_nutricional="Sin calorías, hidratante",
        tiempo_preparacion=Decimal('0.0'),
        comentarios="Agua pura y natural",
        receta="Servir fría",
        disponible=True,
        unidades_disponibles=100,
        num_ingredientes=1,
        kcal=0,
        calorias=Decimal('0.0'),
        proteinas=Decimal('0.0'),
        azucares=Decimal('0.0'),
        etiquetas=[EtiquetaItem.FRIO]
    )
    
    print(f"✅ {coca_cola.descripcion} - ${coca_cola.precio}")
    print(f"✅ {cerveza_corona.descripcion} - ${cerveza_corona.precio}")
    print(f"✅ {agua_mineral.descripcion} - ${agua_mineral.precio}")
    
    return [coca_cola, cerveza_corona, agua_mineral]


def ejemplo_crear_ingredientes():
    """Ejemplo de creación de ingredientes."""
    print("\n🥬 Creando ingredientes de ejemplo...")
    
    # Verduras
    tomate = Ingrediente(
        nombre="Tomate",
        stock=Decimal('20.0'),
        peso=Decimal('0.2'),
        tipo=EtiquetaIngrediente.VERDURA
    )
    
    lechuga = Ingrediente(
        nombre="Lechuga Romana",
        stock=Decimal('15.0'),
        peso=Decimal('0.3'),
        tipo=EtiquetaIngrediente.VERDURA
    )
    
    # Carnes
    panceta = Ingrediente(
        nombre="Panceta",
        stock=Decimal('5.0'),
        peso=Decimal('0.1'),
        tipo=EtiquetaIngrediente.CARNE
    )
    
    pollo = Ingrediente(
        nombre="Pechuga de Pollo",
        stock=Decimal('8.0'),
        peso=Decimal('0.5'),
        tipo=EtiquetaIngrediente.CARNE
    )
    
    # Frutas
    limon = Ingrediente(
        nombre="Limón",
        stock=Decimal('25.0'),
        peso=Decimal('0.1'),
        tipo=EtiquetaIngrediente.FRUTA
    )
    
    print(f"✅ {tomate.nombre} - Stock: {tomate.stock}kg")
    print(f"✅ {lechuga.nombre} - Stock: {lechuga.stock}kg")
    print(f"✅ {panceta.nombre} - Stock: {panceta.stock}kg")
    print(f"✅ {pollo.nombre} - Stock: {pollo.stock}kg")
    print(f"✅ {limon.nombre} - Stock: {limon.stock}kg")
    
    return [tomate, lechuga, panceta, pollo, limon]


def ejemplo_funcionalidades_avanzadas():
    """Ejemplo de funcionalidades avanzadas."""
    print("\n🔧 Demostrando funcionalidades avanzadas...")
    
    # Crear un plato
    plato = Plato(
        descripcion="Pasta con Pollo",
        precio=Decimal('12.00'),
        peso=Decimal('250.0'),
        tipo=EtiquetaPlato.FONDO,
        unidades_disponibles=5,
        calorias=Decimal('450.0')
    )
    
    # Agregar etiquetas
    plato.agregar_etiqueta(EtiquetaItem.CON_GLUTEN)
    plato.agregar_etiqueta(EtiquetaItem.CALIENTE)
    
    print(f"📋 Plato: {plato.descripcion}")
    print(f"💰 Precio: ${plato.precio}")
    print(f"⚖️ Peso: {plato.peso}g")
    print(f"🏷️ Etiquetas: {[e.value for e in plato.etiquetas]}")
    print(f"📊 Densidad calórica: {plato.calcular_densidad_calorica():.2f} cal/g")
    print(f"🍽️ Es plato principal: {plato.es_plato_principal()}")
    
    # Verificar stock
    print(f"📦 Stock disponible: {plato.verificar_stock()}")
    print(f"📦 Unidades disponibles: {plato.unidades_disponibles}")
    
    # Reducir stock
    if plato.reducir_stock(2):
        print(f"✅ Stock reducido exitosamente. Quedan: {plato.unidades_disponibles}")
    else:
        print("❌ No se pudo reducir el stock")
    
    # Crear una bebida
    bebida = Bebida(
        descripcion="Jugo de Naranja",
        precio=Decimal('4.00'),
        litros=Decimal('0.3'),
        alcoholico=False,
        calorias=Decimal('120.0')
    )
    
    print(f"\n🥤 Bebida: {bebida.descripcion}")
    print(f"💰 Precio: ${bebida.precio}")
    print(f"📏 Volumen: {bebida.litros}L")
    print(f"🍺 Es alcohólica: {bebida.es_alcoholica()}")
    print(f"👶 Apta para menores: {bebida.es_apta_para_menores()}")
    print(f"📊 Calorías por ml: {bebida.calcular_calorias_por_ml():.2f} cal/ml")
    
    # Crear un ingrediente
    ingrediente = Ingrediente(
        nombre="Cebolla",
        stock=Decimal('10.0'),
        peso=Decimal('0.15'),
        tipo=EtiquetaIngrediente.VERDURA
    )
    
    print(f"\n🥬 Ingrediente: {ingrediente.nombre}")
    print(f"📦 Stock: {ingrediente.stock}kg")
    print(f"⚖️ Peso unitario: {ingrediente.peso}kg")
    print(f"📊 Peso total: {ingrediente.calcular_peso_total()}kg")
    print(f"🏷️ Tipo: {ingrediente.tipo.value}")
    
    # Verificar stock del ingrediente
    cantidad_necesaria = Decimal('2.0')
    if ingrediente.verificar_stock(cantidad_necesaria):
        print(f"✅ Hay suficiente stock de {ingrediente.nombre}")
        if ingrediente.reducir_stock(cantidad_necesaria):
            print(f"✅ Stock reducido. Quedan: {ingrediente.stock}kg")
    else:
        print(f"❌ No hay suficiente stock de {ingrediente.nombre}")


def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("🚀 Ejemplo de uso del Microservicio de Menú y Carta")
    print("=" * 60)
    
    # Crear platos
    platos = ejemplo_crear_platos()
    
    # Crear bebidas
    bebidas = ejemplo_crear_bebidas()
    
    # Crear ingredientes
    ingredientes = ejemplo_crear_ingredientes()
    
    # Demostrar funcionalidades avanzadas
    ejemplo_funcionalidades_avanzadas()
    
    print("\n" + "=" * 60)
    print("✅ Ejemplo completado exitosamente!")
    print(f"📊 Resumen: {len(platos)} platos, {len(bebidas)} bebidas, {len(ingredientes)} ingredientes")
    print("\n💡 Para usar la API REST, ejecuta: python main.py")
    print("📚 Documentación disponible en: http://localhost:8002/docs")


if __name__ == "__main__":
    main()
