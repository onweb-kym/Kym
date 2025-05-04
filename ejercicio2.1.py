import os
import fitz  # PyMuPDF para el procesamiento de archivos PDF
from flask import Flask, request

aplicacion = Flask(__name__)

CARPETA_SUBIDAS = 'archivos_subidos'
if not os.path.exists(CARPETA_SUBIDAS):
    os.makedirs(CARPETA_SUBIDAS)

aplicacion.config['CARPETA_SUBIDAS'] = CARPETA_SUBIDAS


def analizar_archivo(ruta_archivo, ruta_resumen):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            lineas = contenido.split('\n')
            palabras = contenido.split()
            caracteres = len(contenido)

        resumen = f"Resumen del archivo:\nLíneas: {len(lineas)}\nPalabras: {len(palabras)}\nCaracteres: {caracteres}\n"

        with open(ruta_resumen, 'w', encoding='utf-8') as archivo_resumen:
            archivo_resumen.write(resumen)

        return resumen
    except Exception as error:
        return f"Error procesando el archivo: {error}"


def leer_pdf(ruta_pdf):
    """Extrae el texto de un archivo PDF y lo devuelve como string"""
    try:
        documento = fitz.open(ruta_pdf)
        texto = ""

        for pagina in documento:
            texto += pagina.get_text("text") + "\n"

        return texto
    except Exception as error:
        return f"Error al leer el archivo PDF: {error}"


@aplicacion.route('/')
def inicio():
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Subir Archivo para Análisis</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: #333;
            }
            .contenedor {
                text-align: center;
                padding: 20px;
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 90%;
                max-width: 500px;
            }
            h1 {
                font-size: 1.8rem;
                color: #4caf50;
            }
            form {
                margin: 20px 0;
            }
            input[type="file"] {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 1rem;
            }
            button {
                background: #4caf50;
                color: #fff;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 1rem;
                cursor: pointer;
            }
            button:hover {
                background: #45a049;
            }
            footer {
                margin-top: 10px;
                font-size: 0.9rem;
                color: #777;
            }
        </style>
    </head>
    <body>
        <div class="contenedor">
            <h1>Subir Archivo para Análisis</h1>
            <form action="/Ejercicio unidad 3" method="post" enctype="multipart/form-data">
                <input type="file" name="archivo" accept=".txt, .pdf" required>
                <br><br>
                <button type="submit">Subir y Procesar</button>
            </form>
            <footer>
                <p>Desarrollado con Flask · Ejercicio Mejorado</p>
            </footer>
        </div>
    </body>
    </html>
    '''


@aplicacion.route('/Ejercicio unidad 3', methods=['POST'])
def subir_archivo():
    if 'archivo' not in request.files:
        return "No se subió ningún archivo."

    archivo = request.files['archivo']
    if archivo.filename == '':
        return "No se seleccionó ningún archivo."

    ruta_archivo = os.path.join(aplicacion.config['CARPETA_SUBIDAS'], archivo.filename)
    archivo.save(ruta_archivo)

    ruta_resumen = os.path.join(aplicacion.config['CARPETA_SUBIDAS'], 'resumen.txt')

    # Detectar el tipo de archivo y procesarlo
    if archivo.filename.endswith('.txt'):
        resumen = analizar_archivo(ruta_archivo, ruta_resumen)
    elif archivo.filename.endswith('.pdf'):
        contenido = leer_pdf(ruta_archivo)
        palabras = contenido.split()
        caracteres = len(contenido)
        resumen = f"Resumen del archivo PDF:\nPalabras: {len(palabras)}\nCaracteres: {caracteres}\n"

        with open(ruta_resumen, 'w', encoding='utf-8') as archivo_resumen:
            archivo_resumen.write(resumen)
    else:
        return "Tipo de archivo no soportado."

    return f"<h1>Archivo procesado con éxito</h1><pre>{resumen}</pre>"


if __name__ == '__main__':
    aplicacion.run(debug=True)
