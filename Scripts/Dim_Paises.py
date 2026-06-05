import pandas as pd
import os

# --- CONFIGURACIÓN DE RUTAS ---
PATH_LALIGA = r"C:\Users\Enzo\OneDrive\Escritorio\Universidad\TFG\stats_laliga.csv"
PATH_CHAMPIONS = r"C:\Users\Enzo\OneDrive\Escritorio\Universidad\TFG\stats_champions.csv"
PATH_OUTPUT = r"C:\Users\Enzo\OneDrive\Escritorio\Universidad\TFG\Dim_Nacionalidades.csv"

def generar_dimension_nacionalidades():
    """
    Construye la dimensión de nacionalidades extrayendo los códigos de país de los 
    datasets principales. Aplica un mapeo de estandarización para convertir códigos 
    de dos letras al formato internacional FIFA de tres letras, y los traduce al castellano.
    """
    print("--- INICIANDO CONSTRUCCIÓN DE LA DIMENSIÓN DE NACIONALIDADES ---")
    
    try:
        # 1. Extracción de la columna de nacionalidad de las fuentes principales
        df_liga = pd.read_csv(PATH_LALIGA, usecols=['nation'])
        df_champions = pd.read_csv(PATH_CHAMPIONS, usecols=['nation'])
        
        # Consolidación estructural y deduplicación inicial
        df_naciones_consolidadas = pd.concat([df_liga, df_champions]).dropna().drop_duplicates()

        # 2. Limpieza y extracción del código base
        # En la fuente original, el formato suele incluir prefijos (ej. 'es ESP'), 
        # por lo que se aísla el último elemento
        codigos_extraidos = df_naciones_consolidadas['nation'].astype(str).str.strip().str.split(' ').str[-1].str.upper().tolist()
        
        # Lista de contingencia: Inyección de códigos identificados previamente para asegurar exhaustividad
        codigos_contingencia = [
            'BE', 'BG', 'BY', 'CH', 'CY', 'CZ', 'DE', 'DK', 'ENG', 'ES', 'ESP', 
            'FR', 'GR', 'HU', 'IT', 'NL', 'PL', 'PT', 'RS', 'RU', 'SCT', 'SK', 'UA'
        ]
        
        # Unificación de códigos extraídos y de contingencia mediante conjunto (set) para evitar duplicados
        codigos_totales = list(set(codigos_extraidos + codigos_contingencia))

        # 3. Mapeo de estandarización (Conversión de formato de 2 letras a código FIFA/StatsBomb de 3 letras)
        mapeo_estandarizacion = {
            'BE': 'BEL', 'BG': 'BUL', 'BY': 'BLR', 'CH': 'SUI', 'CY': 'CYP', 'CZ': 'CZE',
            'DE': 'GER', 'DK': 'DEN', 'ENG': 'ENG', 'ES': 'ESP', 'ESP': 'ESP', 'FR': 'FRA',
            'GR': 'GRE', 'HU': 'HUN', 'IT': 'ITA', 'NL': 'NED', 'PL': 'POL', 'PT': 'POR',
            'RS': 'SRB', 'RU': 'RUS', 'SCT': 'SCO', 'SK': 'SVK', 'UA': 'UKR',
            'AR': 'ARG', 'BR': 'BRA', 'CL': 'CHI', 'CO': 'COL', 'UY': 'URU', 'MX': 'MEX'
        }

        # 4. Construcción del DataFrame dimensional
        df_dimension = pd.DataFrame({'Codigo_Crudo': codigos_totales})
        
        # Filtro de limpieza para eliminar cabeceras literales erróneas residuales
        df_dimension = df_dimension[df_dimension['Codigo_Crudo'] != 'NATION']
        
        # Aplicación de las reglas de mapeo, conservando el código crudo si no hay coincidencia
        df_dimension['Codigo'] = df_dimension['Codigo_Crudo'].map(mapeo_estandarizacion).fillna(df_dimension['Codigo_Crudo'])
        
        # Deduplicación post-mapeo y ordenamiento alfabético
        df_dimension = pd.DataFrame({'Codigo': df_dimension['Codigo'].unique()}).sort_values('Codigo').reset_index(drop=True)

        # 5. Generación de clave primaria (Primary Key) secuencial
        df_dimension.insert(0, 'ID_Nacion', range(1, len(df_dimension) + 1))
        
        # 6. Traducción de nomenclaturas al castellano
        diccionario_traduccion = {
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

        # Asignación de nombres de país con etiqueta de revisión en caso de códigos no mapeados
        df_dimension['Pais'] = df_dimension['Codigo'].map(diccionario_traduccion).fillna(df_dimension['Codigo'] + ' (Revisar)')

        # 7. Exportación del conjunto de datos
        df_dimension.to_csv(PATH_OUTPUT, index=False, encoding='utf-8')
        print(f"Operación completada: Se ha generado la dimensión con {len(df_dimension)} registros.")
        
        # Validación de integridad post-procesamiento
        registros_pendientes = df_dimension[df_dimension['Pais'].str.contains('Revisar')]
        if not registros_pendientes.empty:
            print("\nAviso: Se han detectado códigos sin traducción asociada en el diccionario maestro:")
            print(registros_pendientes)
        else:
            print("Validación de integridad exitosa: Todos los códigos han sido mapeados y traducidos correctamente.")

    except Exception as e:
        print(f"Error crítico durante la construcción de la dimensión: {e}")

if __name__ == "__main__":
    generar_dimension_nacionalidades()