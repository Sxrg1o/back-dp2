"""
Tests unitarios para las entidades del dominio.
"""

import pytest
from decimal import Decimal
from domain.entities import Item, Plato, Bebida, Ingrediente
from domain.entities.enums import EtiquetaItem, EtiquetaIngrediente, EtiquetaPlato


class TestIngrediente:
    """Tests para la entidad Ingrediente."""
    
    def test_crear_ingrediente_basico(self):
        """Test para crear un ingrediente básico."""
        ingrediente = Ingrediente(
            nombre="Tomate",
            stock=Decimal('10.0'),
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.VERDURA
        )
        
        assert ingrediente.nombre == "Tomate"
        assert ingrediente.stock == Decimal('10.0')
        assert ingrediente.peso == Decimal('0.2')
        assert ingrediente.tipo == EtiquetaIngrediente.VERDURA
    
    def test_verificar_stock_suficiente(self):
        """Test para verificar stock suficiente."""
        ingrediente = Ingrediente(
            nombre="Tomate",
            stock=Decimal('10.0'),
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.VERDURA
        )
        
        assert ingrediente.verificar_stock(Decimal('5.0')) is True
        assert ingrediente.verificar_stock(Decimal('10.0')) is True
        assert ingrediente.verificar_stock(Decimal('15.0')) is False
    
    def test_reducir_stock_exitoso(self):
        """Test para reducir stock exitosamente."""
        ingrediente = Ingrediente(
            nombre="Tomate",
            stock=Decimal('10.0'),
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.VERDURA
        )
        
        assert ingrediente.reducir_stock(Decimal('3.0')) is True
        assert ingrediente.stock == Decimal('7.0')
    
    def test_reducir_stock_insuficiente(self):
        """Test para reducir stock cuando no hay suficiente."""
        ingrediente = Ingrediente(
            nombre="Tomate",
            stock=Decimal('5.0'),
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.VERDURA
        )
        
        assert ingrediente.reducir_stock(Decimal('10.0')) is False
        assert ingrediente.stock == Decimal('5.0')  # No cambia
    
    def test_calcular_peso_total(self):
        """Test para calcular peso total."""
        ingrediente = Ingrediente(
            nombre="Tomate",
            stock=Decimal('10.0'),
            peso=Decimal('0.2'),
            tipo=EtiquetaIngrediente.VERDURA
        )
        
        assert ingrediente.calcular_peso_total() == Decimal('2.0')


class TestPlato:
    """Tests para la entidad Plato."""
    
    def test_crear_plato_basico(self):
        """Test para crear un plato básico."""
        plato = Plato(
            descripcion="Pasta Carbonara",
            precio=Decimal('15.50'),
            peso=Decimal('300.0'),
            tipo=EtiquetaPlato.FONDO
        )
        
        assert plato.descripcion == "Pasta Carbonara"
        assert plato.precio == Decimal('15.50')
        assert plato.peso == Decimal('300.0')
        assert plato.tipo == EtiquetaPlato.FONDO
        assert plato.get_tipo() == "PLATO"
    
    def test_es_plato_principal(self):
        """Test para verificar si es plato principal."""
        plato = Plato(
            descripcion="Pasta Carbonara",
            precio=Decimal('15.50'),
            peso=Decimal('300.0'),
            tipo=EtiquetaPlato.FONDO
        )
        
        assert plato.es_plato_principal() is True
        assert plato.es_entrada() is False
        assert plato.es_postre() is False
    
    def test_calcular_densidad_calorica(self):
        """Test para calcular densidad calórica."""
        plato = Plato(
            descripcion="Pasta Carbonara",
            precio=Decimal('15.50'),
            peso=Decimal('300.0'),
            calorias=Decimal('600.0')
        )
        
        assert plato.calcular_densidad_calorica() == Decimal('2.0')


