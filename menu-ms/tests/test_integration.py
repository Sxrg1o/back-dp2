"""
Tests de integración para el microservicio de menú.
"""

import pytest
from decimal import Decimal
from sqlalchemy.orm import Session

from infrastructure.repositories import ItemRepositoryImpl, IngredienteRepositoryImpl
from application.services import ItemService, IngredienteService
from domain.entities import Plato, Bebida, Ingrediente
from domain.entities.enums import EtiquetaPlato, EtiquetaIngrediente, EtiquetaItem


class TestItemServiceIntegration:
    """Tests de integración para el servicio de ítems."""
    
    def test_crear_plato_completo(self, db_session: Session, sample_plato: Plato):
        """Test para crear un plato completo con persistencia."""
        # Arrange
        item_repository = ItemRepositoryImpl(db_session)
        plato_repository = ItemRepositoryImpl(db_session)  # Usar el mismo para simplicidad
        bebida_repository = ItemRepositoryImpl(db_session)  # Usar el mismo para simplicidad
        
        service = ItemService(item_repository, plato_repository, bebida_repository)
        
        # Act
        created_plato = service.create_item(sample_plato)
        
        # Assert
        assert created_plato.id is not None
        assert created_plato.descripcion == sample_plato.descripcion
        assert created_plato.precio == sample_plato.precio
        assert created_plato.peso == sample_plato.peso
        assert created_plato.tipo == sample_plato.tipo
        
        # Verificar que se persistió en la base de datos
        retrieved_plato = service.get_item(created_plato.id)
        assert retrieved_plato is not None
        assert retrieved_plato.descripcion == sample_plato.descripcion
    
    def test_crear_bebida_completa(self, db_session: Session, sample_bebida: Bebida):
        """Test para crear una bebida completa con persistencia."""
        # Arrange
        item_repository = ItemRepositoryImpl(db_session)
        plato_repository = ItemRepositoryImpl(db_session)
        bebida_repository = ItemRepositoryImpl(db_session)
        
        service = ItemService(item_repository, plato_repository, bebida_repository)
        
        # Act
        created_bebida = service.create_item(sample_bebida)
        
        # Assert
        assert created_bebida.id is not None
        assert created_bebida.descripcion == sample_bebida.descripcion
        assert created_bebida.precio == sample_bebida.precio
        assert created_bebida.litros == sample_bebida.litros
        assert created_bebida.alcoholico == sample_bebida.alcoholico
        
        # Verificar que se persistió en la base de datos
        retrieved_bebida = service.get_item(created_bebida.id)
        assert retrieved_bebida is not None
        assert retrieved_bebida.descripcion == sample_bebida.descripcion
    
    def test_obtener_todos_items(self, db_session: Session, sample_platos, sample_bebidas):
        """Test para obtener todos los ítems."""
        # Arrange
        item_repository = ItemRepositoryImpl(db_session)
        plato_repository = ItemRepositoryImpl(db_session)
        bebida_repository = ItemRepositoryImpl(db_session)
        
        service = ItemService(item_repository, plato_repository, bebida_repository)
        
        # Crear algunos ítems
        created_items = []
        for plato in sample_platos:
            created_items.append(service.create_item(plato))
        for bebida in sample_bebidas:
            created_items.append(service.create_item(bebida))
        
        # Act
        all_items = service.get_all_items()
        
        # Assert
        assert len(all_items) == len(created_items)
        assert all(item.id is not None for item in all_items)
    
    def test_buscar_items_por_nombre(self, db_session: Session, sample_platos):
        """Test para buscar ítems por nombre."""
        # Arrange
        item_repository = ItemRepositoryImpl(db_session)
        plato_repository = ItemRepositoryImpl(db_session)
        bebida_repository = ItemRepositoryImpl(db_session)
        
        service = ItemService(item_repository, plato_repository, bebida_repository)
        
        # Crear algunos platos
        for plato in sample_platos:
            service.create_item(plato)
        
        # Act
        search_results = service.search_items("Pasta")
        
        # Assert
        assert len(search_results) == 1
        assert "Pasta" in search_results[0].descripcion
    
    def test_obtener_platos_por_tipo(self, db_session: Session, sample_platos):
        """Test para obtener platos por tipo."""
        # Arrange
        item_repository = ItemRepositoryImpl(db_session)
        plato_repository = ItemRepositoryImpl(db_session)
        bebida_repository = ItemRepositoryImpl(db_session)
        
        service = ItemService(item_repository, plato_repository, bebida_repository)
        
        # Crear algunos platos
        for plato in sample_platos:
            service.create_item(plato)
        
        # Act
        entradas = service.get_entradas()
        platos_principales = service.get_platos_principales()
        postres = service.get_postres()
        
        # Assert
        assert len(entradas) == 1
        assert len(platos_principales) == 1
        assert len(postres) == 1
        
        assert entradas[0].tipo == EtiquetaPlato.ENTRADA
        assert platos_principales[0].tipo == EtiquetaPlato.FONDO
        assert postres[0].tipo == EtiquetaPlato.POSTRE
    
    def test_obtener_bebidas_por_tipo(self, db_session: Session, sample_bebidas):
        """Test para obtener bebidas por tipo."""
        # Arrange
        item_repository = ItemRepositoryImpl(db_session)
        plato_repository = ItemRepositoryImpl(db_session)
        bebida_repository = ItemRepositoryImpl(db_session)
        
        service = ItemService(item_repository, plato_repository, bebida_repository)
        
        # Crear algunas bebidas
        for bebida in sample_bebidas:
            service.create_item(bebida)
        
        # Act
        alcoholicas = service.get_bebidas_alcoholicas()
        no_alcoholicas = service.get_bebidas_no_alcoholicas()
        
        # Assert
        assert len(alcoholicas) == 1
        assert len(no_alcoholicas) == 2
        
        assert all(bebida.alcoholico for bebida in alcoholicas)
        assert all(not bebida.alcoholico for bebida in no_alcoholicas)


