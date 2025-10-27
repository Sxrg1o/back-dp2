"""
Utilidades para formateo y normalización de texto.
"""

def normalize_to_title_case(text: str) -> str:
    """
    Normaliza un texto a formato Title Case (Primera Letra De Cada Palabra En Mayúscula).
    
    Convierte cualquier formato de texto (MAYÚSCULAS, minúsculas, MiXtO) a un formato
    consistente donde la primera letra de cada palabra está en mayúscula y el resto 
    en minúscula.
    
    Parameters
    ----------
    text : str
        El texto a normalizar.
        
    Returns
    -------
    str
        El texto normalizado en formato Title Case.
        
    Examples
    --------
    >>> normalize_to_title_case("BEBIDAS CALIENTES")
    'Bebidas Calientes'
    >>> normalize_to_title_case("postres especiales")
    'Postres Especiales'
    >>> normalize_to_title_case("PlAtOs PrInCiPaLeS")
    'Platos Principales'
    """
    if not text or not isinstance(text, str):
        return text
    
    return text.strip().title()


def normalize_category_name(category_name: str) -> str:
    """
    Normaliza específicamente el nombre de una categoría.
    
    Aplica la normalización de Title Case y cualquier regla específica
    que se requiera para los nombres de categorías.
    
    Parameters
    ----------
    category_name : str
        El nombre de la categoría a normalizar.
        
    Returns
    -------
    str
        El nombre de la categoría normalizado.
    """
    if not category_name or not isinstance(category_name, str):
        return category_name
    
    return normalize_to_title_case(category_name)


def normalize_product_name(product_name: str) -> str:
    """
    Normaliza específicamente el nombre de un producto/plato.
    
    Aplica la normalización de Title Case y cualquier regla específica
    que se requiera para los nombres de productos.
    
    Parameters
    ----------
    product_name : str
        El nombre del producto a normalizar.
        
    Returns
    -------
    str
        El nombre del producto normalizado.
        
    Examples
    --------
    >>> normalize_product_name("CEVICHE MIXTO")
    'Ceviche Mixto'
    >>> normalize_product_name("leche de tigre")
    'Leche De Tigre'
    >>> normalize_product_name("ArRoZ cOn MaRiScOs")
    'Arroz Con Mariscos'
    """
    if not product_name or not isinstance(product_name, str):
        return product_name
    
    return normalize_to_title_case(product_name)
