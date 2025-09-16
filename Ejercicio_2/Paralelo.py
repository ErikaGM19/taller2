# Librerías necesarias para ejecutar el código:
import multiprocessing as mp
import time


# Se define una función para la etapa relacionada a leer los archivos. Se asigna un tamaño de bloque de 10000 para pasar a la siguiente etapa:
def leer_archivo(ruta_entrada, cola_salida, chunk_size=10000):

    # Se lee el archivo:
    with open(ruta_entrada, "r", encoding="utf-8") as f:

        # Se van creando los bloques:
        bloque = []

        # Se lee línea a línea:
        for linea in f:

            # Se va almacenando en el bloque, siempre y cuando no supere el tamaño propuesto:
            bloque.append(linea)
            if len(bloque) >= chunk_size:
                cola_salida.put(bloque)
                bloque = []
        
        # Se manda el bloque a la siguiente etapa:
        if bloque:
            cola_salida.put(bloque)
    
    # Se crea la señal de finalización:
    cola_salida.put(None) 


# Se define una función para la etapa relacionada a limpiar los espacios de las líneas de código:
def limpiar_lineas(cola_entrada, cola_salida):

    # Se obtienen los bloques recibidos de la anterior etapa:
    while True:
        bloque = cola_entrada.get()

        # Se crea la señal de finalización:
        if bloque is None:
            cola_salida.put(None)
            break

        # Se limpian los bloques de líneas y se pasan a la siguiente etapa:
        bloque_limpio = [linea.strip() for linea in bloque]
        cola_salida.put(bloque_limpio)


# Se define una función para la etapa relacionada a convertir a mayúsculas el texto:
def convertir_mayusculas(cola_entrada, cola_salida):

    # Se obtienen los bloques recibidos de la anterior etapa:
    while True:
        bloque = cola_entrada.get()

        # Se crea la señal de finalización:
        if bloque is None:
            cola_salida.put(None)
            break

        # Se transforman los bloques de líneas a mayúsculas y se pasan a la siguiente etapa:
        bloque_upper = [linea.upper() for linea in bloque]
        cola_salida.put(bloque_upper)


# Se define una función para la etapa relacionada a guardar los resultados en archivos:
def escribir_archivo(ruta_salida, cola_entrada):

    # Se abre / crea el archivo donde se guardarán los resultados:
    with open(ruta_salida, "w", encoding="utf-8") as f:

        while True:

            # Se crea la señal de finalización:
            bloque = cola_entrada.get()
            if bloque is None:
                break

            # Se almacenan los bloques línea por línea en el archivo:
            for linea in bloque:
                f.write(linea + "\n")


# Se define una función para estructurar el pipeline:
def procesar_texto_pipeline(ruta_entrada, ruta_salida):

    # Se crean las colas transportadoras de bloques:
    cola1 = mp.Queue()
    cola2 = mp.Queue()
    cola3 = mp.Queue()

    # Se define la estructura del pipeline:
    procesos = [
        mp.Process(target=leer_archivo, args=(ruta_entrada, cola1)),
        mp.Process(target=limpiar_lineas, args=(cola1, cola2)),
        mp.Process(target=convertir_mayusculas, args=(cola2, cola3)),
        mp.Process(target=escribir_archivo, args=(ruta_salida, cola3)),
    ]

    # Se inician los procesos:
    for p in procesos: p.start()

    # Se finalizan los procesos:
    for p in procesos: p.join()


# Función principal para ejecutar el código:
if __name__ == "__main__":
    
    # Rutas para cargar y guardar los archivos:
    ruta_entrada = "Entradas/texto_entrada.txt"
    ruta_salida = "Salidas/Paralelo/texto_salida_pipeline.txt"

    # Se inicia la transformación:
    inicio = time.time()
    procesar_texto_pipeline(ruta_entrada, ruta_salida)
    fin = time.time()

    # Se imprimen los resultados:
    print(f"Tiempo total de procesamiento paralelo: {fin - inicio:.2f} segundos")
    print(f"Archivo procesado paralelamente guardado en {ruta_salida}")
   