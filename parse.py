import os
from datetime import datetime

class ParserHtml:
    def __init__(self, articles, output_dir="output"):
        """
        articles: lista de tuplas (titulo, autor, texto)
        output_dir: carpeta donde se guardará el HTML generado
        """
        # Filtramos y normalizamos en la inicialización
        self.articles = self._filter_and_normalize(articles)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _filter_and_normalize(self, articles):
        """
        - Elimina artículos con título, autor o texto vacíos.
        - Quita espacios del autor y capitaliza nombre y apellido.
        """
        normalized = []
        for titulo, autor, texto in articles:
            if titulo.strip() and autor.strip() and texto.strip():
                autor_norm = " ".join(part.capitalize() for part in autor.strip().split())
                normalized.append((titulo.strip(), autor_norm, texto.strip()))
        return normalized

    def generate_html(self, filename="index.html"):
        full_path = os.path.join(self.output_dir, filename)
        html = self._build_html()
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML generado en: {full_path}")

    def _build_html(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        head = f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Noticias del Fuego</title>
  <style>
    /* Reset y tipografía básica */
    body {{
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', Tahoma, sans-serif;
      background-color: #f5f5f5;
      color: #333;
    }}

    /* Header */
    .header {{
      background: #1e88e5;
      color: white;
      padding: 1rem;
      text-align: center;
    }}

    /* Contenedor de artículos */
    .articles {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
      padding: 2rem;
    }}

    /* Tarjeta de artículo */
    .article-card {{
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
    }}
    .article-card h2 {{
      margin: 0 0 0.5rem;
      font-size: 1.5rem;
      color: #1e88e5;
    }}
    .article-card .meta {{
      font-size: 0.9rem;
      margin-bottom: 1rem;
      color: #666;
    }}
    .article-card p {{
      flex-grow: 1;
      line-height: 1.5;
    }}

    /* Footer */
    .footer {{
      text-align: center;
      padding: 1rem;
      font-size: 0.8rem;
      color: #999;
      line-height: 1.2;
    }}
    .footer .powered {{
      margin-top: 0.2rem;
      font-size: 0.7rem;
      color: inherit;
      font-style: normal;
    }}
    .footer .date {{
      margin-top: 0.3rem;
      font-size: 0.7rem;
      color: inherit;
    }}

    /* Responsive */
    @media (max-width: 768px) {{
      .articles {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}
    @media (max-width: 480px) {{
      .articles {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <div class="header">
    <h1>Noticias del Fuego</h1>
  </div>
  <div class="articles">
"""
        cards = ""
        for titulo, autor, texto in self.articles:
            cards += f"""
    <div class="article-card">
      <h2>{titulo}</h2>
      <div class="meta">Por {autor}</div>
      <p>{texto}</p>
    </div>
"""
        footer = f"""
  </div>
  <div class="footer">
    <div>&copy; 2025 - Laboratorio de Programación y Lenguajes</div>
    <div class="powered">Powered by ViktorDev</div>
    <div class="date">Generado el: {now}</div>
  </div>
</body>
</html>
"""
        return head + cards + footer


if __name__ == "__main__":
    # Ejemplos reales (punto 1)
    ejemplos_reales = [
        (
            "Huawei aprovecha el freno de Trump a Nvidia y prepara envíos de su chip para IA a clientes chinos",
            "Rosangel Salazar",
            "Huawei planea comenzar los envíos masivos de su avanzado chip de inteligencia artificial 910C a clientes chinos a partir del mes que viene, dijeron dos personas familiarizadas con el asunto. Añadieron que ya se han realizado algunos envíos."
        ),
        (
            "Ushuaia, la maravilla del fin del mundo que tiene el desafío de equilibrar el turismo con la naturaleza",
            "Lautaro Grinspan y Victor Moriyama",
            "Los visitantes cada vez son más y eso trae prosperidad a la ciudad, pero también representa una carga para la fauna, aumenta el costo de la vida y contribuye a la escasez de viviendas para los trabajadores."
        ),
        (
            "Argentina logra superávit primario de 745.339 mln pesos en marzo",
            "Reuters",
            "En marzo de 2025, el Sector Público Nacional de Argentina registró un superávit primario de 745.339 millones de pesos y un superávit financiero de 398.909 millones de pesos, según informó el ministro de Economía, Luis Caputo."
        ),
        (
            "Milei celebra la guerra de precios entre proveedores y supermercados: “Se van a meter los productos en el orto”",
            "Federico Rivas Molina",
            "En una extensa entrevista, el presidente argentino Javier Milei celebró la confrontación entre supermercados y proveedores por los aumentos de precios, utilizando un lenguaje provocador para destacar el rechazo de grandes cadenas a mercadería con subas de hasta el 12%."
        ),
    ]

    # Ejemplos de normalización y filtrado (punto 2), con 14 casos:
    ejemplos_norm = [
        # Originales
        ("   La luna sobre Ushuaia   ", "  maría pérez  ",
         "Hoy, el cielo se vistió de un manto plateado…"),
        ("", "Juan Gómez",
         "Contenido irrelevante"),
        ("Tecnología y sociedad", " juan gómez  ",
         "El avance de la inteligencia artificial plantea…"),
        ("Economía global 2025", "ana lópez",
         ""),

        ("Turismo invernal en Ushuaia bate récords de reservas", "  carlos ramirez ",
         "Las cabañas en Cerro Castor alcanzaron un 95% de ocupación este año…"),
        ("Desarrollo portuario en Río Grande", "María  López",
         ""),
        ("", "Pedro Fernández",
         "Se inauguró un nuevo centro cultural en Tolhuin…"),
        ("Impacto del cambio climático en el Canal Beagle", "ana perez",
         "Investigadores del CONICET advierten sobre el retroceso glaciar…"),
        ("Nueva ruta aérea Ushuaia-Córdoba anuncia Aerolíneas Argentinas", "  aerolíneas argentinas team ",
         "El servicio comenzará en junio con dos frecuencias semanales…"),
        ("    ", "Laura Gómez",
         "Evento de música fueguina congrega a artistas locales…"),
        ("Programan festival de cine ubicuo en Ushuaia", " juan martín  gómez",
         "La edición 2025 del festival se llevará a cabo del 10 al 15 de mayo…"),
        ("Pesca artesanal de centolla sufre regulaciones", "María    Fernández",
         "El gobierno provincial estableció nuevas cuotas de captura…"),
        ("Reapertura del parque nacional Tierra del Fuego", "",
         "El lunes se reabrió el parque con nuevos senderos señalizados…"),
        ("Salud pública en TDF: brote de gripe aviar controlado", " Dr. luis sanchez ",
         "Las autoridades sanitarias informaron que no se registraron muertes…")
    ]

    # Combinamos ambos conjuntos
    articulos = ejemplos_reales + ejemplos_norm

    parser = ParserHtml(articulos)
    parser.generate_html()
