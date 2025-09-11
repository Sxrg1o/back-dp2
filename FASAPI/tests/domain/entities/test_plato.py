"""
Tests for Plato domain entity.
"""
import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from app.domain.entities.plato import Plato
from app.domain.entities.ingrediente import Ingrediente
from app.domain.value_objects.precio import Precio
from app.domain.value_objects.informacion_nutricional import InformacionNutricional
from app.domain.value_objects.etiqueta_plato import EtiquetaPlato
from app.domain.value_objects.etiqueta_item import EtiquetaItem
from app.domain.value_objects.etiqueta_ingrediente import EtiquetaIngrediente
from app.domain.exceptions.menu_exceptions import RecipeValidationError, IngredienteNotFoundError


class TestPlato:
    """Test cases for Plato domain entity."""

    def test_valid_plato_creation(self):
        """Test creating a valid plato."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=350,
            proteinas=Decimal("25.5"),
            azucares=Decimal("5.0"),
            grasas=Decimal("12.0"),
            carbohidratos=Decimal("30.0"),
            fibra=Decimal("8.0"),
            sodio=Decimal("500.0")
        )
        
        plato = Plato(
            id=uuid4(),
            nombre="Pasta Carbonara",
            descripcion="Delicious pasta with bacon and cream",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=25,
            stock_actual=10,
            stock_minimo=2,
            activo=True,
            etiquetas={EtiquetaItem.CON_GLUTEN},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            receta={},
            tipo_plato=EtiquetaPlato.FONDO,
            instrucciones="Cook pasta, add sauce",
            dificultad="medio",
            chef_recomendado="Chef Mario"
        )
        
        assert plato.nombre == "Pasta Carbonara"
        assert plato.tipo_plato == EtiquetaPlato.FONDO
        assert plato.dificultad == "medio"
        assert plato.chef_recomendado == "Chef Mario"
        assert plato.instrucciones == "Cook pasta, add sauce"
        assert plato.receta == {}

    def test_invalid_empty_recipe_instructions(self):
        """Test that empty recipe instructions raise error."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=350,
            proteinas=Decimal("25.5"),
            azucares=Decimal("5.0"),
            grasas=Decimal("12.0"),
            carbohidratos=Decimal("30.0"),
            fibra=Decimal("8.0"),
            sodio=Decimal("500.0")
        )
        
        with pytest.raises(ValueError, match="Instructions cannot be empty"):
            Plato(
                id=uuid4(),
                nombre="Pasta Carbonara",
                descripcion="Delicious pasta",
                precio=precio,
                informacion_nutricional=info_nutricional,
                tiempo_preparacion=25,
                stock_actual=10,
                stock_minimo=2,
                activo=True,
                etiquetas={EtiquetaItem.CON_GLUTEN},
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                version=1,
                receta={},
                tipo_plato=EtiquetaPlato.FONDO,
                instrucciones="",  # Empty instructions
                dificultad="medio",
                chef_recomendado="Chef Mario"
            )

    def test_invalid_difficulty_level(self):
        """Test that invalid difficulty level raises error."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=350,
            proteinas=Decimal("25.5"),
            azucares=Decimal("5.0"),
            grasas=Decimal("12.0"),
            carbohidratos=Decimal("30.0"),
            fibra=Decimal("8.0"),
            sodio=Decimal("500.0")
        )
        
        with pytest.raises(ValueError, match="Difficulty must be 'facil', 'medio', or 'dificil'"):
            Plato(
                id=uuid4(),
                nombre="Pasta Carbonara",
                descripcion="Delicious pasta",
                precio=precio,
                informacion_nutricional=info_nutricional,
                tiempo_preparacion=25,
                stock_actual=10,
                stock_minimo=2,
                activo=True,
                etiquetas={EtiquetaItem.CON_GLUTEN},
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                version=1,
                receta={},
                tipo_plato=EtiquetaPlato.FONDO,
                instrucciones="Cook pasta",
                dificultad="impossible",  # Invalid difficulty
                chef_recomendado="Chef Mario"
            )

    def test_agregar_ingrediente_receta(self):
        """Test adding ingredient to recipe."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=350,
            proteinas=Decimal("25.5"),
            azucares=Decimal("5.0"),
            grasas=Decimal("12.0"),
            carbohidratos=Decimal("30.0"),
            fibra=Decimal("8.0"),
            sodio=Decimal("500.0")
        )
        
        plato = Plato(
            id=uuid4(),
            nombre="Pasta Carbonara",
            descripcion="Delicious pasta",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=25,
            stock_actual=10,
            stock_minimo=2,
            activo=True,
            etiquetas={EtiquetaItem.CON_GLUTEN},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            receta={},
            tipo_plato=EtiquetaPlato.FONDO,
            instrucciones="Cook pasta",
            dificultad="medio",
            chef_recomendado="Chef Mario"
        )
        
        ingrediente_id = uuid4()
        plato.agregar_ingrediente_receta(ingrediente_id, Decimal("200.0"))
        
        assert ingrediente_id in plato.receta
        assert plato.receta[ingrediente_id] == Decimal("200.0")

    def test_agregar_ingrediente_invalid_quantity(self):
        """Test adding ingredient with invalid quantity."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=350,
            proteinas=Decimal("25.5"),
            azucares=Decimal("5.0"),
            grasas=Decimal("12.0"),
            carbohidratos=Decimal("30.0"),
            fibra=Decimal("8.0"),
            sodio=Decimal("500.0")
        )
        
        plato = Plato(
            id=uuid4(),
            nombre="Pasta Carbonara",
            descripcion="Delicious pasta",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=25,
            stock_actual=10,
            stock_minimo=2,
            activo=True,
            etiquetas={EtiquetaItem.CON_GLUTEN},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            receta={},
            tipo_plato=EtiquetaPlato.FONDO,
            instrucciones="Cook pasta",
            dificultad="medio",
            chef_recomendado="Chef Mario"
        )
        
        with pytest.raises(ValueError, match="Quantity must be positive"):
            plato.agregar_ingrediente_receta(uuid4(), Decimal("-1.0"))

    def test_remover_ingrediente_receta(self):
        """Test removing ingredient from recipe."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=350,
            proteinas=Decimal("25.5"),
            azucares=Decimal("5.0"),
            grasas=Decimal("12.0"),
            carbohidratos=Decimal("30.0"),
            fibra=Decimal("8.0"),
            sodio=Decimal("500.0")
        )
        
        plato = Plato(
            id=uuid4(),
            nombre="Pasta Carbonara",
            descripcion="Delicious pasta",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=25,
            stock_actual=10,
            stock_minimo=2,
            activo=True,
            etiquetas={EtiquetaItem.CON_GLUTEN},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            receta={},
            tipo_plato=EtiquetaPlato.FONDO,
            instrucciones="Cook pasta",
            dificultad="medio",
            chef_recomendado="Chef Mario"
        )
        
        ingrediente_id = uuid4()
        plato.agregar_ingrediente_receta(ingrediente_id, Decimal("200.0"))
        plato.remover_ingrediente_receta(ingrediente_id)
        
        assert ingrediente_id not in plato.receta

    def test_remover_ingrediente_not_in_recipe(self):
        """Test removing ingredient that's not in recipe."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=350,
            proteinas=Decimal("25.5"),
            azucares=Decimal("5.0"),
            grasas=Decimal("12.0"),
            carbohidratos=Decimal("30.0"),
            fibra=Decimal("8.0"),
            sodio=Decimal("500.0")
        )
        
        plato = Plato(
            id=uuid4(),
            nombre="Pasta Carbonara",
            descripcion="Delicious pasta",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=25,
            stock_actual=10,
            stock_minimo=2,
            activo=True,
            etiquetas={EtiquetaItem.CON_GLUTEN},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            receta={},
            tipo_plato=EtiquetaPlato.FONDO,
            instrucciones="Cook pasta",
            dificultad="medio",
            chef_recomendado="Chef Mario"
        )
        
        with pytest.raises(IngredienteNotFoundError):
            plato.remover_ingrediente_receta(uuid4())

    def test_actualizar_cantidad_ingrediente(self):
        """Test updating ingredient quantity in recipe."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=350,
            proteinas=Decimal("25.5"),
            azucares=Decimal("5.0"),
            grasas=Decimal("12.0"),
            carbohidratos=Decimal("30.0"),
            fibra=Decimal("8.0"),
            sodio=Decimal("500.0")
        )
        
        plato = Plato(
            id=uuid4(),
            nombre="Pasta Carbonara",
            descripcion="Delicious pasta",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=25,
            stock_actual=10,
            stock_minimo=2,
            activo=True,
            etiquetas={EtiquetaItem.CON_GLUTEN},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            receta={},
            tipo_plato=EtiquetaPlato.FONDO,
            instrucciones="Cook pasta",
            dificultad="medio",
            chef_recomendado="Chef Mario"
        )
        
        ingrediente_id = uuid4()
        plato.agregar_ingrediente_receta(ingrediente_id, Decimal("200.0"))
        plato.actualizar_cantidad_ingrediente(ingrediente_id, Decimal("300.0"))
        
        assert plato.receta[ingrediente_id] == Decimal("300.0")

    def test_get_ingredientes_necesarios(self):
        """Test getting necessary ingredients for recipe."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=350,
            proteinas=Decimal("25.5"),
            azucares=Decimal("5.0"),
            grasas=Decimal("12.0"),
            carbohidratos=Decimal("30.0"),
            fibra=Decimal("8.0"),
            sodio=Decimal("500.0")
        )
        
        plato = Plato(
            id=uuid4(),
            nombre="Pasta Carbonara",
            descripcion="Delicious pasta",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=25,
            stock_actual=10,
            stock_minimo=2,
            activo=True,
            etiquetas={EtiquetaItem.CON_GLUTEN},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            receta={},
            tipo_plato=EtiquetaPlato.FONDO,
            instrucciones="Cook pasta",
            dificultad="medio",
            chef_recomendado="Chef Mario"
        )
        
        ingrediente1_id = uuid4()
        ingrediente2_id = uuid4()
        plato.agregar_ingrediente_receta(ingrediente1_id, Decimal("200.0"))
        plato.agregar_ingrediente_receta(ingrediente2_id, Decimal("100.0"))
        
        ingredientes = plato.get_ingredientes_necesarios()
        
        assert len(ingredientes) == 2
        assert ingrediente1_id in ingredientes
        assert ingrediente2_id in ingredientes

    def test_calcular_costo_ingredientes(self):
        """Test calculating ingredient costs."""
        precio = Precio(Decimal("15.99"))
        info_nutricional = InformacionNutricional(
            calorias=350,
            proteinas=Decimal("25.5"),
            azucares=Decimal("5.0"),
            grasas=Decimal("12.0"),
            carbohidratos=Decimal("30.0"),
            fibra=Decimal("8.0"),
            sodio=Decimal("500.0")
        )
        
        plato = Plato(
            id=uuid4(),
            nombre="Pasta Carbonara",
            descripcion="Delicious pasta",
            precio=precio,
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=25,
            stock_actual=10,
            stock_minimo=2,
            activo=True,
            etiquetas={EtiquetaItem.CON_GLUTEN},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            receta={},
            tipo_plato=EtiquetaPlato.FONDO,
            instrucciones="Cook pasta",
            dificultad="medio",
            chef_recomendado="Chef Mario"
        )
        
        # Create mock ingredients with prices
        ingrediente1 = Ingrediente(
            id=uuid4(),
            nombre="Pasta",
            descripcion="Fresh pasta",
            precio=Precio(Decimal("2.50")),
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=0,
            stock_actual=100,
            stock_minimo=10,
            activo=True,
            etiquetas={EtiquetaItem.CON_GLUTEN},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            peso_unitario=Decimal("500.0"),
            unidad_medida="gramos",
            fecha_vencimiento=datetime.utcnow() + timedelta(days=30),
            proveedor="Pasta Co",
            tipo=EtiquetaIngrediente.VERDURA
        )
        
        ingrediente2 = Ingrediente(
            id=uuid4(),
            nombre="Bacon",
            descripcion="Crispy bacon",
            precio=Precio(Decimal("5.00")),
            informacion_nutricional=info_nutricional,
            tiempo_preparacion=0,
            stock_actual=50,
            stock_minimo=5,
            activo=True,
            etiquetas={EtiquetaItem.SIN_GLUTEN},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            version=1,
            peso_unitario=Decimal("200.0"),
            unidad_medida="gramos",
            fecha_vencimiento=datetime.utcnow() + timedelta(days=7),
            proveedor="Meat Co",
            tipo=EtiquetaIngrediente.CARNE
        )
        
        plato.agregar_ingrediente_receta(ingrediente1.id, Decimal("200.0"))
        plato.agregar_ingrediente_receta(ingrediente2.id, Decimal("100.0"))
        
        ingredientes_disponibles = [ingrediente1, ingrediente2]
        costo_total = plato.calcular_costo_ingredientes(ingredientes_disponibles)
        
        # Cost calculation: (200g pasta / 500g) * 2.50 + (100g bacon / 200g) * 5.00
        # = 0.4 * 2.50 + 0.5 * 5.00 = 1.00 + 2.50 = 3.50
        assert costo_total == Decimal("3.50")
