# Este es el archivo anterior que tiene todo el proyecto antes de haberlo separado en varios archivos
import os
import re
from datetime import datetime
from collections import OrderedDict

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

class ParserHtml:
    def __init__(self, articulos, output_dir="output"):
        self.articulos = self._filter_and_normalize(articulos)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _filter_and_normalize(self, articulos):
        resultado = []
        for art in articulos:
            if art.titulo.strip() and art.autor.strip() and art.texto.strip():
                autor_norm = " ".join(p.capitalize() for p in art.autor.strip().split())
                resultado.append(Articulo(art.titulo.strip(), autor_norm, art.texto.strip()))
        return resultado

    def filter_by_keyword(self, keyword: str):
        return [art for art in self.articulos if keyword.lower() in art.texto.lower()]

    def _slug(self, text: str) -> str:
        s = text.lower()
        s = re.sub(r"[^a-z0-9]+", "-", s)
        return s.strip('-')

    def generate_html(self, keyword: str = None):
        subset = self.filter_by_keyword(keyword) if keyword else self.articulos
        # Índice
        idx_path = os.path.join(self.output_dir, 'index.html')
        with open(idx_path, 'w', encoding='utf-8') as f:
            f.write(self._build_index(subset))
        print(f"Índice generado: {idx_path}")
        # Artículos
        for art in subset:
            name = f"{self._slug(art.titulo)}.html"
            path = os.path.join(self.output_dir, name)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self._build_article(art))
            print(f"Página artículo: {path}")

    def _build_index(self, subset):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        by_author = OrderedDict()
        for art in subset:
            by_author.setdefault(art.autor, []).append(art)
        html = f"""
<!DOCTYPE html>
<html lang=\"es\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">
  <title>Noticias del Fuego</title>
  <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">
  <style>
    body {{ margin:0; padding:0; font-family:'Segoe UI', Tahoma, sans-serif; background:#f5f5f5; color:#333; }}
    .header {{ background-image:url('../static/foto_faro.jpg'); background-size:cover; background-position:center; min-height:500px; display:flex; align-items:center; justify-content:center; color:#fff; }}
    .header img.logo {{ height:100px; width:100px; }}
    .header h1 {{ margin:0; font-size:2.75rem; text-shadow:2px 2px 4px rgba(0,0,0,0.8); }}
    .footer {{ text-align:center; padding:1rem; font-size:.8rem; color:#999; }}
  </style>
</head>
<body>
  <div class=\"header\"> <img src=\"../static/noticias_del_fuego.png\" class=\"logo\"> <h1>Noticias del Fuego</h1> </div>
  <div class=\"container my-4\">
    <nav class=\"toc d-flex flex-wrap gap-2 mb-4\">
      <h2 class=\"me-3 text-primary\">Índice de Autores</h2>
"""
        for autor in by_author:
            anchor = autor.lower().replace(' ', '-')
            html += f"      <a href=\"#autor-{anchor}\" class=\"btn btn-outline-primary btn-sm\">{autor}</a>\n"
        html += "    </nav>\n"
        # Secciones
        for autor, arts in by_author.items():
            anchor = autor.lower().replace(' ', '-')
            html += f"    <section id=\"autor-{anchor}\" class=\"mb-5\"> <h3 class=\"text-primary\">{autor}</h3> <div class=\"row\">\n"
            for art in arts:
                slug = f"{self._slug(art.titulo)}.html"
                snippet = art.snippet()
                html += f"      <a href=\"{slug}\" class=\"col-md-4 mb-4 text-decoration-none\">"
                html += f"<div class=\"card h-100\"><div class=\"card-body d-flex flex-column\">"
                html += f"<h5 class=\"card-title text-primary\">{art.titulo}</h5>"
                html += f"<p class=\"card-text flex-grow-1\">{snippet}</p></div></div></a>\n"
            html += "    </div> </section>\n"
        # Footer
        html += f"  </div> <div class=\"footer\">&copy; 2025 - Laboratorio de Programación y Lenguajes<br>Powered by ViktorDev<br>Generado: {now}</div>"
        html += "<script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js\"></script></body></html>"
        return html

    def _build_article(self, art):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        html = f"""
<!DOCTYPE html>
<html lang=\"es\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">
  <title>{art.titulo}</title>
  <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">
  <style>
    body {{ margin:0; padding:0; font-family:'Segoe UI', Tahoma, sans-serif; background:#f5f5f5; color:#333; }}
    .header {{ background-image:url('../static/foto_faro.jpg'); background-size:cover; background-position:center; min-height:500px; display:flex; align-items:center; justify-content:center; color:#fff; }}
    .header img.logo {{ height:100px; width:100px; }}
    .header h1 {{ margin:0; font-size:2.75rem; text-shadow:2px 2px 4px rgba(0,0,0,0.8); }}
    .footer {{ text-align:center; padding:1rem; font-size:.8rem; color:#999; }}
  </style>
</head>
<body>
  <div class=\"header\"> <img src=\"../static/noticias_del_fuego.png\" class=\"logo\"> <h1>Noticias del Fuego</h1> </div>
  <nav class=\"navbar bg-light shadow-sm\"><div class=\"container\"><a class=\"navbar-brand\" href=\"index.html\">&larr; Volver al índice</a></div></nav>
  <div class=\"container my-5 bg-white p-4 shadow-sm\">
    <h2 class=\"text-primary\">{art.titulo}</h2>
    <p class=\"fst-italic text-muted\">Por {art.autor}</p>
    <p>{art.texto}</p>
  </div>
  <div class=\"footer\">&copy; 2025 - Laboratorio de Programación y Lenguajes<br>Powered by ViktorDev<br>Generado: {now}</div>
  <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js\"></script>
</body>
</html>
"""
        return html

