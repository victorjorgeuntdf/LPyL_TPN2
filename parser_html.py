import os
import string
from datetime import datetime
from articulo import Articulo, InvalidArticleError

class ParserHtml:
    """
    Genera index.html, resumen.html y páginas individuales para artículos.
    Incluye filtro de autores por inicial del apellido.
    """
    def __init__(self, articulos, output_dir="output"):
        self.errors = []
        self.articulos = self._filter_and_normalize(articulos)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _filter_and_normalize(self, articulos):
        resultado = []
        for art in articulos:
            titulo = art.titulo.strip()
            autor  = art.autor.strip()
            texto  = art.texto.strip()
            if not (titulo and autor and texto):
                continue
            try:
                if len(titulo) < 10:
                    raise InvalidArticleError(f"El título debe tener al menos 10 caracteres ('{titulo}')")
                if len(texto) < 10:
                    raise InvalidArticleError(f"El texto debe tener al menos 10 caracteres ('{texto}')")
            except InvalidArticleError as e:
                self.errors.append(str(e))
                continue
            autor_norm = ' '.join(p.capitalize() for p in autor.split())
            resultado.append(Articulo(titulo, autor_norm, texto))
        return resultado

    def filter_by_keyword(self, keyword: str):
        return [art for art in self.articulos if keyword.lower() in art.texto.lower()]

    def filter_by_initial(self, initial: str):
        return [art for art in self.articulos if art.autor.split()[-1][0].upper() == initial.upper()]

    def generate_html(self, keyword: str = None, initial: str = None):
        if keyword:
            subset = self.filter_by_keyword(keyword)
        elif initial:
            subset = self.filter_by_initial(initial)
        else:
            subset = self.articulos
        self._generate_index(subset)
        self._generate_summary()
        self._generate_article_pages(self.articulos)

    def _generate_index(self, subset):
        content = self._build_index(subset)
        path = os.path.join(self.output_dir, 'index.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Índice generado: {path}")

    def _generate_summary(self):
        content = self._build_summary()
        path = os.path.join(self.output_dir, 'resumen.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Resumen generado: {path}")

    def _generate_article_pages(self, subset):
        for art in subset:
            fname = f"{art.slug()}.html"
            path = os.path.join(self.output_dir, fname)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self._build_article(art))
            print(f"Página generada: {path}")

    def _build_index(self, subset):
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        html = [
            "<!DOCTYPE html>",
            "<html lang='es'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            "  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>",
            "  <title>Noticias del Fuego</title>",
            "  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>",
            "  <style>",
            "    /* Reset y tipografía básica */",
            "    html, body { height:100%; margin:0; padding:0; display:flex; flex-direction:column; font-family:'Segoe UI', Tahoma, sans-serif; background:#f5f5f5; color:#333; }",
            "    /* Header con imagen de fondo adaptada */",
            "    .header { background-image:url('../static/foto_faro.jpg'); background-position:center; background-size:cover; background-repeat:no-repeat; min-height:500px; color:white; display:flex; align-items:center; justify-content:center; gap:1rem; }",
            "    .header img.logo { height:100px; width:100px; }",
            "    .header h1 { margin:0; font-size:2.75rem; text-shadow:2px 2px 4px rgba(0,0,0,0.8); }",
            "    .card-article { box-shadow:0 2px 6px rgba(0,0,0,0.1); transition:transform .3s; }",
            "    .card-article:hover { transform:scale(1.03); }",
            "    .footer { text-align:center; padding:1rem; font-size:0.8rem; color:#999; line-height:1.2; }",
            "    .footer .powered { margin-top:0.2rem; font-size:0.7rem; }",
            "    .footer .date { margin-top:0.2rem; font-size:0.7rem; }",
            "  </style>",
            "</head>",
            "<body>",
            "  <div class='header'><img src='../static/noticias_del_fuego.png' class='logo' alt='Noticias del Fuego'><h1>Noticias del Fuego</h1></div>",
            "  <nav class='navbar navbar-light bg-light shadow-sm'><div class='container'><a class='navbar-brand' href='resumen.html'>Resumen de artículos</a></div></nav>",
            "  <div class='flex-fill container my-4'>",
            "    <div class='letter-filter mb-4'><h2>Filtrar por inicial del apellido</h2><div class='btn-group' role='group'>"
        ]
        for letter in string.ascii_uppercase:
            html.append(f"      <button class='btn btn-outline-secondary' onclick=\"filterByInitial('{letter}')\">{letter}</button>")
        html.append("      <button class='btn btn-outline-secondary' onclick=\"filterByInitial(null)\">Todos</button>")
        html.extend([
            "    </div></div>",
            "    <div class='row'>"
        ])
        for art in subset:
            html.extend([
                "      <div class='col-md-4 mb-4'>",
                f"        <a href='{art.slug()}.html' class='text-decoration-none text-dark'>",
                "          <div class='card h-100 card-article'>",
                "            <div class='card-body d-flex flex-column'>",
                f"              <h5 class='card-title text-primary'>{art.titulo}</h5>",
                f"              <p class='fst-italic mb-2'>Por {art.autor}</p>",
                f"              <p class='card-text flex-grow-1'>{art.snippet()}</p>",
                "            </div></div>",
                "        </a>",
                "      </div>"
            ])
        html.extend([
            "    </div>",
            "  </div>",
            self._build_footer(),
            "  <script>",
            "    function filterByInitial(letter) {",
            "      document.querySelectorAll('.row > .col-md-4').forEach(col => {",
            "        const autor = col.querySelector('.fst-italic').textContent.split(' ')[1][0].toUpperCase();",
            "        col.style.display = (!letter || autor === letter) ? '' : 'none';",
            "      });",
            "    }",
            "  </script>",
            "  <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'></script>",
            "</body>",
            "</html>"
        ])
        return "\n".join(html)

    def _build_summary(self):
        """
        Genera la página resumen de artículos por autor.
        Si no hay artículos, muestra mensaje centrado.
        """
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Conteo por autor
        counts = {}
        for art in self.articulos:
            counts[art.autor] = counts.get(art.autor, 0) + 1

        html = [
            "<!DOCTYPE html>",
            "<html lang='es'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            "  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>",
            "  <title>Resumen de Artículos</title>",
            "  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>",
            "  <style>",
            "    html, body { height:100%; margin:0; padding:0; display:flex; flex-direction:column; font-family:'Segoe UI', Tahoma, sans-serif; background:#f5f5f5; }",
            "    body > .content { flex:1; padding:2rem; }",
            "    table { background:#fff; box-shadow:0 2px 6px rgba(0,0,0,0.1); }",
            "    .table-hover tbody tr:hover { background-color:#f1f1f1; }",
            "    .no-articles { text-align:center; font-size:1.25rem; color:#555; padding:2rem; }",
            "    .footer { text-align:center; padding:1rem; font-size:0.8rem; color:#999; margin-top:auto; background:#fff; }",
            "  </style>",
            "</head>",
            "<body>",
            "  <div class='header'><img src='../static/noticias_del_fuego.png' class='logo'><h1>Noticias del Fuego</h1></div>",
            "  <nav class='navbar navbar-light bg-light shadow-sm'><div class='container'><a class='navbar-brand' href='index.html'>&larr; Volver al Índice</a></div></nav>",
            "  <div class='content container'>"
        ]
        if not counts:
            html.append("    <div class='no-articles'>No se encontraron artículos para mostrar</div>")
        else:
            html.extend([
                "    <h2>Resumen de Artículos por Autor</h2>",
                "    <table class='table table-striped table-hover mt-3'>",
                "      <thead><tr><th>Autor</th><th class='text-center'>Cantidad</th></tr></thead>",
                "      <tbody>"
            ])
            for autor, c in counts.items():
                html.append(f"        <tr><td>{autor}</td><td class='text-center'>{c}</td></tr>")
            html.extend([
                "      </tbody>",
                "    </table>"
            ])
        html.extend([
            "  </div>",
            self._build_footer(),
            "  <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'></script>",
            "</body>",
            "</html>"
        ])
        return "".join(html)

    def _build_article(self, art):
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        html = [
            "<!DOCTYPE html>",
            "<html lang='es'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            "  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>",
            f"  <title>{art.titulo}</title>",
            "  <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>",
            "  <style>",
            "    html, body { height:100%; margin:0; padding:0; display:flex; flex-direction:column; font-family:'Segoe UI', Tahoma, sans-serif; background:#f5f5f5; }",
            "    .header { background-image:url('../static/foto_faro.jpg'); background-position:center; background-size:cover; background-repeat:no-repeat; min-height:500px; color:white; display:flex; align-items:center; justify-content:center; gap:1rem; }",
            "    .header img.logo { height:100px; width:100px; }",
            "    .header h1 { margin:0; font-size:2.75rem; text-shadow:2px 2px 4px rgba(0,0,0,0.8); }",
            "    .footer { text-align:center; padding:1rem; font-size:0.8rem; color:#999; margin-top:auto; }",
            "    .footer .powered { margin-top:0.2rem; font-size:0.7rem; }",
            "    .footer .date { margin-top:0.2rem; font-size:0.7rem; }",
            "  </style>",
            "</head>",
            "<body>",
            "  <div class='header'><img src='../static/noticias_del_fuego.png' class='logo' alt='Noticias del Fuego'><h1>Noticias del Fuego</h1></div>",
            "  <nav class='navbar bg-light shadow-sm'><div class='container'><a class='navbar-brand' href='index.html'>&larr; Volver al Índice</a></div></nav>",
            "  <div class='container my-5'>",
            "    <div class='card shadow-sm'>",
            "      <div class='card-body'>",
            f"        <h2 class='card-title text-primary'>{art.titulo}</h2>",
            f"        <p class='fst-italic'>{art.autor}</p>",
            f"        <p>{art.texto}</p>",
            "      </div>",
            "    </div>",
            self._build_footer(),
            "  <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'></script>",
            "</body>",
            "</html>"
        ]
        return "\n".join(html)

    def _build_footer(self) -> str:
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return (
            "  <footer class='footer'>\n"
            f"    <div>&copy; 2025 - Laboratorio de Programación y Lenguajes</div>\n"
            "    <div class='powered'>Powered by ViktorDev</div>\n"
            f"    <div class='date'>Generado el: {timestamp}</div>\n"
            "  </footer>"
        )
