import pandas as pd
import os
import re
import zlib
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN DEL ENTORNO Y RUTAS ---
DIR_ENTRADA = r"C:\Users\enson\Desktop\TFG\HTML_Champions\Partidos a analizar (Campeones_o_Semis)"
RUTA_SALIDA = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Champions League\eventos_champions_importantes.csv"

def limpiar_comentarios_html(contenido_html):
    """
    Preprocesamiento del código fuente: Elimina las etiquetas de comentario HTML (<!-- -->)
    para exponer al parser tablas y divisiones que la fuente original mantiene ocultas
    hasta la ejecución de scripts JavaScript.
    """
    return contenido_html.replace("<!--", "").replace("-->", "")

def estandarizar_formato_fecha(fecha_cruda):
    """
    Rutina de limpieza estricta mediante expresiones regulares (Regex) para garantizar 
    la compatibilidad del campo temporal con los motores de Business Intelligence (ej. Power BI).
    Transforma formatos con sufijos contextuales en cadenas de fecha puras.
    Ejemplo Entrada: "Saturday April 10, 2010 El Clásico (Leg 1)"
    Ejemplo Salida:  "Saturday April 10, 2010"
    """
    if not isinstance(fecha_cruda, str):
        return ""
        
    # 1. Supresión de información contextual entre paréntesis (ej: "(Leg 1)", "(Extra Time)")
    fecha_limpia = re.sub(r'\s*\(.*?\)', '', fecha_cruda)
    
    # 2. Supresión de nombres comerciales de los enfrentamientos
    fecha_limpia = re.sub(r'El\s*Cl[áa]sico', '', fecha_limpia, flags=re.IGNORECASE)
    
    # 3. Eliminación de separadores de bloque o guiones residuales
    fecha_limpia = fecha_limpia.replace("–", "").replace("-", "")
    
    # 4. Normalización de espacios (eliminación de espacios dobles o saltos de línea ocultos)
    return " ".join(fecha_limpia.split())

def detectar_fase_competicion(soup):
    """
    Algoritmo de inferencia jerárquica para determinar la fase eliminatoria
    del encuentro basándose en el análisis semántico de la cabecera (scorebox).
    """
    try:
        caja_marcador = soup.find("div", class_="scorebox")
        if not caja_marcador:
            return "Fase Desconocida"
        
        texto_inferido = caja_marcador.get_text().lower()

        # Árbol de decisión basado en palabras clave (keywords)
        if "final" in texto_inferido and "quarter" not in texto_inferido and "semi" not in texto_inferido and "1/8" not in texto_inferido:
            return "Final"
        elif "semi-finals" in texto_inferido or "semi-final" in texto_inferido:
            return "Semifinales"
        elif "quarter-finals" in texto_inferido or "quarter-final" in texto_inferido:
            return "Cuartos de Final"
        elif "round of 16" in texto_inferido or "octavos" in texto_inferido:
            return "Octavos de Final"
        elif "group stage" in texto_inferido:
            return "Fase de Grupos"
        else:
            return "Fase Eliminatoria" 
            
    except Exception:
        return "Fase Desconocida"

def extraer_metadatos_partido(soup):
    """
    Extrae los atributos descriptivos del encuentro desde la cabecera del documento HTML.
    """
    rival = "Desconocido"
    fecha_partido = "Desconocida"
    resultado_partido = "Unknown"
    
    # 1. Inferencia del Rival y Fecha desde la etiqueta <title>
    titulo_documento = soup.title.string if soup.title else ""
    if "vs." in titulo_documento:
        segmentos = titulo_documento.split("vs.")
        if "Barcelona" in segmentos[0]: 
            rival = segmentos[1].split("Match Report")[0].strip()
        else: 
            rival = segmentos[0].strip()
        
        # Extracción de la fecha empleando expresiones regulares
        coincidencia_fecha = re.search(r'Match Report – (.+)', titulo_documento)
        if coincidencia_fecha:
            fecha_aislada = coincidencia_fecha.group(1).split("|")[0].strip()
            fecha_partido = estandarizar_formato_fecha(fecha_aislada)

    # 2. Extracción del Resultado Final del encuentro
    try:
        caja_marcador = soup.find("div", class_="scorebox")
        if caja_marcador:
            nodos_resultado = caja_marcador.find_all("div", class_="score")
            if len(nodos_resultado) >= 2:
                goles_local = nodos_resultado[0].get_text(strip=True)
                goles_visitante = nodos_resultado[1].get_text(strip=True)
                resultado_partido = f"{goles_local}-{goles_visitante}"
    except Exception:
        pass

    # 3. Determinación algorítmica de la fase de competición
    fase_torneo = detectar_fase_competicion(soup)

    return fecha_partido, rival, resultado_partido, fase_torneo

