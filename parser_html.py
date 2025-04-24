import os
import re
from datetime import datetime
from collections import OrderedDict
from articulo import Articulo

class ParserHtml:
    """
    Genera index.html y páginas individuales para artículos.
    """
    def __init__(self, articulos, output_dir="output"):
        # Normaliza espacios y capitaliza autor
        self.articulos = self._filter_and_normalize(articulos)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _filter_and_normalize(self, articulos):
        resultado = []
        for art in articulos:
            if art.titulo.strip() and art.autor.strip() and art.texto.strip():
                # Capitalizar cada parte del autor
                partes = art.autor.strip().split()
                autor_norm = " ".join(p.capitalize() for p in partes)
                resultado.append(Articulo(art.titulo.strip(), autor_norm, art.texto.strip()))
        return resultado

    def filter_by_keyword(self, keyword: str):
        return [art for art in self.articulos if keyword.lower() in art.texto.lower()]

    def generate_html(self, keyword: str = None):
        subset = self.filter_by_keyword(keyword) if keyword else self.articulos
        self._generate_index(subset)
        self._generate_article_pages(subset)

    def _generate_index(self, subset):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        by_author = OrderedDict()
        for art in subset:
            by_author.setdefault(art.autor, []).append(art)

        html = """<!DOCTYPE html>
<html lang=\"es\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">
  <title>Noticias del Fuego</title>
  <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">
  <style>
    body { margin:0; padding:0; font-family:'Segoe UI', Tahoma, sans-serif; background:#f5f5f5; color:#333; }
    .header { background-image:url('../static/foto_faro.jpg'); background-size:cover; background-position:center; min-height:500px; display:flex; align-items:center; justify-content:center; color:#fff; }
    .header img.logo { height:100px; width:100px; }
    .header h1 { margin:0; font-size:2.75rem; text-shadow:2px 2px 4px rgba(0,0,0,0.8); }
    .footer { text-align:center; padding:1rem; font-size:.8rem; color:#999; }
  </style>
</head>
<body>
  <div class=\"header\">
    <img src=\"../static/noticias_del_fuego.png\" class=\"logo\">
    <h1>Noticias del Fuego</h1>
  </div>
  <div class=\"container my-4\">
    <nav class=\"toc d-flex flex-wrap gap-2 mb-4\">
      <h2 class=\"me-3 text-primary\">Índice de Autores</h2>"""
        for autor in by_author:
            anchor = autor.lower().replace(' ', '-')
            html += f"\n      <a href=\"#autor-{anchor}\" class=\"btn btn-outline-primary btn-sm\">{autor}</a>"
        html += "\n    </nav>\n"
        for autor, arts in by_author.items():
            anchor = autor.lower().replace(' ', '-')
            html += f"    <section id=\"autor-{anchor}\" class=\"mb-5\">\n      <h3 class=\"text-primary\">{autor}</h3>\n      <div class=\"row\">"
            for art in arts:
                html += f"\n        <a href=\"{art.slug()}.html\" class=\"col-md-4 mb-4 text-decoration-none\">\n          <div class=\"card h-100\"><div class=\"card-body d-flex flex-column\">\n            <h5 class=\"card-title text-primary\">{art.titulo}</h5>\n            <p class=\"card-text flex-grow-1\">{art.snippet()}</p>\n          </div></div>\n        </a>"
            html += "\n      </div>\n    </section>"
        html += f"\n  </div>\n  <div class=\"footer\">&copy; 2025 - Laboratorio de Programación y Lenguajes<br>Powered by ViktorDev<br>Generado el: {now}</div>\n"
        html += "<script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js\"></script>\n</body>\n</html>"
        path = os.path.join(self.output_dir, 'index.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

    def _generate_article_pages(self, subset):
        for art in subset:
            content = self._build_article(art)
            path = os.path.join(self.output_dir, f"{art.slug()}.html")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

    def _build_article(self, art: Articulo) -> str:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        html = """<!DOCTYPE html>
<html lang=\"es\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">
  <title>""" + art.titulo + """</title>
  <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">\n  <style>\n    body { margin:0; padding:0; font-family:'Segoe UI', Tahoma, sans-serif; background:#f5f5f5; color:#333; }\n    .header { background-image:url('../static/foto_faro.jpg'); background-size:cover; background-position:center; min-height:500px; display:flex; align-items:center; justify-content:center; color:#fff; }\n    .header img.logo { height:100px; width:100px; }\n    .header h1 { margin:0; font-size:2.75rem; text-shadow:2px 2px 4px rgba(0,0,0,0.8); }\n    .footer { text-align:center; padding:1rem; font-size:.8rem; color:#999; }\n  </style>\n</head>\n<body>\n  <div class=\"header\"> <img src=\"../static/noticias_del_fuego.png\" class=\"logo\"> <h1>Noticias del Fuego</h1> </div>\n  <nav class=\"navbar bg-light shadow-sm\"><div class=\"container\"><a class=\"navbar-brand\" href=\"index.html\">&larr; Volver al índice</a></div></nav>\n  <div class=\"container my-5 bg-white p-4 shadow-sm\">\n    <h2 class=\"text-primary\">""" + art.titulo + """</h2>\n    <p class=\"fst-italic text-muted\">Por """ + art.autor + """</p>\n    <p>""" + art.texto + """</p>\n  </div>\n  <div class=\"footer\">&copy; 2025 - Laboratorio de Programación y Lenguajes<br>Powered by ViktorDev<br>Generado el: """ + now + """</div>\n  <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js\"></script>\n</body>\n</html>"""
        return html
