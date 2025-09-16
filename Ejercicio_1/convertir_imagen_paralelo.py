from PIL import Image
import os
import time
from concurrent.futures import ProcessPoolExecutor
import shutil

# Función para convertir una imagen a escala de grises con sufijo _gris
def convertir_a_gris(ruta_imagen):
    try:
        imagen = Image.open(ruta_imagen)
        imagen_gris = imagen.convert('L')  # 'L' = escala de grises

        # carpeta de salida
        directorio_salida = "./imagenes_convertidas"
        os.makedirs(directorio_salida, exist_ok=True)  # la crea si no existe

        # nombre del archivo original
        nombre_archivo = os.path.basename(ruta_imagen)
        nombre_salida, extension = os.path.splitext(nombre_archivo)

        # ruta de salida
        ruta_gris = os.path.join(directorio_salida, nombre_salida + "_gris" + extension)

        imagen_gris.save(ruta_gris)
        print(f"Imagen convertida: {ruta_imagen} -> {ruta_gris}")
    except FileNotFoundError:
        print(f"No se encontró la imagen {ruta_imagen}")
    except Exception as e:
        print(f"Error al procesar {ruta_imagen}: {e}")

# Procesamiento paralelo
def procesar_imagenes_paralelo(lista_imagenes):
    with ProcessPoolExecutor() as executor:
        executor.map(convertir_a_gris, lista_imagenes)

 # Programa principal 
if __name__ == "__main__":
    directorio_imagenes = "./imagenes_originales"
    directorio_convertidas = "./imagenes_convertidas"

    # Funcion limpiar carpeta
    def limpiar_carpeta(directorio):
        if os.path.exists(directorio):
            shutil.rmtree(directorio)  # elimina la carpeta completa
        os.makedirs(directorio, exist_ok=True)  # la vuelve a crear
        print(f"Carpeta '{directorio}' limpiada.")

    opcion = input("¿Desea limpiar la carpeta de imágenes convertidas antes de empezar? (s/n): ").lower()
    if opcion == "s":
        limpiar_carpeta(directorio_convertidas)

    # Lista con las rutas completas de todas las imágenes dentro de la carpeta 'imagenes_originales'
    lista_imagenes = [
        os.path.join(directorio_imagenes, f)
        for f in os.listdir(directorio_imagenes)
        if os.path.isfile(os.path.join(directorio_imagenes, f))
    ]

    print("Procesamiento Paralelo")
    inicio = time.time()
    procesar_imagenes_paralelo(lista_imagenes)
    fin = time.time()
    print("Tiempo Paralelo:", fin - inicio, "segundos")

