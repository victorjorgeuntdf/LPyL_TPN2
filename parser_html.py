import os
import string
from datetime import datetime
from articulo import Articulo, InvalidArticleError

# Plantilla unificada para todas las páginas
LAYOUT = """<!DOCTYPE html>
<html lang=\"es\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">
  <title>{title}</title>
  <!-- Favicon para todos los navegadores -->
  <link rel="icon" type="image/x-icon" href="../static/favicon.ico">
  <link rel="icon" type="image/png" href="../static/favicon.png">
  <link rel="apple-touch-icon" href="../static/apple-touch-icon.png">
  <link rel="manifest" href="../static/site.webmanifest">
  <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">
  <style>
    html, body {{
      height:100%; margin:0; padding:0;
      display:flex; flex-direction:column;
      font-family:'Segoe UI', Tahoma, sans-serif;
      background:#f5f5f5; color:#333;
    }}
    /* Header con imagen de fondo */
    .header {{
      background-image:url('../static/foto_faro.jpg');
      background-position:center;
      background-size:cover;
      background-repeat:no-repeat;
      min-height:500px;
      color:white;
      display:flex; align-items:center; justify-content:center; gap:1rem;
    }}
    .header img.logo {{ height:100px; width:100px; }}
    .header h1 {{ margin:0; font-size:2.75rem; text-shadow:2px 2px 4px rgba(0,0,0,0.8); }}

    /* Tarjetas */
    .card-article {{
      box-shadow:0 2px 6px rgba(0,0,0,0.1);
      transition:transform .3s;
    }}
    .card-article:hover {{ transform:scale(1.03); }}

    /* Pie de página al fondo */
    .footer {{
      text-align:center; padding:1rem;
      font-size:0.8rem; color:#999; margin-top:auto; background:#f5f5f5;
    }}
    .footer .powered {{ margin-top:0.15rem; font-size:0.7rem; }}
    .footer .date {{ margin-top:0.15rem; font-size:0.7rem; }}
  </style>
</head>
<body>
  <div class=\"header\"><img src=\"../static/noticias_del_fuego.png\" class=\"logo\" alt=\"Noticias del Fuego\"><h1>Noticias del Fuego</h1></div>
  {navbar}
  <main class=\"flex-fill\">
    <div class=\"container my-4\">
      {content}
    </div>
  </main>
  <footer class=\"footer\">
    <div>&copy; 2025 - Laboratorio de Programación y Lenguajes - UNTDF</div>
    <div class=\"powered\">Powered by ViktorDev</div>
    <div class=\"date\">Generado el: {timestamp}</div>
  </footer>
  <script>
    function filterByInitial(letter) {{
      const cards = document.querySelectorAll('.row > .col-md-4');
      let visible = 0;
      cards.forEach(col => {{
        const subtitle = col.querySelector('.fst-italic').textContent.trim();
        const surname = subtitle.split(' ').slice(-1)[0];
        const initialChar = surname[0].toUpperCase();
        if (!letter || initialChar === letter) {{
          col.style.display = '';
          visible++;
        }} else {{
          col.style.display = 'none';
        }}
      }});
      const noRes = document.getElementById('no-results');
      if (letter && visible === 0) noRes.style.display = '';
      else noRes.style.display = 'none';
    }}
  </script>
  <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js\"></script>
</body>
</html>"""

