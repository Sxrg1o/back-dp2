from typing import List, Dict, Optional, Tuple
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from app.models.menu_y_carta.domain import Item, Plato, Bebida, Ingrediente
from app.models.menu_y_carta.enums import EtiquetaPlato, TipoAlergeno
from app.repositories.menu_repository_interface import IMenuRepository
from app.config import Config

# Modelos de base de datos
Base = declarative_base()

class ItemDB(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    imagen = Column(String(255))
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    disponible = Column(Boolean, default=True)
    categoria = Column(String(50))
    alergenos = Column(Text)
    tiempo_preparacion = Column(Float, default=0)
    descripcion = Column(Text)
    tipo_item = Column(String(20))  # "PLATO" o "BEBIDA"
    
    # Campos específicos de plato
    peso = Column(Float)
    tipo_plato = Column(String(20))  # "ENTRADA", "FONDO", "POSTRE"
    
    # Campos específicos de bebida
    litros = Column(Float)
    con_alcohol = Column(Boolean, default=False)

class IngredienteDB(Base):
    __tablename__ = "ingredientes"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    categoria_alergeno = Column(String(50))

class ItemIngredienteDB(Base):
    __tablename__ = "item_ingredientes"
    
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    ingrediente_id = Column(Integer, ForeignKey('ingredientes.id'), primary_key=True)

class DatabaseMenuRepository(IMenuRepository):
    """Implementación del repositorio de menú usando base de datos"""
    
    def __init__(self, database_url: str = None):
        """
        Inicializa el repositorio con conexión a base de datos
        
        Args:
            database_url: URL de conexión a la base de datos
        """
        self.database_url = database_url or Config.DATABASE_URL
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Crear tablas si no existen
        Base.metadata.create_all(bind=self.engine)
        
        # Inicializar datos si la BD está vacía
        self._inicializar_datos_si_vacio()
    
    def _get_session(self):
        """Obtiene una sesión de base de datos"""
        return self.SessionLocal()
    
    def _inicializar_datos_si_vacio(self):
        """Inicializa datos de ejemplo si la base de datos está vacía"""
        with self._get_session() as session:
            # Verificar si hay datos
            if session.query(ItemDB).count() > 0:
                return  # Ya hay datos, no inicializar
            
            # Crear ingredientes
            ingredientes_data = [
                {"id": 1, "nombre": "Pescado", "categoria_alergeno": "PESCADO"},
                {"id": 2, "nombre": "Limón", "categoria_alergeno": None},
                {"id": 3, "nombre": "Cebolla", "categoria_alergeno": None},
                {"id": 4, "nombre": "Arroz", "categoria_alergeno": None},
                {"id": 5, "nombre": "Mariscos", "categoria_alergeno": "MARISCOS"},
            ]
            
            for ing_data in ingredientes_data:
                ingrediente = IngredienteDB(**ing_data)
                session.add(ingrediente)
            
            # Crear items de ejemplo
            items_data = [
                {
                    "id": 1, "nombre": "Ceviche", "precio": 28.0, "stock": 10,
                    "disponible": True, "categoria": "Plato principal",
                    "alergenos": "Pescado", "tiempo_preparacion": 10.0,
                    "descripcion": "Clásico ceviche peruano",
                    "tipo_item": "PLATO", "peso": 350.0, "tipo_plato": "FONDO"
                },
                {
                    "id": 2, "nombre": "Arroz con mariscos", "precio": 32.0, "stock": 4,
                    "disponible": True, "categoria": "Plato principal",
                    "alergenos": "Mariscos", "tiempo_preparacion": 20.0,
                    "descripcion": "Arroz con mariscos mixtos",
                    "tipo_item": "PLATO", "peso": 450.0, "tipo_plato": "FONDO"
                },
                {
                    "id": 6, "nombre": "Cerveza artesanal", "precio": 8.0, "stock": 20,
                    "disponible": True, "categoria": "Bebida alcohólica",
                    "alergenos": "Gluten", "tiempo_preparacion": 2.0,
                    "descripcion": "Cerveza artesanal peruana",
                    "tipo_item": "BEBIDA", "litros": 0.5, "con_alcohol": True
                }
            ]
            
            for item_data in items_data:
                item = ItemDB(**item_data)
                session.add(item)
            
            session.commit()
    
    def _convertir_item_db_a_dominio(self, item_db: ItemDB) -> Item:
        """Convierte un ItemDB a un objeto de dominio Item"""
        # Obtener ingredientes
        with self._get_session() as session:
            ingredientes_db = session.query(IngredienteDB).join(
                ItemIngredienteDB, IngredienteDB.id == ItemIngredienteDB.ingrediente_id
            ).filter(ItemIngredienteDB.item_id == item_db.id).all()
            
            ingredientes = [
                Ingrediente(
                    id=ing.id,
                    nombre=ing.nombre,
                    categoria_alergeno=TipoAlergeno(ing.categoria_alergeno) if ing.categoria_alergeno else None
                )
                for ing in ingredientes_db
            ]
        
        if item_db.tipo_item == "PLATO":
            return Plato(
                id=item_db.id,
                nombre=item_db.nombre,
                imagen=item_db.imagen or "",
                precio=item_db.precio,
                stock=item_db.stock,
                disponible=item_db.disponible,
                categoria=item_db.categoria or "",
                alergenos=item_db.alergenos or "",
                tiempo_preparacion=item_db.tiempo_preparacion,
                descripcion=item_db.descripcion or "",
                ingredientes=ingredientes,
                grupo_personalizacion=None,  # TODO: Implementar grupos de personalización
                peso=item_db.peso or 0.0,
                tipo=EtiquetaPlato(item_db.tipo_plato) if item_db.tipo_plato else EtiquetaPlato.FONDO
            )
        else:  # BEBIDA
            return Bebida(
                id=item_db.id,
                nombre=item_db.nombre,
                imagen=item_db.imagen or "",
                precio=item_db.precio,
                stock=item_db.stock,
                disponible=item_db.disponible,
                categoria=item_db.categoria or "",
                alergenos=item_db.alergenos or "",
                tiempo_preparacion=item_db.tiempo_preparacion,
                descripcion=item_db.descripcion or "",
                ingredientes=ingredientes,
                grupo_personalizacion=None,  # TODO: Implementar grupos de personalización
                litros=item_db.litros or 0.0,
                con_alcohol=item_db.con_alcohol or False
            )
    
    def obtener_todos_los_items(self) -> Dict[int, Item]:
        """Obtiene todos los items del menú"""
        with self._get_session() as session:
            items_db = session.query(ItemDB).all()
            return {
                item_db.id: self._convertir_item_db_a_dominio(item_db)
                for item_db in items_db
            }
    
    def obtener_item_por_id(self, item_id: int) -> Optional[Item]:
        """Obtiene un item específico por ID"""
        with self._get_session() as session:
            item_db = session.query(ItemDB).filter(ItemDB.id == item_id).first()
            if not item_db:
                return None
            return self._convertir_item_db_a_dominio(item_db)
    
    def obtener_platos(self) -> List[Plato]:
        """Obtiene todos los platos"""
        with self._get_session() as session:
            items_db = session.query(ItemDB).filter(ItemDB.tipo_item == "PLATO").all()
            return [
                self._convertir_item_db_a_dominio(item_db)
                for item_db in items_db
            ]
    
    def obtener_platos_por_tipo(self, tipo: EtiquetaPlato) -> List[Plato]:
        """Obtiene platos filtrados por tipo"""
        with self._get_session() as session:
            items_db = session.query(ItemDB).filter(
                ItemDB.tipo_item == "PLATO",
                ItemDB.tipo_plato == tipo.value
            ).all()
            return [
                self._convertir_item_db_a_dominio(item_db)
                for item_db in items_db
            ]
    
    def obtener_bebidas(self) -> List[Bebida]:
        """Obtiene todas las bebidas"""
        with self._get_session() as session:
            items_db = session.query(ItemDB).filter(ItemDB.tipo_item == "BEBIDA").all()
            return [
                self._convertir_item_db_a_dominio(item_db)
                for item_db in items_db
            ]
    
    def obtener_bebidas_sin_alcohol(self) -> List[Bebida]:
        """Obtiene bebidas sin alcohol"""
        with self._get_session() as session:
            items_db = session.query(ItemDB).filter(
                ItemDB.tipo_item == "BEBIDA",
                ItemDB.con_alcohol == False
            ).all()
            return [
                self._convertir_item_db_a_dominio(item_db)
                for item_db in items_db
            ]
    
    def obtener_bebidas_con_alcohol(self) -> List[Bebida]:
        """Obtiene bebidas con alcohol"""
        with self._get_session() as session:
            items_db = session.query(ItemDB).filter(
                ItemDB.tipo_item == "BEBIDA",
                ItemDB.con_alcohol == True
            ).all()
            return [
                self._convertir_item_db_a_dominio(item_db)
                for item_db in items_db
            ]
    
    def buscar_items_por_nombre(self, nombre: str) -> List[Item]:
        """Busca items por nombre (búsqueda parcial)"""
        with self._get_session() as session:
            items_db = session.query(ItemDB).filter(
                ItemDB.nombre.ilike(f"%{nombre}%")
            ).all()
            return [
                self._convertir_item_db_a_dominio(item_db)
                for item_db in items_db
            ]
    
    def filtrar_por_categoria(self, categoria: str) -> List[Item]:
        """Filtra items por categoría"""
        with self._get_session() as session:
            items_db = session.query(ItemDB).filter(
                ItemDB.categoria.ilike(f"%{categoria}%")
            ).all()
            return [
                self._convertir_item_db_a_dominio(item_db)
                for item_db in items_db
            ]
    
    def filtrar_por_alergenos(self, alergenos: List[TipoAlergeno]) -> List[Item]:
        """Filtra items que contengan los alérgenos especificados"""
        with self._get_session() as session:
            alergenos_str = [alergeno.value for alergeno in alergenos]
            items_db = session.query(ItemDB).filter(
                ItemDB.alergenos.in_(alergenos_str)
            ).all()
            return [
                self._convertir_item_db_a_dominio(item_db)
                for item_db in items_db
            ]
    
    def filtrar_sin_alergenos(self, alergenos: List[TipoAlergeno]) -> List[Item]:
        """Filtra items que NO contengan los alérgenos especificados"""
        with self._get_session() as session:
            alergenos_str = [alergeno.value for alergeno in alergenos]
            items_db = session.query(ItemDB).filter(
                ~ItemDB.alergenos.in_(alergenos_str)
            ).all()
            return [
                self._convertir_item_db_a_dominio(item_db)
                for item_db in items_db
            ]
    
    def obtener_items_disponibles(self) -> List[Item]:
        """Obtiene solo items que están disponibles y tienen stock"""
        with self._get_session() as session:
            items_db = session.query(ItemDB).filter(
                ItemDB.disponible == True,
                ItemDB.stock > 0
            ).all()
            return [
                self._convertir_item_db_a_dominio(item_db)
                for item_db in items_db
            ]
    
    def obtener_ingredientes(self) -> List[Ingrediente]:
        """Obtiene todos los ingredientes"""
        with self._get_session() as session:
            ingredientes_db = session.query(IngredienteDB).all()
            return [
                Ingrediente(
                    id=ing.id,
                    nombre=ing.nombre,
                    categoria_alergeno=TipoAlergeno(ing.categoria_alergeno) if ing.categoria_alergeno else None
                )
                for ing in ingredientes_db
            ]
    
    def obtener_ingrediente_por_id(self, ingrediente_id: int) -> Optional[Ingrediente]:
        """Obtiene un ingrediente por ID"""
        with self._get_session() as session:
            ingrediente_db = session.query(IngredienteDB).filter(IngredienteDB.id == ingrediente_id).first()
            if not ingrediente_db:
                return None
            return Ingrediente(
                id=ingrediente_db.id,
                nombre=ingrediente_db.nombre,
                categoria_alergeno=TipoAlergeno(ingrediente_db.categoria_alergeno) if ingrediente_db.categoria_alergeno else None
            )
    
    def buscar_ingredientes_por_nombre(self, nombre: str) -> List[Ingrediente]:
        """Busca ingredientes por nombre"""
        with self._get_session() as session:
            ingredientes_db = session.query(IngredienteDB).filter(
                IngredienteDB.nombre.ilike(f"%{nombre}%")
            ).all()
            return [
                Ingrediente(
                    id=ing.id,
                    nombre=ing.nombre,
                    categoria_alergeno=TipoAlergeno(ing.categoria_alergeno) if ing.categoria_alergeno else None
                )
                for ing in ingredientes_db
            ]
    
    def obtener_items_por_ingrediente(self, ingrediente_id: int) -> List[Item]:
        """Obtiene items que contengan un ingrediente específico"""
        with self._get_session() as session:
            items_db = session.query(ItemDB).join(
                ItemIngredienteDB, ItemDB.id == ItemIngredienteDB.item_id
            ).filter(ItemIngredienteDB.ingrediente_id == ingrediente_id).all()
            return [
                self._convertir_item_db_a_dominio(item_db)
                for item_db in items_db
            ]
    
    def verificar_disponibilidad_item(self, item_id: int, cantidad: int = 1) -> Tuple[bool, str]:
        """Verifica si un item está disponible en la cantidad solicitada"""
        item = self.obtener_item_por_id(item_id)
        if not item:
            return False, "Item no encontrado"
        
        if not item.disponible:
            return False, "Item no disponible"
        
        if item.stock < cantidad:
            return False, f"Stock insuficiente (disponible: {item.stock})"
        
        return True, "Disponible"

