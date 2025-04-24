import re

class InvalidArticleError(Exception):
    """Excepción de validación, ahora usada en ParserHtml."""
    pass

class Articulo:
    """
    Representa un artículo con título, autor y texto.
    """
    def __init__(self, titulo: str, autor: str, texto: str):
        # Sólo limpiamos, no validamos longitud
        self.titulo = titulo.strip()
        self.autor  = autor.strip()
        self.texto  = texto.strip()

    def snippet(self, length: int = 300) -> str:
        return (self.texto[:length] + "…") if len(self.texto) > length else self.texto

    def slug(self) -> str:
        s = self.titulo.lower()
        return re.sub(r"[^a-z0-9]+", "-", s).strip('-')
