"""
Implementación concreta del repositorio de ítems.
"""

from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from domain.entities import Item, Plato, Bebida
from domain.entities.enums import EtiquetaItem, EtiquetaPlato
from domain.repositories import ItemRepository, PlatoRepository, BebidaRepository
from infrastructure.models.item_model import ItemModel, PlatoModel, BebidaModel, ItemEtiquetaModel


class ItemRepositoryImpl(ItemRepository):
    """
    Implementación concreta del repositorio de ítems.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            db: Sesión de base de datos
        """
        self.db = db
    
    def create(self, item: Item) -> Item:
        """
        Crea un nuevo ítem en el repositorio.
        """
        # Crear el modelo base
        item_model = ItemModel(
            valor_nutricional=item.valor_nutricional,
            precio=item.precio,
            tiempo_preparacion=item.tiempo_preparacion,
            comentarios=item.comentarios,
            receta=item.receta,
            disponible=item.disponible,
            unidades_disponibles=item.unidades_disponibles,
            num_ingredientes=item.num_ingredientes,
            kcal=item.kcal,
            calorias=item.calorias,
            proteinas=item.proteinas,
            azucares=item.azucares,
            descripcion=item.descripcion,
            tipo=item.get_tipo()
        )
        
        self.db.add(item_model)
        self.db.flush()  # Para obtener el ID
        
        # Crear modelo específico según el tipo
        if isinstance(item, Plato):
            plato_model = PlatoModel(
                id=item_model.id,
                peso=item.peso,
                tipo_plato=item.tipo.value
            )
            self.db.add(plato_model)
        elif isinstance(item, Bebida):
            bebida_model = BebidaModel(
                id=item_model.id,
                litros=item.litros,
                alcoholico=item.alcoholico
            )
            self.db.add(bebida_model)
        
        # Agregar etiquetas
        for etiqueta in item.etiquetas:
            etiqueta_model = ItemEtiquetaModel(
                item_id=item_model.id,
                etiqueta=etiqueta.value
            )
            self.db.add(etiqueta_model)
        
        self.db.commit()
        self.db.refresh(item_model)
        
        # Retornar la entidad de dominio
        return item_model.to_domain()
    
    def get_by_id(self, item_id: int) -> Optional[Item]:
        """
        Obtiene un ítem por su ID.
        """
        item_model = self.db.query(ItemModel).filter(ItemModel.id == item_id).first()
        if item_model:
            return item_model.to_domain()
        return None
    
    def get_all(self) -> List[Item]:
        """
        Obtiene todos los ítems del repositorio.
        """
        items = self.db.query(ItemModel).all()
        return [item.to_domain() for item in items]
    
    def get_available(self) -> List[Item]:
        """
        Obtiene todos los ítems disponibles en el menú.
        """
        items = self.db.query(ItemModel).filter(ItemModel.disponible == True).all()
        return [item.to_domain() for item in items]
    
    def get_by_price_range(self, min_price: Decimal, max_price: Decimal) -> List[Item]:
        """
        Obtiene ítems dentro de un rango de precios.
        """
        items = self.db.query(ItemModel).filter(
            ItemModel.precio >= min_price,
            ItemModel.precio <= max_price
        ).all()
        return [item.to_domain() for item in items]
    
    def get_by_etiqueta(self, etiqueta: EtiquetaItem) -> List[Item]:
        """
        Obtiene ítems que tienen una etiqueta específica.
        """
        items = self.db.query(ItemModel).join(ItemEtiquetaModel).filter(
            ItemEtiquetaModel.etiqueta == etiqueta.value
        ).all()
        return [item.to_domain() for item in items]
    
    def search_by_name(self, name: str) -> List[Item]:
        """
        Busca ítems por nombre o descripción.
        """
        items = self.db.query(ItemModel).filter(
            ItemModel.descripcion.ilike(f"%{name}%")
        ).all()
        return [item.to_domain() for item in items]
    
    def update(self, item: Item) -> Item:
        """
        Actualiza un ítem existente.
        """
        item_model = self.db.query(ItemModel).filter(ItemModel.id == item.id).first()
        if not item_model:
            raise ValueError(f"No se encontró un ítem con ID {item.id}")
        
        # Actualizar campos base
        item_model.valor_nutricional = item.valor_nutricional
        item_model.precio = item.precio
        item_model.tiempo_preparacion = item.tiempo_preparacion
        item_model.comentarios = item.comentarios
        item_model.receta = item.receta
        item_model.disponible = item.disponible
        item_model.unidades_disponibles = item.unidades_disponibles
        item_model.num_ingredientes = item.num_ingredientes
        item_model.kcal = item.kcal
        item_model.calorias = item.calorias
        item_model.proteinas = item.proteinas
        item_model.azucares = item.azucares
        item_model.descripcion = item.descripcion
        
        # Actualizar campos específicos
        if isinstance(item, Plato):
            plato_model = self.db.query(PlatoModel).filter(PlatoModel.id == item.id).first()
            if plato_model:
                plato_model.peso = item.peso
                plato_model.tipo_plato = item.tipo.value
        elif isinstance(item, Bebida):
            bebida_model = self.db.query(BebidaModel).filter(BebidaModel.id == item.id).first()
            if bebida_model:
                bebida_model.litros = item.litros
                bebida_model.alcoholico = item.alcoholico
        
        # Actualizar etiquetas
        self.db.query(ItemEtiquetaModel).filter(ItemEtiquetaModel.item_id == item.id).delete()
        for etiqueta in item.etiquetas:
            etiqueta_model = ItemEtiquetaModel(
                item_id=item.id,
                etiqueta=etiqueta.value
            )
            self.db.add(etiqueta_model)
        
        self.db.commit()
        self.db.refresh(item_model)
        
        return item_model.to_domain()
    
    def delete(self, item_id: int) -> bool:
        """
        Elimina un ítem por su ID.
        """
        item_model = self.db.query(ItemModel).filter(ItemModel.id == item_id).first()
        if not item_model:
            return False
        
        # Eliminar etiquetas asociadas
        self.db.query(ItemEtiquetaModel).filter(ItemEtiquetaModel.item_id == item_id).delete()
        
        # Eliminar el ítem
        self.db.delete(item_model)
        self.db.commit()
        
        return True
    
    def update_stock(self, item_id: int, new_stock: int) -> bool:
        """
        Actualiza el stock de un ítem.
        """
        item_model = self.db.query(ItemModel).filter(ItemModel.id == item_id).first()
        if not item_model:
            return False
        
        item_model.unidades_disponibles = new_stock
        item_model.disponible = new_stock > 0
        
        self.db.commit()
        return True


