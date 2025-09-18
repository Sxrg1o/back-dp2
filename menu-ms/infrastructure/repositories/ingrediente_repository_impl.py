"""
Implementación concreta del repositorio de ingredientes.
"""

from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from domain.entities import Ingrediente
from domain.entities.enums import EtiquetaIngrediente
from domain.repositories import IngredienteRepository
from infrastructure.models.item_model import IngredienteModel


class IngredienteRepositoryImpl(IngredienteRepository):
    """
    Implementación concreta del repositorio de ingredientes.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            db: Sesión de base de datos
        """
        self.db = db
    
    def create(self, ingrediente: Ingrediente) -> Ingrediente:
        """
        Crea un nuevo ingrediente en el repositorio.
        """
        ingrediente_model = IngredienteModel(
            nombre=ingrediente.nombre,
            stock=float(ingrediente.stock) if ingrediente.stock is not None else 0.0,
            peso=float(ingrediente.peso) if ingrediente.peso is not None else 0.0,
            tipo=ingrediente.tipo.value
        )
        
        self.db.add(ingrediente_model)
        self.db.commit()
        self.db.refresh(ingrediente_model)
        
        return ingrediente_model.to_domain()
    
    def get_by_id(self, ingrediente_id: int) -> Optional[Ingrediente]:
        """
        Obtiene un ingrediente por su ID.
        """
        ingrediente_model = self.db.query(IngredienteModel).filter(
            IngredienteModel.id == ingrediente_id
        ).first()
        
        if ingrediente_model:
            return ingrediente_model.to_domain()
        return None
    
    def get_all(self) -> List[Ingrediente]:
        """
        Obtiene todos los ingredientes del repositorio.
        """
        ingredientes = self.db.query(IngredienteModel).all()
        return [ingrediente.to_domain() for ingrediente in ingredientes]
    
    def get_by_tipo(self, tipo: EtiquetaIngrediente) -> List[Ingrediente]:
        """
        Obtiene ingredientes por tipo.
        """
        ingredientes = self.db.query(IngredienteModel).filter(
            IngredienteModel.tipo == tipo.value
        ).all()
        return [ingrediente.to_domain() for ingrediente in ingredientes]
    
    def get_verduras(self) -> List[Ingrediente]:
        """
        Obtiene todos los ingredientes de tipo verdura.
        """
        return self.get_by_tipo(EtiquetaIngrediente.VERDURA)
    
    def get_carnes(self) -> List[Ingrediente]:
        """
        Obtiene todos los ingredientes de tipo carne.
        """
        return self.get_by_tipo(EtiquetaIngrediente.CARNE)
    
    def get_frutas(self) -> List[Ingrediente]:
        """
        Obtiene todos los ingredientes de tipo fruta.
        """
        return self.get_by_tipo(EtiquetaIngrediente.FRUTA)
    
    def search_by_name(self, name: str) -> List[Ingrediente]:
        """
        Busca ingredientes por nombre.
        """
        ingredientes = self.db.query(IngredienteModel).filter(
            IngredienteModel.nombre.ilike(f"%{name}%")
        ).all()
        return [ingrediente.to_domain() for ingrediente in ingredientes]
    
    def get_low_stock(self, threshold: Decimal = Decimal('10.0')) -> List[Ingrediente]:
        """
        Obtiene ingredientes con stock bajo.
        """
        ingredientes = self.db.query(IngredienteModel).filter(
            IngredienteModel.stock <= threshold
        ).all()
        return [ingrediente.to_domain() for ingrediente in ingredientes]
    
    def update(self, ingrediente: Ingrediente) -> Ingrediente:
        """
        Actualiza un ingrediente existente.
        """
        ingrediente_model = self.db.query(IngredienteModel).filter(
            IngredienteModel.id == ingrediente.id
        ).first()
        
        if not ingrediente_model:
            raise ValueError(f"No se encontró un ingrediente con ID {ingrediente.id}")
        
        ingrediente_model.nombre = ingrediente.nombre
        ingrediente_model.stock = ingrediente.stock
        ingrediente_model.peso = ingrediente.peso
        ingrediente_model.tipo = ingrediente.tipo.value
        
        self.db.commit()
        self.db.refresh(ingrediente_model)
        
        return ingrediente_model.to_domain()
    
    def delete(self, ingrediente_id: int) -> bool:
        """
        Elimina un ingrediente por su ID.
        """
        ingrediente_model = self.db.query(IngredienteModel).filter(
            IngredienteModel.id == ingrediente_id
        ).first()
        
        if not ingrediente_model:
            return False
        
        self.db.delete(ingrediente_model)
        self.db.commit()
        
        return True
    
    def update_stock(self, ingrediente_id: int, new_stock: Decimal) -> bool:
        """
        Actualiza el stock de un ingrediente.
        """
        ingrediente_model = self.db.query(IngredienteModel).filter(
            IngredienteModel.id == ingrediente_id
        ).first()
        
        if not ingrediente_model:
            return False
        
        ingrediente_model.stock = new_stock
        self.db.commit()
        
        return True
    
    def reduce_stock(self, ingrediente_id: int, cantidad: Decimal) -> bool:
        """
        Reduce el stock de un ingrediente.
        """
        ingrediente_model = self.db.query(IngredienteModel).filter(
            IngredienteModel.id == ingrediente_id
        ).first()
        
        if not ingrediente_model:
            return False
        
        if ingrediente_model.stock < cantidad:
            return False
        
        ingrediente_model.stock -= cantidad
        self.db.commit()
        
        return True
