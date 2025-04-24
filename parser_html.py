import os
from datetime import datetime
from collections import OrderedDict
from articulo import Articulo, InvalidArticleError

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
            titulo = art.titulo.strip()
            autor  = art.autor.strip()
            texto  = art.texto.strip()
            # Validar no vacíos
            if not (titulo and autor and texto):
                continue
            # Validar longitud mínima
            try:
                if len(titulo) < 10:
                    raise InvalidArticleError(f"El título debe tener al menos 10 caracteres ('{titulo}')")
                if len(texto) < 10:
                    raise InvalidArticleError(f"El texto debe tener al menos 10 caracteres ('{texto}')")
            except InvalidArticleError as e:
                # Registrar error y continuar
                self.errors.append(str(e))
                continue
            # Normalizar autor
            partes = autor.split()
            autor_norm = " ".join(p.capitalize() for p in partes)
            # Crear objeto Articulo ya limpio
            resultado.append(Articulo(titulo, autor_norm, texto))
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
        # Head and styles
        html.extend([
            "<!DOCTYPE html>",
            "<html lang='es'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            "  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>",
            "  <title>Noticias del Fuego</title>",
            "  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>",
            "  <style>",
            "    body { margin:0; padding:0; font-family:'Segoe UI', Tahoma, sans-serif; background:#f5f5f5; color:#333; }",
            "    .header { background-image:url('../static/foto_faro.jpg'); background-size:cover; background-position:center; min-height:500px; display:flex; align-items:center; justify-content:center; color:#fff; }",
            "    .header img.logo { height:100px; width:100px; }",
            "    .header h1 { margin:0; font-size:2.75rem; text-shadow:2px 2px 4px rgba(0,0,0,0.8); }",
            "    .footer { text-align:center; padding:1rem; font-size:0.8rem; color:#999; line-height:1.2; }",
            "    .footer .powered { margin-top:0.2rem; font-size:0.7rem; color:inherit; }",
            "    .footer .date { margin-top:0.2rem; font-size:0.7rem; color:inherit; }",
            "  </style>",
            "</head>",
            "<body>"
        ])
        # Header
        html.append("  <div class='header'><img src='../static/noticias_del_fuego.png' class='logo'><h1>Noticias del Fuego</h1></div>")
        html.append("  <div class='container my-4'>")
        # Summary table card
        html.extend([
            "    <div class='card shadow-sm mb-5'>",
            "      <div class='card-body'>",
            "        <h2 class='card-title'>Resumen de artículos por autor</h2>",
            "        <table class='table table-bordered table-hover'>",
            "          <thead class='table-light'><tr><th>Autor</th><th class='text-center'>Cantidad</th></tr></thead>",
            "          <tbody>"
        ])
        for autor, arts in by_author.items():
            html.append(f"            <tr><td>{autor}</td><td class='text-center'>{len(arts)}</td></tr>")
        html.extend([
            "          </tbody>",
            "        </table>",
            "      </div>",
            "    </div>"
        ])
        # Author index nav
        html.append("    <nav class='toc d-flex flex-wrap gap-2 mb-4'><h2 class='me-3 text-primary'>Índice de Autores</h2>")
        for autor in by_author:
            anchor = autor.lower().replace(' ', '-')
            html.append(f"      <a href='#autor-{anchor}' class='btn btn-outline-primary btn-sm'>{autor}</a>")
        html.append("    </nav>")
        # Sections
        for autor, arts in by_author.items():
            anchor = autor.lower().replace(' ', '-')
            html.extend([
                f"    <section id='autor-{anchor}' class='mb-5'>",
                f"      <h3 class='text-primary'>{autor}</h3>",
                "      <div class='row'>"
            ])
            for art in arts:
                html.extend([
                    f"        <a href='{art.slug()}.html' class='col-md-4 mb-4 text-decoration-none'>",
                    "          <div class='card h-100'><div class='card-body d-flex flex-column'>",
                    f"            <h5 class='card-title text-primary'>{art.titulo}</h5>",
                    f"            <p class='card-text flex-grow-1'>{art.snippet()}</p>",
                    "          </div></div>",
                    "        </a>"
                ])
            html.extend([
                "      </div>",
                "    </section>"
            ])
        # Footer
        html.append(self._build_footer())
        html.append("  <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'></script>")
        html.append("</body>")
        html.append("</html>")
        return "\n".join(html)

    def _build_article(self, art):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        html = []
        html.extend([
            "<!DOCTYPE html>",
            "<html lang='es'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            "  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>",
            f"  <title>{art.titulo}</title>",
            "  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>",
            "  <style>",
            "    body { margin:0; padding:0; font-family:'Segoe UI', Tahoma, sans-serif; background:#f5f5f5; color:#333; }",
            "    .header { background-image:url('../static/foto_faro.jpg'); background-size:cover; background-position:center; min-height:500px; display:flex; align-items:center; justify-content:center; color:#fff; }",
            "    .header img.logo { height:100px; width:100px; }",
            "    .header h1 { margin:0; font-size:2.75rem; text-shadow:2px 2px 4px rgba(0,0,0,0.8); }",
            "    .footer { text-align:center; padding:1rem; font-size:0.8rem; color:#999; line-height:1.2; }",
            "    .footer .powered { margin-top:0.2rem; font-size:0.7rem; color:inherit; }",
            "    .footer .date { margin-top:0.2rem; font-size:0.7rem; color:inherit; }",
            "  </style>",
            "</head>",
            "<body>",
            "  <div class='header'><img src='../static/noticias_del_fuego.png' class='logo'><h1>Noticias del Fuego</h1></div>",
            "  <nav class='navbar bg-light shadow-sm'><div class='container'><a class='navbar-brand' href='index.html'>&larr; Volver al índice</a></div></nav>",
            "  <div class='container my-5 bg-white p-4 shadow-sm'>",
            f"    <h2 class='text-primary'>{art.titulo}</h2>",
            f"    <p class='fst-italic text-muted'>Por {art.autor}</p>",
            f"    <p>{art.texto}</p>",
            "  </div>"
        ])
        # Footer at bottom outside content
        html.append(self._build_footer())
        html.append("  <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'></script>")
        html.append("</body>")
        html.append("</html>")
        return "\n".join(html)

    def _build_footer(self) -> str:
        year = datetime.now().year
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return (
            "  <footer class='footer mt-5'>\n"
            f"    <div>&copy; {year} - Laboratorio de Programación y Lenguajes</div>\n"
            "    <div class='powered'>Powered by ViktorDev</div>\n"
            f"    <div class='date'>Generado el: {timestamp}</div>\n"
            "  </footer>"
        )
