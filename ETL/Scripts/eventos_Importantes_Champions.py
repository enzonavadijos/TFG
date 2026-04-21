import pandas as pd
import os
import re
import zlib
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN DEL ENTORNO ---
INPUT_FOLDER = r"C:\Users\enson\Desktop\TFG\HTML_Champions\Partidos a analizar (Campeones_o_Semis)"
OUTPUT_FILE = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Champions League\eventos_champions_importantes.csv"

def limpiar_comentarios_html(html_content):
    # Preprocesamiento: Elimina comentarios para exponer datos ocultos
    return html_content.replace("", "")

def limpiar_fecha_para_powerbi(fecha_raw):
    """
    Función de limpieza estricta para garantizar que Power BI reconozca la fecha.
    Entrada: "Saturday April 10, 2010 El Clásico (Leg 1)"
    Salida:  "Saturday April 10, 2010"
    """
    if not isinstance(fecha_raw, str):
        return ""
        
    # 1. Eliminar cualquier cosa entre paréntesis (ej: "(Leg 1)", "(Extra Time)")
    fecha_limpia = re.sub(r'\s*\(.*?\)', '', fecha_raw)
    
    # 2. Eliminar "ElClasico", "El Clásico" o variantes
    fecha_limpia = re.sub(r'El\s*Cl[áa]sico', '', fecha_limpia, flags=re.IGNORECASE)
    
    # 3. Eliminar posibles guiones o separadores raros al final
    fecha_limpia = fecha_limpia.replace("–", "").replace("-", "")
    
    # 4. Quitar espacios dobles que hayan podido quedar
    return " ".join(fecha_limpia.split())

def detectar_fase(soup):
    # Algoritmo de detección de fase de competición
    try:
        scorebox = soup.find("div", class_="scorebox")
        if not scorebox:
            return "Fase Desconocida"
        
        texto_cabecera = scorebox.get_text().lower()

        # Jerarquía de detección
        if "final" in texto_cabecera and "quarter" not in texto_cabecera and "semi" not in texto_cabecera and "1/8" not in texto_cabecera:
            return "Final"
        elif "semi-finals" in texto_cabecera or "semi-final" in texto_cabecera:
            return "Semifinales"
        elif "quarter-finals" in texto_cabecera or "quarter-final" in texto_cabecera:
            return "Cuartos de Final"
        elif "round of 16" in texto_cabecera or "octavos" in texto_cabecera:
            return "Octavos de Final"
        elif "group stage" in texto_cabecera:
            return "Fase de Grupos"
        else:
            return "Fase Eliminatoria" 
            
    except:
        return "Fase Desconocida"

def extraer_info_cabecera(soup):
    rival = "Desconocido"
    fecha = "Desconocida"
    resultado = "Unknown"
    
    # 1. Extracción de Rival y Fecha
    title = soup.title.string if soup.title else ""
    if "vs." in title:
        parts = title.split("vs.")
        if "Barcelona" in parts[0]: 
            rival = parts[1].split("Match Report")[0].strip()
        else: 
            rival = parts[0].strip()
        
        date_match = re.search(r'Match Report – (.+)', title)
        if date_match:
            fecha_cruda = date_match.group(1).split("|")[0].strip()
            # APLICAMOS LA NUEVA LIMPIEZA
            fecha = limpiar_fecha_para_powerbi(fecha_cruda)

    # 2. Extracción de Resultado
    try:
        scorebox = soup.find("div", class_="scorebox")
        if scorebox:
            scores = scorebox.find_all("div", class_="score")
            if len(scores) >= 2:
                res_local = scores[0].get_text(strip=True)
                res_visit = scores[1].get_text(strip=True)
                resultado = f"{res_local}-{res_visit}"
    except:
        pass

    # 3. Detección de Fase
    fase = detectar_fase(soup)

    return fecha, rival, resultado, fase

def generar_id_numerico(fecha, rival):
    # Generación de Primary Key numérica (Hash CRC32)
    firma = f"{fecha}_{rival}"
    return zlib.crc32(firma.encode('utf-8'))

