import pandas as pd
import os
import re
import zlib
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN DE RUTAS Y ENTORNO ---
DIR_ENTRADA = r"C:\Users\enson\Desktop\TFG\HTML_Champions\Partidos a analizar (Campeones_o_Semis)"
DIR_SALIDA = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Champions League"

def preprocesar_html(contenido_html):
    """
    Elimina los bloques de comentarios HTML (<!-- -->) para exponer 
    las estructuras tabulares que permanecen ocultas en el código fuente.
    """
    return contenido_html.replace("<!--", "").replace("-->", "")

def generar_clave_primaria_hash(fecha, rival):
    """
    Genera un identificador numérico único e inmutable (Hash CRC32) basado en 
    la firma temporal y el rival para mantener la integridad referencial.
    """
    cadena_firma = f"{fecha}_{rival}"
    return zlib.crc32(cadena_firma.encode('utf-8'))

def estandarizar_formato_fecha(fecha_cruda):
    """
    Normaliza la cadena temporal mediante Expresiones Regulares (Regex) eliminando 
    ruido contextual (paréntesis, nombres de torneos) para compatibilidad con Power BI.
    """
    fecha_limpia = re.sub(r'\s*\(.*?\)', '', fecha_cruda)
    fecha_limpia = re.sub(r'El\s*Cl[áa]sico', '', fecha_limpia, flags=re.IGNORECASE)
    return " ".join(fecha_limpia.split())

def extraer_metadatos_y_alineaciones(ruta_archivo):
    """
    Parsea el documento HTML para extraer metadatos del partido (posesión, goles) 
    y ejecuta un algoritmo de inferencia por exclusión para deducir la alineación titular.
    """
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo_html:
            soup = BeautifulSoup(preprocesar_html(archivo_html.read()), "html.parser")
        
        # --- 1. EXTRACCIÓN DE METADATOS BASE ---
        titulo_documento = soup.title.string if soup.title else ""
        if "Barcelona" not in titulo_documento and "vs." not in titulo_documento:
            return None, [] 

        try:
            if "vs." in titulo_documento:
                segmentos = titulo_documento.split("vs.")
                if "Barcelona" in segmentos[0]:
                    rival = segmentos[1].split("Match Report")[0].strip()
                else:
                    rival = segmentos[0].strip()
            else:
                rival = "Desconocido"
            
            coincidencia_fecha = re.search(r'Match Report – (.+)', titulo_documento)
            fecha = estandarizar_formato_fecha(coincidencia_fecha.group(1).split("|")[0].strip()) if coincidencia_fecha else "Unknown"
            id_partido = generar_clave_primaria_hash(fecha, rival)
        except Exception:
            return None, [] 

        # --- 2. IDENTIFICACIÓN DE SUPLENTES (Análisis de Telemetría Temporal) ---
        # Se escanea el cronograma de eventos para aislar los identificadores (href) 
        # de los jugadores que ingresaron al campo como sustitutos.
        conjunto_suplentes_href = set()
        contenedor_eventos = soup.find("div", id="events_wrap")
        
        if contenedor_eventos:
            for evento in contenedor_eventos.find_all("div", class_="event"):
                if "sub" in str(evento).lower():
                    enlaces_jugadores = evento.find_all("a")
                    # La estructura del DOM sitúa al jugador entrante en el primer nodo de anclaje
                    if len(enlaces_jugadores) > 0:
                        href_jugador = enlaces_jugadores[0].get("href")
                        if href_jugador: 
                            conjunto_suplentes_href.add(href_jugador)

        # --- 3. EXTRACCIÓN DE ESTADÍSTICAS E INFERENCIA DE TITULARIDAD ---
        diccionario_metadatos = {
            "id_partido": id_partido, 
            "fecha": fecha, 
            "rival": rival,
            "posesion_barca": None,
            "goles_barca": 0
        }
        lista_eventos_titulares = []

        # Subrutina: Posesión y Marcador
        try:
            caja_estadisticas = soup.find("div", id="team_stats")
            if caja_estadisticas:
                for fila in caja_estadisticas.find_all("tr"):
                    if "Possession" in fila.get_text():
                        valores = fila.find_all("td")
                        if valores: diccionario_metadatos["posesion_barca"] = valores[0].get_text().strip()
            
            caja_marcador = soup.find("div", class_="scorebox")
            if caja_marcador:
                nodos_marcador = caja_marcador.find_all("div", class_="score")
                if len(nodos_marcador) >= 2: diccionario_metadatos["goles_barca"] = nodos_marcador[0].get_text().strip()
        except Exception: 
            pass

        # Subrutina: Inferencia de Titulares
        try:
            tablas_documento = soup.find_all("table")
            for tabla in tablas_documento:
                leyenda_tabla = tabla.caption.get_text() if tabla.caption else ""
                
                # Aislamiento de la matriz estadística global del equipo objetivo
                if "Barcelona" in leyenda_tabla and "Stats" in leyenda_tabla and "Goalkeeper" not in leyenda_tabla:
                    cuerpo_tabla = tabla.find("tbody")
                    if cuerpo_tabla:
                        filas_datos = cuerpo_tabla.find_all("tr")
                        for fila in filas_datos:
                            clases_fila = fila.get("class", [])
                            # Omisión de encabezados secundarios o espaciadores de diseño
                            if "thead" in clases_fila or "spacer" in clases_fila: continue

                            nodo_jugador = fila.find("th", {"data-stat": "player"})
                            if nodo_jugador:
                                etiqueta_enlace = nodo_jugador.find("a")
                                if etiqueta_enlace:
                                    nombre_jugador = etiqueta_enlace.get_text(strip=True)
                                    href_identificador = etiqueta_enlace.get("href") 
                                    
                                    # LÓGICA DE INFERENCIA POR EXCLUSIÓN:
                                    # Si un jugador con actividad registrada en el partido NO figura 
                                    # en el conjunto de suplentes entrantes, se deduce unívocamente 
                                    # su condición de componente de la alineación titular.
                                    if href_identificador not in conjunto_suplentes_href:
                                        lista_eventos_titulares.append({
                                            "id_partido": id_partido,
                                            "fecha": fecha,
                                            "equipo_rival": rival,
                                            "minuto": 0,
                                            "jugador_implicado": nombre_jugador,
                                            "tipo_evento": "TITULAR",
                                            "detalle_accion": "Alineación Inicial",
                                            "fase": "Champions"
                                        })
        except Exception:
            pass

        return diccionario_metadatos, lista_eventos_titulares

    except Exception as e:
        print(f"Error de procesamiento en el archivo {os.path.basename(ruta_archivo)}: {e}")
        return None, []