class TestBebida:
    """Tests para la entidad Bebida."""
    
    def test_crear_bebida_basica(self):
        """Test para crear una bebida básica."""
        bebida = Bebida(
            descripcion="Coca Cola",
            precio=Decimal('3.50'),
            litros=Decimal('0.5'),
            alcoholico=False
        )
        
        assert bebida.descripcion == "Coca Cola"
        assert bebida.precio == Decimal('3.50')
        assert bebida.litros == Decimal('0.5')
        assert bebida.alcoholico is False
        assert bebida.get_tipo() == "BEBIDA"
    
    def test_es_alcoholica(self):
        """Test para verificar si es alcohólica."""
        bebida_alcoholica = Bebida(
            descripcion="Cerveza",
            precio=Decimal('4.50'),
            litros=Decimal('0.5'),
            alcoholico=True
        )
        
        bebida_no_alcoholica = Bebida(
            descripcion="Agua",
            precio=Decimal('2.00'),
            litros=Decimal('0.5'),
            alcoholico=False
        )
        
        assert bebida_alcoholica.es_alcoholica() is True
        assert bebida_no_alcoholica.es_alcoholica() is False
    
    def test_es_apta_para_menores(self):
        """Test para verificar si es apta para menores."""
        bebida_alcoholica = Bebida(
            descripcion="Cerveza",
            precio=Decimal('4.50'),
            litros=Decimal('0.5'),
            alcoholico=True
        )
        
        bebida_no_alcoholica = Bebida(
            descripcion="Agua",
            precio=Decimal('2.00'),
            litros=Decimal('0.5'),
            alcoholico=False
        )
        
        assert bebida_alcoholica.es_apta_para_menores() is False
        assert bebida_no_alcoholica.es_apta_para_menores() is True
    
    def test_calcular_calorias_por_ml(self):
        """Test para calcular calorías por mililitro."""
        bebida = Bebida(
            descripcion="Coca Cola",
            precio=Decimal('3.50'),
            litros=Decimal('0.5'),
            calorias=Decimal('200.0')
        )
        
        # 200 calorías / (0.5 litros * 1000 ml/litro) = 0.4 cal/ml
        assert bebida.calcular_calorias_por_ml() == Decimal('0.4')


class TestItem:
    """Tests para la entidad Item base."""
    
    def test_verificar_stock_disponible(self):
        """Test para verificar stock disponible."""
        plato = Plato(
            descripcion="Pasta",
            precio=Decimal('10.0'),
            peso=Decimal('300.0'),
            unidades_disponibles=5,
            disponible=True
        )
        
        assert plato.verificar_stock() is True
    
    def test_verificar_stock_no_disponible(self):
        """Test para verificar stock no disponible."""
        plato = Plato(
            descripcion="Pasta",
            precio=Decimal('10.0'),
            peso=Decimal('300.0'),
            unidades_disponibles=0,
            disponible=False
        )
        
        assert plato.verificar_stock() is False
    
    def test_reducir_stock_exitoso(self):
        """Test para reducir stock exitosamente."""
        plato = Plato(
            descripcion="Pasta",
            precio=Decimal('10.0'),
            peso=Decimal('300.0'),
            unidades_disponibles=5,
            disponible=True
        )
        
        assert plato.reducir_stock(2) is True
        assert plato.unidades_disponibles == 3
        assert plato.disponible is True
    
    def test_reducir_stock_agotar(self):
        """Test para reducir stock hasta agotarlo."""
        plato = Plato(
            descripcion="Pasta",
            precio=Decimal('10.0'),
            peso=Decimal('300.0'),
            unidades_disponibles=2,
            disponible=True
        )
        
        assert plato.reducir_stock(2) is True
        assert plato.unidades_disponibles == 0
        assert plato.disponible is False
    
    def test_agregar_etiqueta(self):
        """Test para agregar etiqueta."""
        plato = Plato(
            descripcion="Pasta",
            precio=Decimal('10.0'),
            peso=Decimal('300.0')
        )
        
        plato.agregar_etiqueta(EtiquetaItem.VEGANO)
        assert EtiquetaItem.VEGANO in plato.etiquetas
    
    def test_remover_etiqueta(self):
        """Test para remover etiqueta."""
        plato = Plato(
            descripcion="Pasta",
            precio=Decimal('10.0'),
            peso=Decimal('300.0'),
            etiquetas=[EtiquetaItem.VEGANO, EtiquetaItem.SIN_GLUTEN]
        )
        
        plato.remover_etiqueta(EtiquetaItem.VEGANO)
        assert EtiquetaItem.VEGANO not in plato.etiquetas
        assert EtiquetaItem.SIN_GLUTEN in plato.etiquetas
    
    def test_tiene_etiqueta(self):
        """Test para verificar si tiene etiqueta."""
        plato = Plato(
            descripcion="Pasta",
            precio=Decimal('10.0'),
            peso=Decimal('300.0'),
            etiquetas=[EtiquetaItem.VEGANO]
        )
        
        assert plato.tiene_etiqueta(EtiquetaItem.VEGANO) is True
        assert plato.tiene_etiqueta(EtiquetaItem.SIN_GLUTEN) is False