class TestIngredienteServiceIntegration:
    """Tests de integración para el servicio de ingredientes."""
    
    def test_crear_ingrediente_completo(self, db_session: Session, sample_ingrediente: Ingrediente):
        """Test para crear un ingrediente completo con persistencia."""
        # Arrange
        ingrediente_repository = IngredienteRepositoryImpl(db_session)
        service = IngredienteService(ingrediente_repository)
        
        # Act
        created_ingrediente = service.create_ingrediente(sample_ingrediente)
        
        # Assert
        assert created_ingrediente.id is not None
        assert created_ingrediente.nombre == sample_ingrediente.nombre
        assert created_ingrediente.stock == sample_ingrediente.stock
        assert created_ingrediente.peso == sample_ingrediente.peso
        assert created_ingrediente.tipo == sample_ingrediente.tipo
        
        # Verificar que se persistió en la base de datos
        retrieved_ingrediente = service.get_ingrediente(created_ingrediente.id)
        assert retrieved_ingrediente is not None
        assert retrieved_ingrediente.nombre == sample_ingrediente.nombre
    
    def test_obtener_ingredientes_por_tipo(self, db_session: Session, sample_ingredientes):
        """Test para obtener ingredientes por tipo."""
        # Arrange
        ingrediente_repository = IngredienteRepositoryImpl(db_session)
        service = IngredienteService(ingrediente_repository)
        
        # Crear algunos ingredientes
        for ingrediente in sample_ingredientes:
            service.create_ingrediente(ingrediente)
        
        # Act
        verduras = service.get_verduras()
        carnes = service.get_carnes()
        frutas = service.get_frutas()
        
        # Assert
        assert len(verduras) == 1
        assert len(carnes) == 1
        assert len(frutas) == 1
        
        assert verduras[0].tipo == EtiquetaIngrediente.VERDURA
        assert carnes[0].tipo == EtiquetaIngrediente.CARNE
        assert frutas[0].tipo == EtiquetaIngrediente.FRUTA
    
    def test_buscar_ingredientes_por_nombre(self, db_session: Session, sample_ingredientes):
        """Test para buscar ingredientes por nombre."""
        # Arrange
        ingrediente_repository = IngredienteRepositoryImpl(db_session)
        service = IngredienteService(ingrediente_repository)
        
        # Crear algunos ingredientes
        for ingrediente in sample_ingredientes:
            service.create_ingrediente(ingrediente)
        
        # Act
        search_results = service.search_ingredientes("Tomate")
        
        # Assert
        assert len(search_results) == 1
        assert "Tomate" in search_results[0].nombre
    
    def test_obtener_ingredientes_stock_bajo(self, db_session: Session):
        """Test para obtener ingredientes con stock bajo."""
        # Arrange
        ingrediente_repository = IngredienteRepositoryImpl(db_session)
        service = IngredienteService(ingrediente_repository)
        
        # Crear ingredientes con diferentes niveles de stock
        ingrediente_alto_stock = Ingrediente(
            nombre="Tomate",
            stock=Decimal('50.0'),
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.VERDURA
        )
        
        ingrediente_bajo_stock = Ingrediente(
            nombre="Pollo",
            stock=Decimal('5.0'),
            peso=Decimal('1.0'),
            tipo=EtiquetaIngrediente.CARNE
        )
        
        service.create_ingrediente(ingrediente_alto_stock)
        service.create_ingrediente(ingrediente_bajo_stock)
        
        # Act
        low_stock_ingredientes = service.get_ingredientes_low_stock(Decimal('10.0'))
        
        # Assert
        assert len(low_stock_ingredientes) == 1
        assert low_stock_ingredientes[0].nombre == "Pollo"
        assert low_stock_ingredientes[0].stock <= Decimal('10.0')
    
    def test_actualizar_stock_ingrediente(self, db_session: Session, sample_ingrediente: Ingrediente):
        """Test para actualizar el stock de un ingrediente."""
        # Arrange
        ingrediente_repository = IngredienteRepositoryImpl(db_session)
        service = IngredienteService(ingrediente_repository)
        
        created_ingrediente = service.create_ingrediente(sample_ingrediente)
        new_stock = Decimal('30.0')
        
        # Act
        success = service.update_ingrediente_stock(created_ingrediente.id, new_stock)
        
        # Assert
        assert success is True
        
        # Verificar que el stock se actualizó
        updated_ingrediente = service.get_ingrediente(created_ingrediente.id)
        assert updated_ingrediente.stock == new_stock
    
    def test_reducir_stock_ingrediente(self, db_session: Session, sample_ingrediente: Ingrediente):
        """Test para reducir el stock de un ingrediente."""
        # Arrange
        ingrediente_repository = IngredienteRepositoryImpl(db_session)
        service = IngredienteService(ingrediente_repository)
        
        created_ingrediente = service.create_ingrediente(sample_ingrediente)
        cantidad_a_reducir = Decimal('5.0')
        stock_original = created_ingrediente.stock
        
        # Act
        success = service.reduce_ingrediente_stock(created_ingrediente.id, cantidad_a_reducir)
        
        # Assert
        assert success is True
        
        # Verificar que el stock se redujo
        updated_ingrediente = service.get_ingrediente(created_ingrediente.id)
        assert updated_ingrediente.stock == stock_original - cantidad_a_reducir