def ejecutar_extraccion_titulares_champions():
    """
    Orquesta el flujo de procesamiento iterativo sobre el directorio de documentos HTML,
    consolidando los resultados de metadatos e inferencias de titularidad en 
    estructuras relacionales (CSVs) para su ingesta analítica.
    """
    print("--- INICIANDO INFERENCIA DE ALINEACIONES (LÓGICA DE EXCLUSIÓN) ---")
    
    if not os.path.exists(DIR_ENTRADA):
        print("Error crítico: El directorio de origen especificado no existe.")
        return

    registros_metadatos = []
    registros_alineaciones = []
    partidos_procesados = 0
    
    # Exploración recursiva del sistema de archivos
    for raiz, directorios, ficheros in os.walk(DIR_ENTRADA):
        for fichero in ficheros:
            if fichero.endswith(".html"):
                ruta_completa = os.path.join(raiz, fichero)
                metadatos, titulares = extraer_metadatos_y_alineaciones(ruta_completa)
                
                if metadatos: 
                    registros_metadatos.append(metadatos)
                    partidos_procesados += 1
                if titulares: 
                    registros_alineaciones.extend(titulares)
                
                if partidos_procesados % 10 == 0: 
                    print(".", end="", flush=True)

    print(f"\nOperación iterativa finalizada. Total de encuentros analizados: {partidos_procesados}")

    # Consolidación y persistencia de las tablas de hechos (Fact Tables)
    if registros_metadatos:
        df_estadisticas_generales = pd.DataFrame(registros_metadatos)
        os.makedirs(DIR_SALIDA, exist_ok=True)
        ruta_salida_stats = os.path.join(DIR_SALIDA, "Fact_Champions_Stats.csv")
        df_estadisticas_generales.to_csv(ruta_salida_stats, index=False, encoding='utf-8-sig')
        print(f"Persistencia completada: Matriz de estadísticas globales exportada exitosamente.")

    if registros_alineaciones:
        df_alineaciones_titulares = pd.DataFrame(registros_alineaciones)
        ruta_salida_titulares = os.path.join(DIR_SALIDA, "Fact_Champions_Titulares.csv")
        df_alineaciones_titulares.to_csv(ruta_salida_titulares, index=False, encoding='utf-8-sig')
        print(f"Persistencia completada: Registro dimensional de titulares (vía exclusión ID) exportado exitosamente.")

if __name__ == "__main__":
    ejecutar_extraccion_titulares_champions()