if __name__ == "__main__":
    # [Ejemplos de artículos]
    ejemplos_reales = [
        (
            "Huawei planea iniciar en mayo el envío de su chip de IA 910C a clientes chinos",
            "Rosangel Salazar",
            "Huawei planea iniciar en mayo el envío de su nuevo chip de inteligencia artificial 910C a empresas chinas especializadas en procesamiento de datos. Según fuentes cercanas al proyecto, el fabricante completó las pruebas internas y logró un rendimiento comparable a soluciones occidentales, garantizando compatibilidad con arquitecturas existentes y optimizando el consumo energético."
        ),
        (
            "Temporada invernal en Ushuaia bate récords de reservas",
            "Lautaro Grinspan",
            "En Ushuaia, la temporada de turismo invernal registró un aumento histórico de reservas en cabañas y hoteles, alcanzando un 92% de ocupación durante julio. Las autoridades políticas destacan el impacto económico positivo, mientras organizaciones ambientales advierten sobre la presión sobre la flora y fauna local. Para mitigar efectos, se proponen nuevas rutas de senderismo menos concurridas."
        ),
        (
            "El Gobierno nacional anunció superávit primario de 745.339 mln pesos",
            "Reuters",
            "El Gobierno nacional anunció un superávit primario de 745.339 millones de pesos en marzo de 2025, atribuido a la contención del gasto público y al crecimiento de la recaudación tributaria. El ministro de Economía subrayó el compromiso con la disciplina fiscal y anticipó próximas reformas orientadas a promover la inversión privada y revitalizar sectores productivos."
        ),
        (
            "El presidente Javier Milei defiende la liberalización de precios",
            "Federico Rivas Molina",
            "El presidente Javier Milei defendió en una conferencia su política de liberalización de precios y criticó la postura de supermercados y proveedores por supuestos acuerdos para subir los costos. En su intervención, Milei aseguró que las medidas beneficiarán al consumidor y advirtió que impulsará una ley para sancionar a empresas que mantengan prácticas de fijación de precios abusivas."
        )
    ]

    # [Ejemplos de filtrado]
    ejemplos_norm = [
        # María Pérez
        ("Incremento de cruceros en Ushuaia amenaza ecosistema costero", "  maría pérez  ",
         "El aumento de cruceros en Ushuaia durante la temporada alta ha generado preocupación entre biólogos marinos y funcionarios locales. Las emisiones de los grandes barcos y el tránsito constante cerca de la costa podrían alterar la fauna autóctona. Expertos sugieren establecer zonas de exclusión y mejorar los protocolos de limpieza para proteger los hábitats marinos."),
        ("Proyección del crecimiento inmobiliario en Río Grande", "  maría pérez  ",
         "El boom inmobiliario en Río Grande se ha visto impulsado por la demanda de viviendas estudiantiles y de trabajadores temporarios. El aumento de torres de departamentos deriva en debates sobre planificación urbana y disponibilidad de servicios. Autoridades trabajan en un plan regulatorio que priorice el desarrollo sustentable y espacios verdes. Incluye planos para nuevos espacios recreativos y reservas verdes que garanticen calidad de vida a largo plazo."),
        ("Debate sobre el costo de vida en la provincia", "  maría pérez  ",
         "La discusión sobre el costo de vida en Tierra del Fuego se intensificó tras el informe de inflación local, que supera el promedio nacional. Ciudadanos exigen revisar subsidios al transporte y analizar políticas de ingresos para trabajadores estatales. Economistas recomiendan una serie de medidas fiscales para amortiguar el impacto en sectores vulnerables."),
        ("Innovaciones locales en energías renovables en TDF", "  maría pérez  ",
         "Pequeñas empresas fueguinas comienzan a implementar paneles solares y aerogeneradores adaptados al clima extremo de la región. Estas iniciativas reducen costos de electricidad y aumentan la independencia energética de comunidades aisladas. El Gobierno provincial ofrece líneas de crédito y asesoría técnica para expandir estos proyectos y mejorar la matriz energética."),
        # Carlos Ramírez
        ("Festival de la centolla atrae a turistas de todo el país", "carlos ramirez",
         "El tradicional Festival de la Centolla en Río Grande registró un récord de asistencia, con visitantes de más de diez provincias argentinas. El evento celebra la pesca artesanal y ofrece conciertos, ferias de gastronomía y talleres de cocina. Organizadores estiman que el impacto económico superó los cinco millones de pesos en ventas directas durante el fin de semana."),
        ("Nuevos senderos eco-turísticos inaugurados en Tolhuin", "carlos ramirez",
         "Autoridades municipales y organizaciones ambientales inauguraron nuevos senderos en el bosque de Tolhuin, diseñados para minimizar el impacto humano. Con señalización didáctica y miradores estratégicos, buscan educar sobre la biodiversidad local. Se espera que estas rutas fortalezcan el turismo sostenible y generen nuevas oportunidades para guías locales."),
        ("Plan de renovación urbana en Ushuaia recibe fondos nacionales", "carlos ramirez",
         "El Gobierno nacional autorizó financiamiento para la renovación de espacios públicos en Ushuaia, incluyendo remodelación de plazas y mejora de veredas. El proyecto prevé modernizar el mobiliario urbano y optimizar la accesibilidad. Funcionarios destacaron que las obras generarán empleo local y elevarán la calidad de vida de residentes y visitantes. El financiamiento incluirá mejoras en conexiones de transporte urbano y caminos rurales para facilitar el acceso a nuevos desarrollos."),
        ("Inversión privada impulsa proyectos tecnológicos en TDF", "carlos ramirez",
         "Empresas de base tecnológica de Tierra del Fuego recibieron inversiones de capital de riesgo para proyectos de software y robótica. Estos fondos permitirán desarrollar prototipos y escalar aplicaciones vinculadas a logística portuaria y monitoreo ambiental. Emprendedores locales confían en que esto generará un ecosistema innovador en la provincia. Además, se planea abrir un centro de innovación conjunta con la Universidad Nacional de Tierra del Fuego."),
        # Ana López
        ("Aumento de tarifas del transporte en la ruta 3 genera protestas", " ana lópez ",
         "El reciente incremento de tarifas en el transporte interurbano de la ruta 3 movilizó a sindicatos y usuarios en Ushuaia y Río Grande. Se organizaron manifestaciones y cortes parciales de ruta para reclamar una revisión de los costos y analizar la situación de familias de bajos ingresos. Autoridades provinciales anunciaron mesas de diálogo para resolver el conflicto."),
        ("Descubrimiento arqueológico sacude a la comunidad yagana", " ana lópez ",
         "Investigadores hallaron en la costa del Canal Beagle restos de herramientas de piedra atribuidas a la cultura yagana con más de mil años de antigüedad. El hallazgo se produjo durante una prospección arqueológica y plantea nuevas hipótesis sobre asentamientos tempranos. El Museo del Fin del Mundo prepara una exhibición para presentar las piezas al público."),
        # Invalidos
        ("Programa educativo digital llega a escuelas rurales", "                   ",
         "El Ministerio de Educación lanzó una plataforma digital con contenidos interactivos para estudiantes de zonas rurales de Tierra del Fuego. Incluye clases en video, ejercicios evaluables y seguimiento docente. El programa busca reducir la brecha educativa y fomentar habilidades digitales. Se proyecta expandir el alcance a más de cincuenta instituciones durante el próximo semestre."),
        ("", " ana lópez ",
         "Datos del sector energético indican una disminución del 12% en las exportaciones de crudo desde la refinería de Río Grande en abril. La baja se atribuye a la menor demanda internacional y ajustes en la producción por mantenimiento de equipos. Empresas evalúan estrategias comerciales para diversificar destinos y mejorar la competitividad. Asimismo, se analizan oportunidades en mercados asiáticos para recuperar volumen de envíos durante la próxima temporada."),
        ("", "María Pérez", "Título faltante para validar filtro."),
        ("Titular de prueba", "", "Autor faltante para validar filtro."),
        ("Titular de prueba", "Autor de prueba", ""),
    ]
    
    ejemplos = ejemplos_reales + ejemplos_norm
    parser = ParserHtml([Articulo(t,a,tx) for t,a,tx in ejemplos])
    parser.generate_html()
