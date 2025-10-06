"""
Unit tests for RolMySQLRepository
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from src.repositories.auth.rol_mysql_repository import RolMySQLRepository
from src.models.auth.rol_model import RolModel


@pytest.mark.asyncio
async def test_get_by_id():
    """
    Verifica que get_by_id obtiene un rol correctamente.
    """
    mock_db = AsyncMock()

    # Rol esperado
    rol_esperado = RolModel(
        id_rol=1,
        nombre="admin",
        descripcion="Administrador"
    )

    # Configurar mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = rol_esperado
    mock_db.execute.return_value = mock_result

    # Ejecutar
    repo = RolMySQLRepository()
    resultado = await repo.get_by_id(mock_db, 1)

    # Verificar
    assert resultado is not None
    assert resultado.id_rol == 1
    assert resultado.nombre == "admin"
    mock_db.execute.assert_called_once()


@pytest.mark.asyncio
async def test_create_rol():
    """
    Verifica que create_rol crea un rol correctamente.
    """
    mock_db = AsyncMock()

    # Mock del resultado de insert
    mock_result = MagicMock()
    mock_result.inserted_primary_key = [1]
    mock_db.execute.return_value = mock_result

    # Mock para get_by_id (se llama después del insert)
    rol_creado = RolModel(
        id_rol=1,
        nombre="nuevo_rol",
        descripcion="Descripción del rol"
    )

    # Ejecutar con patch de get_by_id
    repo = RolMySQLRepository()

    # Simular que get_by_id devuelve el rol creado
    with pytest.mock.patch.object(repo, 'get_by_id', new=AsyncMock(return_value=rol_creado)):
        resultado = await repo.create_rol(
            mock_db,
            nombre="nuevo_rol",
            descripcion="Descripción del rol"
        )

    # Verificar
    assert resultado is not None
    assert resultado.nombre == "nuevo_rol"
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_roles():
    """
    Verifica que get_all obtiene todos los roles.
    """
    mock_db = AsyncMock()

    # Roles esperados
    roles_esperados = [
        RolModel(id_rol=1, nombre="admin"),
        RolModel(id_rol=2, nombre="mesero"),
        RolModel(id_rol=3, nombre="cocinero")
    ]

    # Configurar mock
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = roles_esperados
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result

    # Ejecutar
    repo = RolMySQLRepository()
    resultado = await repo.get_all(mock_db)

    # Verificar
    assert len(resultado) == 3
    assert resultado[0].nombre == "admin"
    assert resultado[1].nombre == "mesero"
    mock_db.execute.assert_called_once()