def generar_clave_primaria_hash(fecha, rival):
    """
    Genera un identificador numérico único (Primary Key) mediante el algoritmo 
    de redundancia cíclica (CRC32), asegurando integridad referencial sin colisiones.
    """
    cadena_firma = f"{fecha}_{rival}"
    return zlib.crc32(cadena_firma.encode('utf-8'))

def procesar_timeline_eventos(ruta_archivo):
    """
    Parsea la estructura DOM del documento, extrae los metadatos principales 
    e itera sobre el contenedor cronológico ('timeline') para tipificar 
    y estructurar cada evento individual del partido.
    """
    nombre_archivo = os.path.basename(ruta_archivo)
    
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo_html:
            html_crudo = archivo_html.read()
        
        # Parseo del modelo de objetos del documento (DOM)
        html_limpio = limpiar_comentarios_html(html_crudo)
        soup = BeautifulSoup(html_limpio, "html.parser")
        
        # Extracción de entidades principales
        fecha, rival, resultado, fase = extraer_metadatos_partido(soup)
        id_partido_hash = generar_clave_primaria_hash(fecha, rival)
        
        # Generación de etiqueta descriptiva contextual
        etiqueta_contexto = f"{fase} vs {rival} ({fecha})"

        lista_eventos = []
        contenedor_eventos = soup.find("div", id="events_wrap")
        
        if not contenedor_eventos:
            return None

        # Iteración secuencial sobre el flujo de eventos
        for evento in contenedor_eventos.find_all("div", class_="event"):
            texto_completo = evento.get_text(" ", strip=True)
            
            # Extracción del timestamp del evento (minuto de juego)
            patron_tiempo = re.search(r"(\d+(?:\+\d+)?)\’", texto_completo)
            minuto_juego = patron_tiempo.group(1) if patron_tiempo else "0"
            
            # Tipificación semántica del evento
            tipo_incidencia = "Otro"
            identificador_icono = str(evento).lower()
            if "score" in identificador_icono or "goal" in identificador_icono: 
                tipo_incidencia = "Gol"
            elif "card" in identificador_icono:
                if "red" in identificador_icono or "yellow_red" in identificador_icono: 
                    tipo_incidencia = "Tarjeta Roja"
                else: 
                    tipo_incidencia = "Tarjeta Amarilla"
            elif "sub" in identificador_icono: 
                tipo_incidencia = "Sustitución"
            elif "penalty" in identificador_icono and "miss" in identificador_icono: 
                tipo_incidencia = "Penalti Fallado"

            # Parseo de entidades actoras y detalles de la acción
            enlaces_implicados = evento.find_all("a")
            jugador_principal = "Desconocido"
            detalle_evento = texto_completo
            
            if patron_tiempo: 
                detalle_evento = detalle_evento.replace(patron_tiempo.group(0), "").strip()
            
            if len(enlaces_implicados) > 0:
                jugador_principal = enlaces_implicados[0].get_text()
                detalle_evento = detalle_evento.replace(jugador_principal, "").strip()
                
                # Ramificación lógica según el tipo de incidencia
                if tipo_incidencia == "Sustitución":
                    if len(enlaces_implicados) > 1:
                        jugador_sustituido = enlaces_implicados[1].get_text()
                        detalle_evento = f"Entra al campo (Sale {jugador_sustituido})"
                    else:
                        detalle_evento = "Entra desde el banquillo"
                elif tipo_incidencia == "Gol":
                    detalle_evento = re.sub(r'\d+[:\-]\d+', '', detalle_evento).strip().replace("—", "").strip()
                    if "Assist" in texto_completo and len(enlaces_implicados) > 1:
                        jugador_asistente = enlaces_implicados[1].get_text()
                        detalle_evento = f"Asistencia de {jugador_asistente}"
                    elif "Penalty" in texto_completo: detalle_evento = "De Penalti"
                    elif "Head" in texto_completo: detalle_evento = "De Cabeza"
                    elif not detalle_evento: detalle_evento = "Jugada individual"
            elif "Card" in tipo_incidencia:
                 detalle_evento = re.sub(r'\d+[:\-]\d+', '', detalle_evento).strip()
                 detalle_evento = detalle_evento.replace("Yellow Card", "").replace("Red Card", "").replace("—", "").strip()
                 if not jugador_principal or jugador_principal == "Desconocido": 
                     jugador_principal = texto_completo.split(" ")[0]

            # Construcción estructurada del registro
            lista_eventos.append({
                'id_partido': id_partido_hash,
                'fecha': fecha,
                'equipo_rival': rival,
                'resultado': resultado,
                'fase': fase,
                'minuto': minuto_juego,
                'jugador_implicado': jugador_principal,
                'tipo_evento': tipo_incidencia,
                'detalle_accion': detalle_evento,
                'etiqueta_partido': etiqueta_contexto
            })

        return pd.DataFrame(lista_eventos)

    except Exception as e:
        print(f"Error de procesamiento en el archivo {nombre_archivo}: {e}")
        return None

