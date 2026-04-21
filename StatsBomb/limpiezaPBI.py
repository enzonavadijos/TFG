# -*- coding: utf-8 -*-
import os
import glob
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

carpeta_origen = "datos_fbref_estable"
carpeta_destino = "Datos_PBI_Por_Competicion"

# Buscamos todos los CSV en la carpeta origen y subcarpetas
archivos = glob.glob(f"{carpeta_origen}/**/*.csv", recursive=True)
logging.info(f"Encontrados {len(archivos)} archivos. Iniciando reorganización de carpetas...")

for archivo in archivos:
    # Extraemos el nombre del archivo, ej: "General_LaLiga_2018-2019.csv"
    nombre_archivo = os.path.basename(archivo)
    nombre_sin_ext = nombre_archivo.replace(".csv", "")
    partes = nombre_sin_ext.split("_")
    
    # Identificamos la competición y la temporada según el nombre del archivo
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
        # Para LaLiga y Champions
        competicion = partes[1]
        temporada = partes[2]

    # 1. Creamos la carpeta específica de la competición en el destino
    ruta_carpeta_competicion = os.path.join(carpeta_destino, competicion)
    os.makedirs(ruta_carpeta_competicion, exist_ok=True)

    # 2. Leemos el CSV
    try:
        df = pd.read_csv(archivo)
        
        # 3. Añadimos ÚNICAMENTE la columna 'Temporada' (la ponemos la primera para que se vea bien)
        if 'Temporada' not in df.columns:
            df.insert(0, 'Temporada', temporada)
        
        # 4. Lo guardamos en su nueva carpeta sin mezclarlo con otros
        ruta_final = os.path.join(ruta_carpeta_competicion, nombre_archivo)
        df.to_csv(ruta_final, index=False, encoding='utf-8-sig')
        
    except Exception as e:
        logging.error(f"Error procesando {archivo}: {e}")

logging.info("\n¡Proceso completado!")
logging.info(f"Revisa la carpeta '{carpeta_destino}'. Tendrás subcarpetas limpias por torneo y los archivos con su columna 'Temporada' lista para Power BI.")