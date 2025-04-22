import os

class ParserHtml:
    def __init__(self, articles, output_dir="output"):
        self.articles = articles
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_html(self, filename="index.html"):
        full_path = os.path.join(self.output_dir, filename)
        html = self._build_html()
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML generado en: {full_path}")

    def _build_html(self):
        head = f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Artículos Periodísticos</title>
  <link rel="stylesheet" href="../static/index.css">
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
        footer = """
  </div>
  <div class="footer">
    <div>&copy; 2025 - Laboratorio de Programación y Lenguajes</div>
    <div class="powered">Powered by ViktorDev</div>
  </div>


</body>
</html>
"""
        return head + cards + footer

if __name__ == "__main__":
    articulos = [
        (
            "Huawei aprovecha el freno de Trump a Nvidia y prepara envíos de su chip para IA a clientes chinos",
            "Rosangel Salazar",
            "Huawei planea comenzar los envíos masivos de su avanzado chip de inteligencia artificial 910C a clientes chinos a partir del mes que viene, dijeron dos personas familiarizadas con el asunto. Añadieron que ya se han realizado algunos envíos."  # :contentReference[oaicite:0]{index=0}
        ),
        (
            "Ushuaia, la maravilla del fin del mundo que tiene el desafío de equilibrar el turismo con la naturaleza",
            "Lautaro Grinspan y Victor Moriyama",
            "Los visitantes cada vez son más y eso trae prosperidad a la ciudad, pero también representa una carga para la fauna, aumenta el costo de la vida y contribuye a la escasez de viviendas para los trabajadores."  # :contentReference[oaicite:1]{index=1}
        ),
        (
            "Argentina logra superávit primario de 745.339 mln pesos en marzo",
            "Reuters",
            "En marzo de 2025, el Sector Público Nacional de Argentina registró un superávit primario de 745.339 millones de pesos y un superávit financiero de 398.909 millones de pesos, según informó el ministro de Economía, Luis Caputo."  # :contentReference[oaicite:2]{index=2}
        ),
        (
            "Milei celebra la guerra de precios entre proveedores y supermercados: “Se van a meter los productos en el orto”",
            "Federico Rivas Molina",
            "En una extensa entrevista, el presidente argentino Javier Milei celebró la confrontación entre supermercados y proveedores por los aumentos de precios, utilizando un lenguaje provocador para destacar el rechazo de grandes cadenas a mercadería con subas de hasta el 12%."  # :contentReference[oaicite:3]{index=3}
        )
    ]

    parser = ParserHtml(articulos)
    parser.generate_html()
