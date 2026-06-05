import os
import pandas as pd
from bs4 import BeautifulSoup
import re
import warnings

# Supresión de advertencias no críticas relativas a tipos de datos y análisis de HTML en Pandas
warnings.filterwarnings("ignore") 

# --- CONFIGURACIÓN DEL ENTORNO Y RUTAS ---
BASE_DIR = r"C:\Users\enson\Desktop\TFG\ETL"
DIR_HTML_LOCAL = os.path.join(BASE_DIR, "HTML_Partidos")
PATH_OUTPUT_PARTIDOS = os.path.join(BASE_DIR, "CSV", "Fact_Tactica_Avanzada.csv")
PATH_OUTPUT_JUGADORES = os.path.join(BASE_DIR, "CSV", "Fact_Estadisticas_Jugadores_RAW.csv")

def extraer_metadatos_y_estadisticas_html():
    """
    Motor de procesamiento ETL local. Recorre recursivamente los documentos HTML 
    descargados, extrae metadatos tácticos (entrenador, posesión, esquema) mediante 
    análisis del DOM (BeautifulSoup) e infiere métricas estadísticas individuales 
    (DataFrames) correlacionando alineaciones y tablas de rendimiento.
    """
    print("INICIANDO")
    
    archivos_html = [f for f in os.listdir(DIR_HTML_LOCAL) if f.endswith('.html')]
    print(f"Info: Detectados {len(archivos_html)} documentos locales en cola de procesamiento\n")
    
    coleccion_metadatos_partidos = []
    coleccion_estadisticas_jugadores = []
    
    for archivo in archivos_html:
        ruta_absoluta = os.path.join(DIR_HTML_LOCAL, archivo)
        
        # 1. Parseo estático de metadatos desde la nomenclatura del archivo
        try:
            segmentos = archivo.replace(".html", "").split("_", 2)
            id_partido = segmentos[0]
            fecha_partido = segmentos[1]
            rival_partido = segmentos[2]
        except Exception:
            continue
            
        try:
            with open(ruta_absoluta, 'r', encoding='utf-8') as archivo_local:
                contenido_html = archivo_local.read()
                
            soup = BeautifulSoup(contenido_html, 'html.parser')
            
            # --- 2. EXTRACCIÓN DE METADATOS TÁCTICOS Y POSESIÓN ---
            entrenador_inferido = "Desconocido"
            posesion_inferida = None
            esquema_tactico = "Desconocida"
            
            # Evaluación del contenedor principal de la cabecera (Scorebox)
            caja_marcador = soup.find('div', class_='scorebox')
            if caja_marcador:
                nodos_entrenador = caja_marcador.find_all('div', class_='datapoint')
                for nodo in nodos_entrenador:
                    texto_nodo = nodo.text
                    if 'Manager' in texto_nodo or 'Entrenador' in texto_nodo:
                        texto_limpio = texto_nodo.replace('Manager:', '').replace('Entrenador:', '').strip()
                        # Validación heurística mediante lista blanca de técnicos históricos
                        lista_tecnicos_historicos = ['Xavi', 'Koeman', 'Rijkaard', 'Guardiola', 'Flick', 'Martino', 'Valverde', 'Setién', 'Enrique', 'Vilanova', 'Roura', 'Sergi']
                        if any(tecnico in texto_limpio for tecnico in lista_tecnicos_historicos):
                            entrenador_inferido = texto_limpio

            # Extracción del diferencial de posesión
            tabla_estadisticas_globales = soup.find('div', id='team_stats')
            if tabla_estadisticas_globales:
                for fila_stat in tabla_estadisticas_globales.find_all('tr'):
                    if 'Possession' in fila_stat.text or 'Posesión' in fila_stat.text:
                        valores_posesion = re.findall(r'\d+%', fila_stat.text)
                        if len(valores_posesion) >= 2:
                            posesion_inferida = f"{valores_posesion[0]} - {valores_posesion[1]}"

            # --- 3. RECONSTRUCCIÓN DE ALINEACIONES (Contexto Titular/Suplente) ---
            contenedores_alineacion = soup.find_all('div', class_='lineup')
            diccionario_titularidad = {} 
            diccionario_posiciones = {} 
            
            for alineacion in contenedores_alineacion:
                cabecera_tabla = alineacion.find('th')
                if cabecera_tabla and 'Barcelona' in cabecera_tabla.text:
                    # Inferencia de la formación inicial mediante expresiones regulares
                    coincidencia_formacion = re.search(r'\(([\d-]+)\)', cabecera_tabla.text)
                    if coincidencia_formacion:
                        esquema_tactico = coincidencia_formacion.group(1)
                        
                    es_titular_flag = 1
                    for fila_jugador in alineacion.find_all('tr')[1:]:
                        # Detección de separadores estructurales (Inicio de banquillo de suplentes)
                        if fila_jugador.find('td', class_='spacer') or 'Bench' in fila_jugador.text or 'Banquillo' in fila_jugador.text:
                            es_titular_flag = 0
                            continue
                            
                        enlace_jugador = fila_jugador.find('a')
                        if enlace_jugador:
                            nombre_jugador = enlace_jugador.text.strip()
                            diccionario_titularidad[nombre_jugador] = es_titular_flag
                            
                            # Extracción de la nomenclatura de posición táctica
                            celdas_datos = fila_jugador.find_all('td')
                            if len(celdas_datos) > 1:
                                diccionario_posiciones[nombre_jugador] = celdas_datos[1].text.strip()

            # --- 4. EXTRACCIÓN DE ESTADÍSTICAS AVANZADAS (Parseo Vectorizado) ---
            # Delegamos a Pandas la construcción estructural de todas las tablas HTML del documento
            dataframes_html = pd.read_html(contenido_html)
            estadisticas_localizadas = False
            
            for df_tabla in dataframes_html:
                # Aplanamiento de cabeceras jerárquicas (MultiIndex)
                if isinstance(df_tabla.columns, pd.MultiIndex):
                    columnas_aplanadas = [col[1] for col in df_tabla.columns]
                    df_tabla.columns = columnas_aplanadas
                else:
                    columnas_aplanadas = df_tabla.columns.tolist()
                    
                # Criterio de validación: La tabla debe contener referencias explícitas a jugadores
                if 'Player' in columnas_aplanadas or 'Jugador' in columnas_aplanadas:
                    nombres_en_tabla = df_tabla.iloc[:, 0].astype(str).tolist()
                    
                    # Criterio heurístico de pertenencia: Se requiere un umbral mínimo de 
                    # 3 coincidencias con nuestra alineación titular para confirmar el dataset correcto.
                    coincidencias_positivas = sum(1 for nombre in nombres_en_tabla if nombre in diccionario_titularidad)
                    
                    if coincidencias_positivas >= 3:
                        estadisticas_localizadas = True
                        for _, registro_estadistico in df_tabla.iterrows():
                            jugador = str(registro_estadistico.iloc[0])
                            
                            # Omisión de filas totalizadoras o celdas vacías
                            if jugador == 'nan' or 'Players' in jugador or 'Jugadores' in jugador:
                                continue
                            
                            # Extracción y casteo de métricas. Se infiere 0 ante ausencia de datos (temporadas antiguas)
                            minutos = registro_estadistico.get('Min', 0)
                            goles = registro_estadistico.get('Gls', 0)
                            asistencias = registro_estadistico.get('Ast', 0)
                            
                            amarillas = registro_estadistico.get('CrdY', 0) if 'CrdY' in columnas_aplanadas else 0
                            rojas = registro_estadistico.get('CrdR', 0) if 'CrdR' in columnas_aplanadas else 0
                            xg_esperado = registro_estadistico.get('xG', 0) if 'xG' in columnas_aplanadas else None
                            
                            coleccion_estadisticas_jugadores.append({
                                'ID_Partido': id_partido,
                                'Jugador': jugador,
                                'Posicion_Partido': diccionario_posiciones.get(jugador, ""),
                                'Titular': diccionario_titularidad.get(jugador, 0),
                                'Minutos': minutos,
                                'Goles': goles,
                                'Asistencias': asistencias,
                                'Amarillas': amarillas,
                                'Rojas': rojas,
                                'xG': xg_esperado
                            })
                        break # Ruptura del bucle tras localizar y procesar la tabla del equipo objetivo
            
            # Contingencia: Persistencia mínima de datos (Alineación) ante ausencia de tablas avanzadas
            if not estadisticas_localizadas:
                for jugador, flag_titular in diccionario_titularidad.items():
                    coleccion_estadisticas_jugadores.append({
                        'ID_Partido': id_partido,
                        'Jugador': jugador,
                        'Posicion_Partido': diccionario_posiciones.get(jugador, ""),
                        'Titular': flag_titular,
                        'Minutos': None, 'Goles': None, 'Asistencias': None,
                        'Amarillas': None, 'Rojas': None, 'xG': None
                    })

            # Inserción del registro en la tabla de hechos (Fact Table) de contexto
            coleccion_metadatos_partidos.append({
                'ID_Partido': id_partido,
                'Fecha': fecha_partido,
                'Rival': rival_partido,
                'Entrenador': entrenador_inferido,
                'Formacion': esquema_tactico,
                'Posesion_Bruta': posesion_inferida
            })
            
        except Exception:
            # Control pasivo de errores iterativos para prevenir la interrupción del bucle principal
            pass

    # 5. Consolidación y exportación de modelos relacionales
    df_contexto_partidos = pd.DataFrame(coleccion_metadatos_partidos)
    df_estadisticas_individuales = pd.DataFrame(coleccion_estadisticas_jugadores)
    
    df_contexto_partidos.to_csv(PATH_OUTPUT_PARTIDOS, index=False, encoding='utf-8-sig')
    df_estadisticas_individuales.to_csv(PATH_OUTPUT_JUGADORES, index=False, encoding='utf-8-sig')
    
    print("\nProceso ETL completado con éxito.")
    print(f"Total de contextos tácticos analizados: {len(df_contexto_partidos)}")
    print(f"Total de registros de rendimiento individual procesados: {len(df_estadisticas_individuales)}")
    print("Archivos exportados exitosamente al directorio local.")

if __name__ == "__main__":
    extraer_metadatos_y_estadisticas_html()