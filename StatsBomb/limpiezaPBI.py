import os
import glob
import pandas as pd
import logging

# --- CONFIGURACIÓN DEL SISTEMA DE AUDITORÍA (LOGGING) ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [ETL] - %(message)s')

# --- CONFIGURACIÓN DE RUTAS ---
DIR_ORIGEN = "datos_fbref_estable"
DIR_DESTINO = "Datos_PBI_Por_Competicion"

def ejecutar_enriquecimiento_y_particionado():
    """
    Orquesta la fase final de transformación y particionado del modelo de datos.
    Recorre el repositorio estructurado, extrae metadatos (competición y temporada) 
    desde la nomenclatura de los archivos, inyecta la dimensión temporal (Temporada) 
    en el DataFrame y particiona físicamente los archivos resultantes por competición 
    para optimizar su posterior ingesta y modelado en Power BI.
    """
    logging.info("--- INICIANDO ENRIQUECIMIENTO DIMENSIONAL Y PARTICIONADO ---")
    
    # Búsqueda recursiva del lote de archivos CSV consolidados en las fases previas
    coleccion_archivos = glob.glob(f"{DIR_ORIGEN}/**/*.csv", recursive=True)
    logging.info(f"Info: Detectados {len(coleccion_archivos)} modelos tabulares. Iniciando reorganización topológica...")

    for archivo in coleccion_archivos:
        # Extracción de metadatos desde la nomenclatura del archivo
        # Ej: "General_LaLiga_2018-2019.csv"
        nombre_archivo = os.path.basename(archivo)
        nombre_sin_ext = nombre_archivo.replace(".csv", "")
        partes = nombre_sin_ext.split("_")
        
        # Clasificación heurística de la competición y resolución de la temporada
        if "Supercopa_Espana" in nombre_archivo:
            competicion = "Supercopa_Espana"
            temporada = partes[-1]
        elif "Supercopa_Europa" in nombre_archivo:
            competicion = "Supercopa_Europa"
            temporada = partes[-1]
        elif "CopaDelRey" in nombre_archivo:
            competicion = "CopaDelRey"
            temporada = partes[-1]
        else:
            # Lógica de asignación para competiciones regulares (LaLiga, Champions)
            competicion = partes[1]
            temporada = partes[2]

        # 1. Particionado Físico: Creación del directorio de dominio (Competición)
        ruta_directorio_competicion = os.path.join(DIR_DESTINO, competicion)
        os.makedirs(ruta_directorio_competicion, exist_ok=True)

        # 2. Ingesta del modelo tabular individual
        try:
            df = pd.read_csv(archivo)
            
            # 3. Enriquecimiento Dimensional
            # Inyección de la variable temporal (Temporada) como primer atributo (índice 0)
            # para facilitar su indexación y modelado semántico en herramientas OLAP.
            if 'Temporada' not in df.columns:
                df.insert(0, 'Temporada', temporada)
            
            # 4. Persistencia en el nuevo esquema particionado
            ruta_salida = os.path.join(ruta_directorio_competicion, nombre_archivo)
            
            # Exportación con codificación 'utf-8-sig' para preservar caracteres especiales (ej. tildes, eñes)
            df.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
            
        except Exception as e:
            logging.error(f"Fallo durante la transformación estructural del recurso {archivo}: {e}")

    logging.info("\n" + "="*70)
    logging.info("PROCESO DE PARTICIONADO Y ENRIQUECIMIENTO FINALIZADO EXITOSAMENTE")
    logging.info(f"Los modelos han sido estructurados en el directorio: '{DIR_DESTINO}'.")
    logging.info("El ecosistema de datos está preparado para su importación a Power BI.")
    logging.info("="*70)

if __name__ == "__main__":
    ejecutar_enriquecimiento_y_particionado()