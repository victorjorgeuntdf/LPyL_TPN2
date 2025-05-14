import os
import zipfile
from datetime import datetime

def crear_zip_proyecto():
    # Configuración
    nombre_zip = f"noticias_del_fuego_{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
    archivos_a_incluir = [
        'articulo.py',
        'parser_html.py',
        'runner.py',
        'test_parser.py',
        'parse.py',
        'LICENSE',
        'README.md',
        'TP 2.pdf',
        'crear_zip.py',
    ]
    carpetas_a_incluir = [
        'static' ,
        'output',
    ]

    # Crear el archivo ZIP
    with zipfile.ZipFile(nombre_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Agregar archivos individuales
        for archivo in archivos_a_incluir:
            if os.path.exists(archivo):
                zipf.write(archivo)
                print(f"Agregado: {archivo}")
            else:
                print(f"Advertencia: {archivo} no encontrado, omitiendo")

        # Agregar carpetas y su contenido
        for carpeta in carpetas_a_incluir:
            if os.path.exists(carpeta):
                for root, dirs, files in os.walk(carpeta):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=os.path.dirname(carpeta))
                        zipf.write(file_path, arcname)
                        print(f"Agregado: {file_path} como {arcname}")
            else:
                print(f"Advertencia: carpeta {carpeta} no encontrada, omitiendo")

    print(f"\nArchivo ZIP creado exitosamente: {nombre_zip}")
    print(f"Tamaño: {os.path.getsize(nombre_zip)/1024:.2f} KB")

if __name__ == "__main__":
    crear_zip_proyecto()