from typing import List
from .item import Item

class Opcion:
    def __init__(
        self,
        etiqueta: str,
        precioAdicional: float,
        es_default: bool = False,
        seleccionado: bool = False
    ):
        self.etiqueta = etiqueta
        self.precioAdicional = precioAdicional
        self.es_default = es_default
        self.seleccionado = seleccionado

    def __repr__(self):
        return (
            f"Opcion(etiqueta='{self.etiqueta}', precioAdicional={self.precioAdicional}, "
            f"es_default={self.es_default}, seleccionado={self.seleccionado})"
        )

class GrupoPersonalizacion:
    def __init__(
        self,
        item: Item = None,
        etiqueta: str = "",
        tipo: str = "",
        opciones: List[Opcion] = None
    ):
        self.item = item
        self.etiqueta = etiqueta
        self.tipo = tipo
        self.opciones = opciones

    def __repr__(self):
        return (
            f"GrupoPersonalizacion(item={self.item.nombre}, etiqueta='{self.etiqueta}', "
            f"tipo='{self.tipo}', opciones={self.opciones})"
        )