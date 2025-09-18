"""
Modelos de base de datos para ítems del menú.
"""

from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from decimal import Decimal

Base = declarative_base()

# Tabla de asociación para la relación many-to-many entre ítems e ingredientes
item_ingrediente_association = Table(
    'item_ingrediente',
    Base.metadata,
    Column('item_id', Integer, ForeignKey('items.id'), primary_key=True),
    Column('ingrediente_id', Integer, ForeignKey('ingredientes.id'), primary_key=True),
    Column('cantidad', Numeric(10, 3), nullable=False, default=1.0)
)

# Tabla de asociación para las etiquetas de ítems
item_etiqueta_association = Table(
    'item_etiqueta',
    Base.metadata,
    Column('item_id', Integer, ForeignKey('items.id'), primary_key=True),
    Column('etiqueta', String(50), primary_key=True)
)


class ItemModel(Base):
    """
    Modelo de base de datos para ítems del menú.
    """
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, index=True)
    valor_nutricional = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    tiempo_preparacion = Column(Numeric(8, 2), nullable=False, default=0)
    comentarios = Column(Text, nullable=True)
    receta = Column(Text, nullable=True)
    disponible = Column(Boolean, nullable=False, default=True)
    unidades_disponibles = Column(Integer, nullable=False, default=0)
    num_ingredientes = Column(Integer, nullable=False, default=0)
    kcal = Column(Integer, nullable=False, default=0)
    calorias = Column(Numeric(8, 2), nullable=False, default=0)
    proteinas = Column(Numeric(8, 2), nullable=False, default=0)
    azucares = Column(Numeric(8, 2), nullable=False, default=0)
    descripcion = Column(String(500), nullable=False)
    tipo = Column(String(20), nullable=False)  # 'PLATO' o 'BEBIDA'
    
    # Relación con ingredientes
    ingredientes = relationship(
        "IngredienteModel",
        secondary=item_ingrediente_association,
        back_populates="items"
    )
    
    # Relación con etiquetas
    etiquetas = relationship(
        "ItemEtiquetaModel",
        back_populates="item"
    )
    
    def to_domain(self):
        """
        Convierte el modelo a entidad de dominio.
        """
        from domain.entities import Item, Plato, Bebida
        from domain.entities.enums import EtiquetaItem, EtiquetaPlato
        
        # Convertir etiquetas
        etiquetas = [EtiquetaItem(etiqueta.etiqueta) for etiqueta in self.etiquetas]
        
        if self.tipo == 'PLATO':
            return Plato(
                id=self.id,
                valor_nutricional=self.valor_nutricional or "",
                precio=self.precio,
                tiempo_preparacion=self.tiempo_preparacion,
                comentarios=self.comentarios or "",
                receta=self.receta or "",
                disponible=self.disponible,
                unidades_disponibles=self.unidades_disponibles,
                num_ingredientes=self.num_ingredientes,
                kcal=self.kcal,
                calorias=self.calorias,
                proteinas=self.proteinas,
                azucares=self.azucares,
                descripcion=self.descripcion,
                etiquetas=etiquetas,
                peso=getattr(self, 'peso', Decimal('0.0')),
                tipo=EtiquetaPlato(getattr(self, 'tipo_plato', 'FONDO'))
            )
        elif self.tipo == 'BEBIDA':
            return Bebida(
                id=self.id,
                valor_nutricional=self.valor_nutricional or "",
                precio=self.precio,
                tiempo_preparacion=self.tiempo_preparacion,
                comentarios=self.comentarios or "",
                receta=self.receta or "",
                disponible=self.disponible,
                unidades_disponibles=self.unidades_disponibles,
                num_ingredientes=self.num_ingredientes,
                kcal=self.kcal,
                calorias=self.calorias,
                proteinas=self.proteinas,
                azucares=self.azucares,
                descripcion=self.descripcion,
                etiquetas=etiquetas,
                litros=getattr(self, 'litros', Decimal('0.0')),
                alcoholico=getattr(self, 'alcoholico', False)
            )
        else:
            # Fallback para ítems genéricos
            return Item(
                id=self.id,
                valor_nutricional=self.valor_nutricional or "",
                precio=self.precio,
                tiempo_preparacion=self.tiempo_preparacion,
                comentarios=self.comentarios or "",
                receta=self.receta or "",
                disponible=self.disponible,
                unidades_disponibles=self.unidades_disponibles,
                num_ingredientes=self.num_ingredientes,
                kcal=self.kcal,
                calorias=self.calorias,
                proteinas=self.proteinas,
                azucares=self.azucares,
                descripcion=self.descripcion,
                etiquetas=etiquetas
            )


class PlatoModel(ItemModel):
    """
    Modelo de base de datos para platos.
    """
    __tablename__ = 'platos'
    
    id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    peso = Column(Numeric(8, 2), nullable=False)
    tipo_plato = Column(String(20), nullable=False)  # 'ENTRADA', 'FONDO', 'POSTRE'


class BebidaModel(ItemModel):
    """
    Modelo de base de datos para bebidas.
    """
    __tablename__ = 'bebidas'
    
    id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    litros = Column(Numeric(8, 3), nullable=False)
    alcoholico = Column(Boolean, nullable=False, default=False)


class IngredienteModel(Base):
    """
    Modelo de base de datos para ingredientes.
    """
    __tablename__ = 'ingredientes'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, unique=True)
    stock = Column(Numeric(10, 3), nullable=False, default=0)
    peso = Column(Numeric(8, 3), nullable=False, default=1.0)
    tipo = Column(String(20), nullable=False)  # 'VERDURA', 'CARNE', 'FRUTA'
    
    # Relación con ítems
    items = relationship(
        "ItemModel",
        secondary=item_ingrediente_association,
        back_populates="ingredientes"
    )
    
    def to_domain(self):
        """
        Convierte el modelo a entidad de dominio.
        """
        from domain.entities import Ingrediente
        from domain.entities.enums import EtiquetaIngrediente
        
        return Ingrediente(
            id=self.id,
            nombre=self.nombre,
            stock=self.stock,
            peso=self.peso,
            tipo=EtiquetaIngrediente(self.tipo)
        )


class ItemEtiquetaModel(Base):
    """
    Modelo de base de datos para etiquetas de ítems.
    """
    __tablename__ = 'item_etiquetas'
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    etiqueta = Column(String(50), nullable=False)
    
    # Relación con ítem
    item = relationship("ItemModel", back_populates="etiquetas")