class PlatoRepositoryImpl(PlatoRepository):
    """
    Implementación concreta del repositorio de platos.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            db: Sesión de base de datos
        """
        self.db = db
    
    def create(self, plato: Plato) -> Plato:
        """
        Crea un nuevo plato en el repositorio.
        """
        # Usar el repositorio de ítems para crear el plato
        item_repo = ItemRepositoryImpl(self.db)
        return item_repo.create(plato)
    
    def get_by_tipo(self, tipo: EtiquetaPlato) -> List[Plato]:
        """
        Obtiene platos por tipo.
        """
        platos = self.db.query(ItemModel).join(PlatoModel).filter(
            PlatoModel.tipo_plato == tipo.value
        ).all()
        return [plato.to_domain() for plato in platos if isinstance(plato.to_domain(), Plato)]
    
    def get_entradas(self) -> List[Plato]:
        """
        Obtiene todos los platos de entrada.
        """
        return self.get_by_tipo(EtiquetaPlato.ENTRADA)
    
    def get_platos_principales(self) -> List[Plato]:
        """
        Obtiene todos los platos principales.
        """
        return self.get_by_tipo(EtiquetaPlato.FONDO)
    
    def get_postres(self) -> List[Plato]:
        """
        Obtiene todos los postres.
        """
        return self.get_by_tipo(EtiquetaPlato.POSTRE)


class BebidaRepositoryImpl(BebidaRepository):
    """
    Implementación concreta del repositorio de bebidas.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            db: Sesión de base de datos
        """
        self.db = db
    
    def create(self, bebida: Bebida) -> Bebida:
        """
        Crea una nueva bebida en el repositorio.
        """
        # Usar el repositorio de ítems para crear la bebida
        item_repo = ItemRepositoryImpl(self.db)
        return item_repo.create(bebida)
    
    def get_alcoholicas(self) -> List[Bebida]:
        """
        Obtiene todas las bebidas alcohólicas.
        """
        bebidas = self.db.query(ItemModel).join(BebidaModel).filter(
            BebidaModel.alcoholico == True
        ).all()
        return [bebida.to_domain() for bebida in bebidas if isinstance(bebida.to_domain(), Bebida)]
    
    def get_no_alcoholicas(self) -> List[Bebida]:
        """
        Obtiene todas las bebidas no alcohólicas.
        """
        bebidas = self.db.query(ItemModel).join(BebidaModel).filter(
            BebidaModel.alcoholico == False
        ).all()
        return [bebida.to_domain() for bebida in bebidas if isinstance(bebida.to_domain(), Bebida)]
    
    def get_by_volume_range(self, min_volume: Decimal, max_volume: Decimal) -> List[Bebida]:
        """
        Obtiene bebidas dentro de un rango de volumen.
        """
        bebidas = self.db.query(ItemModel).join(BebidaModel).filter(
            BebidaModel.litros >= min_volume,
            BebidaModel.litros <= max_volume
        ).all()
        return [bebida.to_domain() for bebida in bebidas if isinstance(bebida.to_domain(), Bebida)]
