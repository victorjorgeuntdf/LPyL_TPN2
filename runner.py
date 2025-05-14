from articulo import Articulo
from parser_html import ParserHtml

class HtmlApp:
    """Ejecuta ParserHtml con ejemplos concretos."""
    def __init__(self):
        # [Ejemplos de artículos]
        self.ejemplos_reales = [
        (
            "Huawei planea iniciar en mayo el envío de su chip de IA 910C a clientes chinos",
            " rosangel salazar   ",
            "Huawei planea iniciar en mayo el envío de su nuevo chip de inteligencia artificial 910C a empresas chinas especializadas en procesamiento de datos. Según fuentes cercanas al proyecto, el fabricante completó las pruebas internas y logró un rendimiento comparable a soluciones occidentales, garantizando compatibilidad con arquitecturas existentes y optimizando el consumo energético."
        ),
        (
            "Temporada invernal en Ushuaia bate récords de reservas",
            "Lautaro Grinspan  ",
            "En Ushuaia, la temporada de turismo invernal registró un aumento histórico de reservas en cabañas y hoteles, alcanzando un 92% de ocupación durante julio. Las autoridades políticas destacan el impacto económico positivo, mientras organizaciones ambientales advierten sobre la presión sobre la flora y fauna local. Para mitigar efectos, se proponen nuevas rutas de senderismo menos concurridas."
        ),
        (
            "El Gobierno nacional anunció superávit primario de 745.339 mln pesos",
            "Reuters",
            "El Gobierno nacional anunció un superávit primario de 745.339 millones de pesos en marzo de 2025, atribuido a la contención del gasto público y al crecimiento de la recaudación tributaria. El ministro de Economía subrayó el compromiso con la disciplina fiscal y anticipó próximas reformas orientadas a promover la inversión privada y revitalizar sectores productivos."
        ),
        (
            "El presidente Javier Milei defiende la liberalización de precios",
            " Molina Federico Rivas",
            "El presidente Javier Milei defendió en una conferencia su política de liberalización de precios y criticó la postura de supermercados y proveedores por supuestos acuerdos para subir los costos. En su intervención, Milei aseguró que las medidas beneficiarán al consumidor y advirtió que impulsará una ley para sancionar a empresas que mantengan prácticas de fijación de precios abusivas."
        )
        ]
        # [Ejemplos de filtrado]
        self.ejemplos_norm = [
        #  María Pérez 
        ("Incremento de cruceros en Ushuaia amenaza ecosistema costero", "  maría pérez    ",
         "El aumento de cruceros en Ushuaia durante la temporada alta ha generado preocupación entre biólogos marinos y funcionarios locales. Las emisiones de los grandes barcos y el tránsito constante cerca de la costa podrían alterar la fauna autóctona. Expertos sugieren establecer zonas de exclusión y mejorar los protocolos de limpieza para proteger los hábitats marinos."),
        ("Proyección del crecimiento inmobiliario en Río Grande", "  maría pérez    ",
         "El boom inmobiliario en Río Grande se ha visto impulsado por la demanda de viviendas estudiantiles y de trabajadores temporarios. El aumento de torres de departamentos deriva en debates sobre planificación urbana y disponibilidad de servicios. Autoridades trabajan en un plan regulatorio que priorice el desarrollo sustentable y espacios verdes. Incluye planos para nuevos espacios recreativos y reservas verdes que garanticen calidad de vida a largo plazo."),
        ("Debate sobre el costo de vida en la provincia", "  maría pérez    ",
         "La discusión sobre el costo de vida en Tierra del Fuego se intensificó tras el informe de inflación local, que supera el promedio nacional. Ciudadanos exigen revisar subsidios al transporte y analizar políticas de ingresos para trabajadores estatales. Economistas recomiendan una serie de medidas fiscales para amortiguar el impacto en sectores vulnerables."),
        ("Innovaciones locales en energías renovables en TDF", "  maría pérez    ",
         "Pequeñas empresas fueguinas comienzan a implementar paneles solares y aerogeneradores adaptados al clima extremo de la región. Estas iniciativas reducen costos de electricidad y aumentan la independencia energética de comunidades aisladas. El Gobierno provincial ofrece líneas de crédito y asesoría técnica para expandir estos proyectos y mejorar la matriz energética."),
        # Carlos Ramírez 
        ("Festival de la centolla atrae a turistas de todo el país", "carlos ramirez  ",
         "El tradicional Festival de la Centolla en Río Grande registró un récord de asistencia, con visitantes de más de diez provincias argentinas. El evento celebra la pesca artesanal y ofrece conciertos, ferias de gastronomía y talleres de cocina. Organizadores estiman que el impacto económico superó los cinco millones de pesos en ventas directas durante el fin de semana."),
        ("Nuevos senderos eco-turísticos inaugurados en Tolhuin", "carlos ramirez  ",
         "Autoridades municipales y organizaciones ambientales inauguraron nuevos senderos en el bosque de Tolhuin, diseñados para minimizar el impacto humano. Con señalización didáctica y miradores estratégicos, buscan educar sobre la biodiversidad local. Se espera que estas rutas fortalezcan el turismo sostenible y generen nuevas oportunidades para guías locales."),
        ("Plan de renovación urbana en Ushuaia recibe fondos nacionales", "carlos ramirez  ",
         "El Gobierno nacional autorizó financiamiento para la renovación de espacios públicos en Ushuaia, incluyendo remodelación de plazas y mejora de veredas. El proyecto prevé modernizar el mobiliario urbano y optimizar la accesibilidad. Funcionarios destacaron que las obras generarán empleo local y elevarán la calidad de vida de residentes y visitantes. El financiamiento incluirá mejoras en conexiones de transporte urbano y caminos rurales para facilitar el acceso a nuevos desarrollos."),
        ("Inversión privada impulsa proyectos tecnológicos en TDF", "carlos ramirez  ",
         "Empresas de base tecnológica de Tierra del Fuego recibieron inversiones de capital de riesgo para proyectos de software y robótica. Estos fondos permitirán desarrollar prototipos y escalar aplicaciones vinculadas a logística portuaria y monitoreo ambiental. Emprendedores locales confían en que esto generará un ecosistema innovador en la provincia. Además, se planea abrir un centro de innovación conjunta con la Universidad Nacional de Tierra del Fuego."),
        # Ana López
        ("Aumento de tarifas del transporte en la ruta 3 genera protestas", "ana lópez   ",
         "El reciente incremento de tarifas en el transporte interurbano de la ruta 3 movilizó a sindicatos y usuarios en Ushuaia y Río Grande. Se organizaron manifestaciones y cortes parciales de ruta para reclamar una revisión de los costos y analizar la situación de familias de bajos ingresos. Autoridades provinciales anunciaron mesas de diálogo para resolver el conflicto."),
        ("Descubrimiento arqueológico sacude a la comunidad yagana", "ana lópez   ",
         "Investigadores hallaron en la costa del Canal Beagle restos de herramientas de piedra atribuidas a la cultura yagana con más de mil años de antigüedad. El hallazgo se produjo durante una prospección arqueológica y plantea nuevas hipótesis sobre asentamientos tempranos. El Museo del Fin del Mundo prepara una exhibición para presentar las piezas al público."),
        # Invalidos
        ("Programa educativo digital llega a escuelas rurales", "                   ",
         "El Ministerio de Educación lanzó una plataforma digital con contenidos interactivos para estudiantes de zonas rurales de Tierra del Fuego. Incluye clases en video, ejercicios evaluables y seguimiento docente. El programa busca reducir la brecha educativa y fomentar habilidades digitales. Se proyecta expandir el alcance a más de cincuenta instituciones durante el próximo semestre."),
        ("", "ana lópez   ",
         "Datos del sector energético indican una disminución del 12% en las exportaciones de crudo desde la refinería de Río Grande en abril. La baja se atribuye a la menor demanda internacional y ajustes en la producción por mantenimiento de equipos. Empresas evalúan estrategias comerciales para diversificar destinos y mejorar la competitividad. Asimismo, se analizan oportunidades en mercados asiáticos para recuperar volumen de envíos durante la próxima temporada."),
        ("", "María Pérez  ", "Título faltante para validar filtro."),
        ("Titular de prueba", "", "Autor faltante para validar filtro."),
        ("Titular de prueba", "Autor de prueba", ""),
        ]

    def run(self):
        articulos = [Articulo(t, a, tx) for t, a, tx in  self.ejemplos_norm + self.ejemplos_reales]
        parser = ParserHtml(articulos)
        parser.generate_html()

if __name__ == "__main__":
    HtmlApp().run()
