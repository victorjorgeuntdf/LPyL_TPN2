import re

class Articulo:
    """
    Representa un artículo con título, autor y texto.
    """
    def __init__(self, titulo: str, autor: str, texto: str):
        self.titulo = titulo
        self.autor = autor
        self.texto = texto

    def snippet(self, length: int = 300) -> str:
        return (self.texto[:length] + "…") if len(self.texto) > length else self.texto

    def slug(self) -> str:
        s = self.titulo.lower()
        s = re.sub(r"[^a-z0-9]+", "-", s)
        return s.strip('-')