class ParserHtml:
    """
    Genera index.html, resumen.html y páginas individuales para artículos.
    Incluye filtro por inicial del apellido (última palabra del autor).
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

    def _get_adjacent_articles(self, current_article):
        """Devuelve el artículo anterior y siguiente en base a la lista ordenada."""
        index = None
        for i, art in enumerate(self.articulos):
            if art.slug() == current_article.slug():
                index = i
                break
        
        if index is None:
            return None, None
        
        prev_art = self.articulos[index - 1] if index > 0 else None
        next_art = self.articulos[index + 1] if index < len(self.articulos) - 1 else None
        
        return prev_art, next_art

    def filter_by_keyword(self, keyword: str):
        return [art for art in self.articulos if keyword.lower() in art.texto.lower()]

    def filter_by_initial(self, initial: str):
        return [art for art in self.articulos if art.autor.split()[-1][0].upper() == initial.upper()]

    def generate_html(self, keyword: str = None, initial: str = None):
        nav = ''
        if not keyword and initial is None:
            nav = "<nav class='navbar navbar-light bg-light shadow-sm'><div class='container'><a class='navbar-brand' href='resumen.html'>Resumen de artículos</a></div></nav>"

        # Botones A-Z para filtrar
        letter_filter = ['<div class=\"letter-filter mb-4\"><h2>Filtrar por inicial del apellido</h2><div class=\"btn-group\" role=\"group\">']
        for letter in string.ascii_uppercase:
            letter_filter.append(f"<button class='btn btn-outline-secondary' onclick=\"filterByInitial('{letter}')\">{letter}</button>")
        letter_filter.append("<button class='btn btn-outline-secondary' onclick=\"filterByInitial(null)\">Todos</button></div></div>")
        letter_html = '\n'.join(letter_filter)

        # Placeholder para "no resultados"
        no_results_html = "<div id='no-results' class='text-center fw-bold mt-5' style='display:none'>No existen artículos para esta inicial</div>"

        # Grid de tarjetas completo
        cards_html = self._build_cards(self.articulos)

        # Generar index
        index_content = letter_html + no_results_html + cards_html
        page = LAYOUT.format(
            title="Noticias del Fuego",
            navbar=nav,
            content=index_content,
            year=datetime.now().year,
            timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )
        with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(page)

        # Resumen
        summary_html = self._build_summary()
        summary_page = LAYOUT.format(
            title="Resumen de Artículos",
            navbar="<nav class='navbar navbar-light bg-light shadow-sm'><div class='container'><a class='navbar-brand' href='index.html'>Volver al Índice</a></div></nav>",
            content=summary_html,
            year=datetime.now().year,
            timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )
        with open(os.path.join(self.output_dir, 'resumen.html'), 'w', encoding='utf-8') as f:
            f.write(summary_page)

        # Artículos
        for art in self.articulos:
            prev_art, next_art = self._get_adjacent_articles(art)
            
            # Construir navegación
            nav_links = []
            if prev_art:
                nav_links.append(f"<a href='{prev_art.slug()}.html' class='btn btn-outline-primary'>&larr; Anterior: {prev_art.titulo[:30]}...</a>")
            if next_art:
                nav_links.append(f"<a href='{next_art.slug()}.html' class='btn btn-outline-primary'>Siguiente: {next_art.titulo[:30]}... &rarr;</a>")
            
            nav_html = ""
            if nav_links:
                nav_html = f"""
                <div class="article-navigation mt-4 d-flex justify-content-between">
                    {nav_links[0] if len(nav_links) > 1 else ''}
                    {nav_links[1] if len(nav_links) > 1 else nav_links[0]}
                </div>
                """
            
            art_content = f"""
            <h2 class='text-primary'>{art.titulo}</h2>
            <p class='fst-italic'>Por {art.autor}</p>
            <p>{art.texto}</p>
            {nav_html}
            """
            
            art_page = LAYOUT.format(
                title=art.titulo,
                navbar="<nav class='navbar bg-light shadow-sm'><div class='container'><a class='navbar-brand' href='index.html'>&larr; Volver al Índice</a></div></nav>",
                content=f"<div class='card shadow-sm'><div class='card-body'>{art_content}</div></div>",
                year=datetime.now().year,
                timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            )
            
            with open(os.path.join(self.output_dir, f"{art.slug()}.html"), 'w', encoding='utf-8') as f:
                f.write(art_page)

    def _build_cards(self, subset):
        if not subset:
            return "<div class='text-center'>No hay artículos para mostrar</div>"
        html = ['<div class=\"row\">']
        for art in subset:
            html.append(f"""
  <div class='col-md-4 mb-4'>
    <a href='{art.slug()}.html' class='text-decoration-none text-dark'>
      <div class='card h-100 card-article'>
        <div class='card-body d-flex flex-column'>
          <h5 class='card-title text-primary'>{art.titulo}</h5>
          <p class='fst-italic mb-2'>Por {art.autor}</p>
          <p class='card-text flex-grow-1'>{art.snippet()}</p>
        </div>
      </div>
    </a>
  </div>
""")
        html.append('</div>')
        return '\n'.join(html)

    def _build_summary(self):
        counts = {}
        for art in self.articulos:
            counts[art.autor] = counts.get(art.autor, 0) + 1
        if not counts:
            return "<div class='text-center'>No se encontraron artículos para mostrar</div>"
        html = [
            "<div class='card shadow-sm mb-5'>",
            "  <div class='card-body'>",
            "    <h2 class='card-title'>Resumen de artículos por autor</h2>",
            "    <table class='table table-bordered table-hover'>",
            "      <thead class='table-light'><tr><th>Autor</th><th class='text-center'>Cantidad</th></tr></thead>",
            "      <tbody>"
        ]
        for autor, c in counts.items():
            html.append(f"        <tr><td>{autor}</td><td class='text-center'>{c}</td></tr>")
        html.extend([
            "      </tbody>",
            "    </table>",
            "  </div>",
            "</div>"
        ])
        return '\n'.join(html)