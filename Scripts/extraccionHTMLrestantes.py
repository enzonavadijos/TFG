import os
import pandas as pd
from bs4 import BeautifulSoup
import re
import warnings
warnings.filterwarnings("ignore") # Para que no molesten avisos de Pandas

# --- RUTAS ---
CARPETA_BASE = r"C:\Users\enson\Desktop\TFG\ETL"
carpeta_html = os.path.join(CARPETA_BASE, "HTML_Partidos")
ruta_partidos = os.path.join(CARPETA_BASE, "CSV", "Fact_Tactica_Avanzada.csv")
ruta_jugadores = os.path.join(CARPETA_BASE, "CSV", "Fact_Estadisticas_Jugadores_RAW.csv")

def excavadora_nivel_dios():
    print("--- 🚜 INICIANDO EXCAVADORA NIVEL DIOS ---")
    
    archivos = [f for f in os.listdir(carpeta_html) if f.endswith('.html')]
    print(f"📂 Procesando {len(archivos)} partidos locales. Agárrate que esto va rápido...\n")
    
    datos_partidos = []
    datos_jugadores = []
    
    for archivo in archivos:
        ruta_completa = os.path.join(carpeta_html, archivo)
        
        try:
            partes = archivo.replace(".html", "").split("_", 2)
            id_partido = partes[0]
            fecha = partes[1]
            rival = partes[2]
        except:
            continue
            
        try:
            with open(ruta_completa, 'r', encoding='utf-8') as f:
                html = f.read()
                
            soup = BeautifulSoup(html, 'html.parser')
            
            # --- 1. INFO TÁCTICA Y POSESIÓN ---
            entrenador_barca = "Desconocido"
            posesion_barca = None
            formacion_barca = "Desconocida"
            
            scorebox = soup.find('div', class_='scorebox')
            if scorebox:
                managers = scorebox.find_all('div', class_='datapoint')
                for div in managers:
                    texto = div.text
                    if 'Manager' in texto or 'Entrenador' in texto:
                        limpio = texto.replace('Manager:', '').replace('Entrenador:', '').strip()
                        nombres_barca = ['Xavi', 'Koeman', 'Rijkaard', 'Guardiola', 'Flick', 'Martino', 'Valverde', 'Setién', 'Enrique', 'Vilanova', 'Roura', 'Sergi']
                        if any(n in limpio for n in nombres_barca):
                            entrenador_barca = limpio

            tabla_stats = soup.find('div', id='team_stats')
            if tabla_stats:
                for fila in tabla_stats.find_all('tr'):
                    if 'Possession' in fila.text or 'Posesión' in fila.text:
                        nums = re.findall(r'\d+%', fila.text)
                        if len(nums) >= 2:
                            posesion_barca = f"{nums[0]} - {nums[1]}"

            # --- 2. ALINEACIONES (Titular/Suplente) ---
            lineups = soup.find_all('div', class_='lineup')
            dicc_titulares = {} # Para saber quién fue titular
            dicc_posiciones = {} # Posición que jugó ese día
            
            for lineup in lineups:
                header = lineup.find('th')
                if header and 'Barcelona' in header.text:
                    match_formacion = re.search(r'\(([\d-]+)\)', header.text)
                    if match_formacion:
                        formacion_barca = match_formacion.group(1)
                        
                    es_titular = 1
                    for fila in lineup.find_all('tr')[1:]:
                        if fila.find('td', class_='spacer') or 'Bench' in fila.text or 'Banquillo' in fila.text:
                            es_titular = 0
                            continue
                            
                        enlace = fila.find('a')
                        if enlace:
                            nombre = enlace.text.strip()
                            dicc_titulares[nombre] = es_titular
                            
                            # Intentar sacar la posición si viene en la tabla de alineación
                            pos_tds = fila.find_all('td')
                            if len(pos_tds) > 1:
                                dicc_posiciones[nombre] = pos_tds[1].text.strip()

            # --- 3. ESTADÍSTICAS AVANZADAS (Usando Pandas para leer las tablas del HTML) ---
            tablas_df = pd.read_html(html)
            stats_encontradas = False
            
            for df_tabla in tablas_df:
                if isinstance(df_tabla.columns, pd.MultiIndex):
                    columnas = [col[1] for col in df_tabla.columns]
                    df_tabla.columns = columnas
                else:
                    columnas = df_tabla.columns.tolist()
                    
                # Buscar tabla que tenga "Player" y comprobar si es la del Barça
                if 'Player' in columnas or 'Jugador' in columnas:
                    nombres_tabla = df_tabla.iloc[:, 0].astype(str).tolist()
                    # Si al menos 3 jugadores de nuestro diccionario están en esta tabla, es la del Barça
                    coincidencias = sum(1 for n in nombres_tabla if n in dicc_titulares)
                    
                    if coincidencias >= 3:
                        stats_encontradas = True
                        for _, fila_df in df_tabla.iterrows():
                            jugador = str(fila_df.iloc[0])
                            if jugador == 'nan' or 'Players' in jugador or 'Jugadores' in jugador:
                                continue
                            
                            # Extraemos datos, poniendo 0 si no existen en esa época
                            minutos = fila_df.get('Min', 0)
                            goles = fila_df.get('Gls', 0)
                            asistencias = fila_df.get('Ast', 0)
                            
                            # Cuidado con tarjetas y xG, que a veces cambian de nombre o no existen
                            amarillas = fila_df.get('CrdY', 0) if 'CrdY' in columnas else 0
                            rojas = fila_df.get('CrdR', 0) if 'CrdR' in columnas else 0
                            xg = fila_df.get('xG', 0) if 'xG' in columnas else None
                            
                            datos_jugadores.append({
                                'ID_Partido': id_partido,
                                'Jugador': jugador,
                                'Posicion_Partido': dicc_posiciones.get(jugador, ""),
                                'Titular': dicc_titulares.get(jugador, 0),
                                'Minutos': minutos,
                                'Goles': goles,
                                'Asistencias': asistencias,
                                'Amarillas': amarillas,
                                'Rojas': rojas,
                                'xG': xg
                            })
                        break # Ya procesamos la tabla del Barça, salimos del bucle de tablas
            
            # Si FBref no tenía tabla de estadísticas detallada (partidos muy antiguos), guardamos lo básico
            if not stats_encontradas:
                for jugador, es_titular in dicc_titulares.items():
                    datos_jugadores.append({
                        'ID_Partido': id_partido,
                        'Jugador': jugador,
                        'Posicion_Partido': dicc_posiciones.get(jugador, ""),
                        'Titular': es_titular,
                        'Minutos': None, 'Goles': None, 'Asistencias': None,
                        'Amarillas': None, 'Rojas': None, 'xG': None
                    })

            # Guardar la fila del partido
            datos_partidos.append({
                'ID_Partido': id_partido,
                'Fecha': fecha,
                'Rival': rival,
                'Entrenador': entrenador_barca,
                'Formacion': formacion_barca,
                'Posesion_Bruta': posesion_barca
            })
            
        except Exception as e:
            pass # Ignoramos errores puntuales para que no pare la máquina

    df_partidos = pd.DataFrame(datos_partidos)
    df_jugadores = pd.DataFrame(datos_jugadores)
    
    df_partidos.to_csv(ruta_partidos, index=False, encoding='utf-8-sig')
    df_jugadores.to_csv(ruta_jugadores, index=False, encoding='utf-8-sig')
    
    print(f"📊 Partidos analizados: {len(df_partidos)}")
    print(f"🏃‍♂️ Estadísticas de jugadores extraídas: {len(df_jugadores)}")
    print(f"📍 Archivos limpios en tu carpeta CSV.")

if __name__ == "__main__":
    excavadora_nivel_dios()