def ejecutar_etl_eventos_champions():
    """
    Orquesta el flujo de extracción, transformación y carga (ETL) de los 
    documentos HTML relativos a la Champions League, generando un modelo 
    tabular estructurado.
    """
    print("--- INICIANDO PROCESO ETL: NORMALIZACIÓN DE EVENTOS (CHAMPIONS LEAGUE) ---")
    
    if not os.path.exists(DIR_ENTRADA):
        print(f"Error crítico: Directorio de entrada inaccesible o inexistente: {DIR_ENTRADA}")
        return

    # Exploración recursiva del directorio para localizar documentos HTML
    archivos_objetivo = []
    for raiz, directorios, ficheros in os.walk(DIR_ENTRADA):
        for fichero in ficheros:
            if fichero.endswith(".html"):
                archivos_objetivo.append(os.path.join(raiz, fichero))

    print(f"Info: Documentos detectados en cola de procesamiento: {len(archivos_objetivo)}")
    
    lista_dataframes_procesados = []
    for archivo in archivos_objetivo:
        df_partido = procesar_timeline_eventos(archivo)
        if df_partido is not None:
            # Validación simple de metadatos extraídos
            fase_detectada = df_partido['fase'].iloc[0] if not df_partido.empty else "N/A"
            print(f"Completado: {os.path.basename(archivo)} | Fase: {fase_detectada} | Extracciones: {len(df_partido)}")
            lista_dataframes_procesados.append(df_partido)
    
    # Consolidación estructural de los DataFrames temporales
    if lista_dataframes_procesados:
        df_consolidado_final = pd.concat(lista_dataframes_procesados, ignore_index=True)
        
        # Definición explícita del orden de las columnas analíticas
        columnas_ordenadas = [
            'id_partido', 'fecha', 'equipo_rival', 'resultado', 'fase', 'minuto', 
            'jugador_implicado', 'tipo_evento', 'detalle_accion', 'etiqueta_partido'
        ]
        
        df_consolidado_final = df_consolidado_final[columnas_ordenadas]
        
        # Persistencia en formato CSV asegurando codificación para caracteres especiales
        os.makedirs(os.path.dirname(RUTA_SALIDA), exist_ok=True)
        df_consolidado_final.to_csv(RUTA_SALIDA, index=False, encoding='utf-8-sig')
        print(f"\nProceso finalizado exitosamente. Dataset maestro exportado a: {RUTA_SALIDA}")
    else:
        print("\nError: Fallo en la generación del dataset. Ausencia de datos válidos estructurados.")

if __name__ == "__main__":
    ejecutar_etl_eventos_champions()