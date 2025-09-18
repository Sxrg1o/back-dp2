"""
Configuración del paquete para el microservicio de menú.
"""

from setuptools import setup, find_packages

setup(
    name="menu-ms",
    version="1.0.0",
    description="Microservicio de Menú y Carta para el restaurante Domótica",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.116.1",
        "uvicorn[standard]>=0.35.0",
        "pydantic>=2.11.9",
        "sqlalchemy>=2.0.43",
        "python-multipart>=0.0.12",
    ],
)
