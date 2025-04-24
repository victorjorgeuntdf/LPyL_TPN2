import os
import shutil
from articulo import Articulo, InvalidArticleError
from parser_html import ParserHtml

# Test de la clase Articulo
def test_articulo_snippet_and_slug():
    long_text = "x" * 350
    art = Articulo("Long Title Sample", "John Doe", long_text)
    assert art.snippet() == "x" * 300 + "…"

    short_text = "Texto corto"
    art2 = Articulo("Valid Title", "Jane Roe", short_text)
    assert art2.snippet() == short_text

    art3 = Articulo("Test Title", "Author Example", "Content sufficient")
    assert art3.slug() == "test-title"

# Test de ParserHtml: filtrado y normalización
def test_filter_and_normalize():
    raw = [
        Articulo("Short", "A B", "Valid text content longer"),         # título muy corto
        Articulo("Valid Title", "", "Valid text content longer"),     # autor vacío
        Articulo("Valid Title", "john doe", "Short"),                 # texto muy corto
        Articulo("Valid Title", "john doe", "Valid text content OK")  # válido
    ]
    tmp = "tmp_test"
    parser = ParserHtml(raw, output_dir=tmp)
    assert len(parser.articulos) == 1
    valid = parser.articulos[0]
    assert valid.autor == "John Doe"
    assert valid.titulo == "Valid Title"
    shutil.rmtree(tmp)

# Test de métodos de filtrado
def test_filter_methods():
    arts = [
        Articulo("Article One", "Alice Smith", "Python is great and versatile"),
        Articulo("Article Two", "Bob Brown", "JavaScript is also great and popular")
    ]
    tmp = "tmp2"
    parser = ParserHtml(arts, output_dir=tmp)
    # Filtrado por palabra clave
    kw = parser.filter_by_keyword("python")
    assert len(kw) == 1 and kw[0].autor == "Alice Smith"

    # Filtrado por inicial del apellido
    init = parser.filter_by_initial("B")
    assert len(init) == 1 and init[0].autor == "Bob Brown"

    shutil.rmtree(tmp)

# Test de generación de archivos HTML
def test_generate_html_creates_files():
    art = Articulo("Test Title A", "Ann A", "Some long text " * 20)
    tmp = "tmp_html"
    parser = ParserHtml([art], output_dir=tmp)
    parser.generate_html()

    files = os.listdir(tmp)
    assert "index.html" in files
    assert "resumen.html" in files
    article_pages = [f for f in files if f.endswith(".html") and f not in ("index.html", "resumen.html")]
    assert len(article_pages) == 1

    shutil.rmtree(tmp)

if __name__ == "__main__":
    test_articulo_snippet_and_slug()
    test_filter_and_normalize()
    test_filter_methods()
    test_generate_html_creates_files()
    print("¡Todos los tests pasaron!")