def procesar_eventos(filepath):
    filename = os.path.basename(filepath)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_html = f.read()
        
        # Parseo del DOM
        clean_html = limpiar_comentarios_html(raw_html)
        soup = BeautifulSoup(clean_html, "html.parser")
        
        # Extracción de Metadatos
        fecha, rival, resultado, fase = extraer_info_cabecera(soup)
        id_partido = generar_id_numerico(fecha, rival)
        
        # Etiqueta para visualización
        etiqueta = f"{fase} vs {rival} ({fecha})"

        eventos = []
        events_div = soup.find("div", id="events_wrap")
        
        if not events_div:
            return None

        # Iteración de Eventos
        for event in events_div.find_all("div", class_="event"):
            full_text = event.get_text(" ", strip=True)
            
            # Minuto del evento
            match_time = re.search(r"(\d+(?:\+\d+)?)\’", full_text)
            minuto = match_time.group(1) if match_time else "0"
            
            # Tipificación del evento
            tipo_evento = "Otro"
            icono = str(event).lower()
            if "score" in icono or "goal" in icono: tipo_evento = "Gol"
            elif "card" in icono:
                if "red" in icono or "yellow_red" in icono: tipo_evento = "Tarjeta Roja"
                else: tipo_evento = "Tarjeta Amarilla"
            elif "sub" in icono: tipo_evento = "Sustitución"
            elif "penalty" in icono and "miss" in icono: tipo_evento = "Penalti Fallado"

            # Actores y Detalle
            links = event.find_all("a")
            jugador = "Desconocido"
            detalle = full_text
            
            if match_time: detalle = detalle.replace(match_time.group(0), "").strip()
            
            if len(links) > 0:
                jugador = links[0].get_text()
                detalle = detalle.replace(jugador, "").strip()
                
                if tipo_evento == "Sustitución":
                    if len(links) > 1:
                        sale = links[1].get_text()
                        detalle = f"Entra al campo (Sale {sale})"
                    else:
                        detalle = "Entra desde el banquillo"
                elif tipo_evento == "Gol":
                    detalle = re.sub(r'\d+[:\-]\d+', '', detalle).strip().replace("—", "").strip()
                    if "Assist" in full_text and len(links) > 1:
                        asistente = links[1].get_text()
                        detalle = f"Asistencia de {asistente}"
                    elif "Penalty" in full_text: detalle = "De Penalti"
                    elif "Head" in full_text: detalle = "De Cabeza"
                    elif not detalle: detalle = "Jugada individual"
            elif "Card" in tipo_evento:
                 detalle = re.sub(r'\d+[:\-]\d+', '', detalle).strip()
                 detalle = detalle.replace("Yellow Card", "").replace("Red Card", "").replace("—", "").strip()
                 if not jugador or jugador == "Desconocido": jugador = full_text.split(" ")[0]

            # Construcción del registro
            eventos.append({
                'id_partido': id_partido,
                'fecha': fecha,
                'equipo_rival': rival,
                'resultado': resultado,
                'fase': fase,
                'minuto': minuto,
                'jugador_implicado': jugador,
                'tipo_evento': tipo_evento,
                'detalle_accion': detalle,
                'etiqueta_partido': etiqueta
            })

        return pd.DataFrame(eventos)

    except Exception as e:
        print(f"⚠️ Error procesando archivo {filename}: {e}")
        return None

def main():
    print("Iniciando proceso ETL: Normalización de Eventos Champions...")
    
    if not os.path.exists(INPUT_FOLDER):
        print(f"❌ Ruta de entrada inaccesible: {INPUT_FOLDER}")
        return

    archivos = []
    for root, dirs, files in os.walk(INPUT_FOLDER):
        for file in files:
            if file.endswith(".html"):
                archivos.append(os.path.join(root, file))

    print(f"Archivos en cola de procesamiento: {len(archivos)}")
    
    all_dfs = []
    for archivo in archivos:
        df = procesar_eventos(archivo)
        if df is not None:
            # Validación simple
            fase_actual = df['fase'].iloc[0] if not df.empty else "N/A"
            print(f"   ✅ Procesado: {os.path.basename(archivo)} | Fase: {fase_actual} | Registros: {len(df)}")
            all_dfs.append(df)
    
    if all_dfs:
        df_final = pd.concat(all_dfs, ignore_index=True)
        
        # Selección final de columnas
        cols = ['id_partido', 'fecha', 'equipo_rival', 'resultado', 'fase', 'minuto', 
                'jugador_implicado', 'tipo_evento', 'detalle_accion', 'etiqueta_partido']
        
        df_final = df_final[cols]
        
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        df_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print(f"✅ Dataset generado exitosamente: {OUTPUT_FILE}")
    else:
        print("❌ Fallo en la generación del dataset: No hay datos válidos.")

if __name__ == "__main__":
    main()