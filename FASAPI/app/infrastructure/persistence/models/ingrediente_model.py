"""SQLAlchemy model for Ingrediente entity."""

from sqlalchemy import Column, String, Float, DateTime, ForeignKey

from app.infrastructure.persistence.models.item_model import ItemModel


class IngredienteModel(ItemModel):
    """SQLAlchemy model for Ingrediente persistence."""
    
    __tablename__ = "ingredientes"
    
    # Foreign key to parent table for joined table inheritance
    id = Column(String, ForeignKey("items.id"), primary_key=True)
    
    # Ingredient-specific fields
    tipo_ingrediente = Column(String(50), nullable=False)  # EtiquetaIngrediente enum value
    peso_unitario = Column(Float, nullable=False)  # in grams
    unidad_medida = Column(String(50), nullable=False)  # e.g., "gramos", "litros", "unidades"
    fecha_vencimiento = Column(DateTime(timezone=True))
    proveedor = Column(String(255))
    
    __mapper_args__ = {
        "polymorphic_identity": "ingrediente",
    }