import os
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
        content = self._build_index(subset)
        path = os.path.join(self.output_dir, 'index.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Índice generado: {path}")

    def _generate_article_pages(self, subset):
        for art in subset:
            fname = f"{art.slug()}.html"
            path = os.path.join(self.output_dir, fname)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self._build_article(art))
            print(f"Página generada: {path}")

    def _build_index(self, subset):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        by_author = OrderedDict()
        for art in subset:
            by_author.setdefault(art.autor, []).append(art)

        html = []
        # Head with updated footer CSS
        html.append("<!DOCTYPE html>")
        html.append("<html lang='es'>")
        html.append("<head>")
        html.append("  <meta charset='UTF-8'>")
        html.append("  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>")
        html.append("  <title>Noticias del Fuego</title>")
        html.append("  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>")
        html.append("  <style>")
        html.append("    body { margin:0; padding:0; font-family:'Segoe UI', Tahoma, sans-serif; background:#f5f5f5; color:#333; }")
        html.append("    .header { background-image:url('../static/foto_faro.jpg'); background-size:cover; background-position:center; min-height:500px; display:flex; align-items:center; justify-content:center; color:#fff; }")
        html.append("    .header img.logo { height:100px; width:100px; }")
        html.append("    .header h1 { margin:0; font-size:2.75rem; text-shadow:2px 2px 4px rgba(0,0,0,0.8); }")
        html.append("    .footer { text-align:center; padding:1rem; font-size:0.8rem; color:#999; line-height:1.2; }")
        html.append("    .footer .powered { margin-top:0.2rem; font-size:0.7rem; color:inherit; }")
        html.append("    .footer .date { margin-top:0.2rem; font-size:0.7rem; color:inherit; }")
        html.append("  </style>")
        html.append("</head>")
        html.append("<body>")
        # Header
        html.append("  <div class='header'><img src='../static/noticias_del_fuego.png' class='logo'><h1>Noticias del Fuego</h1></div>")
        # Index nav
        html.append("  <div class='container my-4'>")
        html.append("    <nav class='toc d-flex flex-wrap gap-2 mb-4'><h2 class='me-3 text-primary'>Índice de Autores</h2>")
        for autor in by_author:
            anchor = autor.lower().replace(' ', '-')
            html.append(f"      <a href='#autor-{anchor}' class='btn btn-outline-primary btn-sm'>{autor}</a>")
        html.append("    </nav>")
        # Sections
        for autor, arts in by_author.items():
            anchor = autor.lower().replace(' ', '-')
            html.append(f"    <section id='autor-{anchor}' class='mb-5'>")
            html.append(f"      <h3 class='text-primary'>{autor}</h3>")
            html.append("      <div class='row'>")
            for art in arts:
                html.append(f"        <a href='{art.slug()}.html' class='col-md-4 mb-4 text-decoration-none'>")
                html.append("          <div class='card h-100'><div class='card-body d-flex flex-column'>")
                html.append(f"            <h5 class='card-title text-primary'>{art.titulo}</h5>")
                html.append(f"            <p class='card-text flex-grow-1'>{art.snippet()}</p>")
                html.append("          </div></div>")
                html.append("        </a>")
            html.append("      </div>")
            html.append("    </section>")
        # Footer
        html.append(self._build_footer())
        html.append("  <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'></script>")
        html.append("</body>")
        html.append("</html>")
        return "\n".join(html)

    def _build_article(self, art):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html lang='es'>")
        html.append("<head>")
        html.append("  <meta charset='UTF-8'>")
        html.append("  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>")
        html.append(f"  <title>{art.titulo}</title>")
        html.append("  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>")
        html.append("  <style>")
        html.append("    body { margin:0; padding:0; font-family:'Segoe UI', Tahoma, sans-serif; background:#f5f5f5; color:#333; }")
        html.append("    .header { background-image:url('../static/foto_faro.jpg'); background-size:cover; background-position:center; min-height:500px; display:flex; align-items:center; justify-content:center; color:#fff; }")
        html.append("    .header img.logo { height:100px; width:100px; }")
        html.append("    .header h1 { margin:0; font-size:2.75rem; text-shadow:2px 2px 4px rgba(0,0,0,0.8); }")
        html.append("    .footer { text-align:center; padding:1rem; font-size:0.8rem; color:#999; line-height:1.2; }")
        html.append("    .footer .powered { margin-top:0.2rem; font-size:0.7rem; color:inherit; }")
        html.append("    .footer .date { margin-top:0.2rem; font-size:0.7rem; color:inherit; }")
        html.append("  </style>")
        html.append("</head>")
        html.append("<body>")
        html.append("  <div class='header'><img src='../static/noticias_del_fuego.png' class='logo'><h1>Noticias del Fuego</h1></div>")
        html.append("  <nav class='navbar bg-light shadow-sm'><div class='container'><a class='navbar-brand' href='index.html'>&larr; Volver al índice</a></div></nav>" )
        html.append("  <div class='container my-5 bg-white p-4 shadow-sm'>")
        html.append(f"    <h2 class='text-primary'>{art.titulo}</h2>")
        html.append(f"    <p class='fst-italic text-muted'>Por {art.autor}</p>")
        html.append(f"    <p>{art.texto}</p>")
        html.append("  </div>")
        html.append(self._build_footer())
        html.append("  <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'></script>")
        html.append("</body>")
        html.append("</html>")
        return "\n".join(html)

    def _build_footer(self) -> str:
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return (
            "  <div class='footer'>\n"
            f"    <div>&copy; 2025 - Laboratorio de Programación y Lenguajes</div>\n"
            "    <div class='powered'>Powered by ViktorDev</div>\n"
            f"    <div class='date'>Generado el: {timestamp}</div>\n"
            "  </div>"
        )
