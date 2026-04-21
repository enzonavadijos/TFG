import pandas as pd

# 1. Rutas
ruta_laliga = r"C:\Users\enson\Desktop\TFG\ETL\CSV\LaLiga\stats_laliga.csv"
ruta_champions = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Champions League\stats_champions.csv"
ruta_salida = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Dim_Nacionalidades.csv"

try:
    # 2. Leer datos existentes
    df_liga = pd.read_csv(ruta_laliga, usecols=['nation'])
    df_champ = pd.read_csv(ruta_champions, usecols=['nation'])
    df_naciones = pd.concat([df_liga, df_champ]).dropna().drop_duplicates()

    # 3. LISTA DE SEGURIDAD (Inyectamos los países de tus capturas para que NO falten)
    codigos_encontrados = df_naciones['nation'].astype(str).str.strip().str.split(' ').str[-1].str.upper().tolist()
    
    captura_champions = [
        'BE', 'BG', 'BY', 'CH', 'CY', 'CZ', 'DE', 'DK', 'ENG', 'ES', 'ESP', 
        'FR', 'GR', 'HU', 'IT', 'NL', 'PL', 'PT', 'RS', 'RU', 'SCT', 'SK', 'UA'
    ]
    todos_los_codigos = list(set(codigos_encontrados + captura_champions))

    # 4. MAPEO MAESTRO (Conversión a 3 letras FIFA/StatsBomb)
    mapeo_estandar = {
        'BE': 'BEL', 'BG': 'BUL', 'BY': 'BLR', 'CH': 'SUI', 'CY': 'CYP', 'CZ': 'CZE',
        'DE': 'GER', 'DK': 'DEN', 'ENG': 'ENG', 'ES': 'ESP', 'ESP': 'ESP', 'FR': 'FRA',
        'GR': 'GRE', 'HU': 'HUN', 'IT': 'ITA', 'NL': 'NED', 'PL': 'POL', 'PT': 'POR',
        'RS': 'SRB', 'RU': 'RUS', 'SCT': 'SCO', 'SK': 'SVK', 'UA': 'UKR',
        'AR': 'ARG', 'BR': 'BRA', 'CL': 'CHI', 'CO': 'COL', 'UY': 'URU', 'MX': 'MEX'
    }

    # 5. Construir el DataFrame Final
    df_final = pd.DataFrame({'Codigo_Crudo': todos_los_codigos})
    
    # Filtramos la palabra 'NATION' por si acaso
    df_final = df_final[df_final['Codigo_Crudo'] != 'NATION']
    
    # Aplicamos el mapeo
    df_final['Codigo'] = df_final['Codigo_Crudo'].map(mapeo_estandar).fillna(df_final['Codigo_Crudo'])
    
    # Limpiamos duplicados y ordenamos alfabéticamente
    df_dim = pd.DataFrame({'Codigo': df_final['Codigo'].unique()}).sort_values('Codigo').reset_index(drop=True)

    # 6. ID 
    df_dim.insert(0, 'ID_Nacion', range(1, len(df_dim) + 1))
    
    # 7. TRADUCTOR COMPLETO (¡Aquí estaban los que faltaban!)
    traductor = {
        'ARG': 'Argentina', 'ESP': 'España', 'BRA': 'Brasil', 'FRA': 'Francia',
        'NED': 'Países Bajos', 'POR': 'Portugal', 'GER': 'Alemania', 'ENG': 'Inglaterra',
        'CMR': 'Camerún', 'SWE': 'Suecia', 'URU': 'Uruguay', 'CIV': 'Costa de Marfil',
        'CRO': 'Croacia', 'DEN': 'Dinamarca', 'POL': 'Polonia', 'CHI': 'Chile',
        'MEX': 'México', 'USA': 'Estados Unidos', 'ITA': 'Italia', 'BEL': 'Bélgica',
        'SEN': 'Senegal', 'MLI': 'Malí', 'GHA': 'Ghana', 'MAR': 'Marruecos',
        'TUR': 'Turquía', 'ISL': 'Islandia', 'BIH': 'Bosnia y Herzegovina',
        'UKR': 'Ucrania', 'AUT': 'Austria', 'COL': 'Colombia', 'VEN': 'Venezuela',
        'WAL': 'Gales', 'SCO': 'Escocia', 'SUI': 'Suiza', 'SRB': 'Serbia',
        'JPN': 'Japón', 'KOR': 'Corea del Sur', 'GRE': 'Grecia', 'CZE': 'República Checa',
        'BUL': 'Bulgaria', 'SVK': 'Eslovaquia', 'CYP': 'Chipre', 'RUS': 'Rusia',
        'HUN': 'Hungría', 'BLR': 'Bielorrusia', 'ROU': 'Rumanía', 'NOR': 'Noruega',
        'ALB': 'Albania', 'GUI': 'Guinea', 'GAB': 'Gabón', 'MNE': 'Montenegro',
        'GLP': 'Guadalupe', 'PAR': 'Paraguay', 'PER': 'Perú', 'FIN': 'Finlandia',
        'IRL': 'Irlanda', 'DOM': 'República Dominicana', 'ALG': 'Argelia', 'EGY': 'Egipto'
    }

    # Asignar nombres
    df_dim['Pais'] = df_dim['Codigo'].map(traductor).fillna(df_dim['Codigo'] + ' (Revisar)')

    # 8. Guardar
    df_dim.to_csv(ruta_salida, index=False, encoding='utf-8')
    print(f"✅ ¡Hecho! {len(df_dim)} países creados.")
    
    # Comprobación de seguridad en la consola
    revisar = df_dim[df_dim['Pais'].str.contains('Revisar')]
    if not revisar.empty:
        print("\n⚠️ Aún faltan por traducir estos códigos:")
        print(revisar)
    else:
        print("🎉 ¡Ningún país requiere revisión! Todos mapeados al 100%.")

except Exception as e:
    print(f"❌ Error: {e}")