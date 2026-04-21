import pandas as pd

print("Construyendo la Dimensión de Temporadas (Palmarés Histórico Transparente)...")

# Diccionario maestro con nombres de columnas directos y limpios
historial = [
    {"Temporada": "2003-2004", "LaLiga": 2, "Champions_League": "No participó", "Copa_del_Rey": "Cuartos", "Supercopa_Espana": "No participó", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 0},
    {"Temporada": "2004-2005", "LaLiga": 1, "Champions_League": "Octavos", "Copa_del_Rey": "Treintaidosavos", "Supercopa_Espana": "No participó", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 1},
    {"Temporada": "2005-2006", "LaLiga": 1, "Champions_League": "Campeón", "Copa_del_Rey": "Cuartos", "Supercopa_Espana": "Campeón", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 3},
    {"Temporada": "2006-2007", "LaLiga": 2, "Champions_League": "Octavos", "Copa_del_Rey": "Semifinales", "Supercopa_Espana": "Campeón", "Supercopa_Europa": "Subcampeón", "Mundial_Clubes": "Subcampeón", "Titulos_Totales": 1},
    {"Temporada": "2007-2008", "LaLiga": 3, "Champions_League": "Semifinales", "Copa_del_Rey": "Semifinales", "Supercopa_Espana": "No participó", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 0},
    
    # --- SEXTETE: Año 2009 ---
    {"Temporada": "2008-2009", "LaLiga": 1, "Champions_League": "Campeón", "Copa_del_Rey": "Campeón", "Supercopa_Espana": "No participó", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 3},
    {"Temporada": "2009-2010", "LaLiga": 1, "Champions_League": "Semifinales", "Copa_del_Rey": "Octavos", "Supercopa_Espana": "Campeón", "Supercopa_Europa": "Campeón", "Mundial_Clubes": "Campeón", "Titulos_Totales": 4},
    
    {"Temporada": "2010-2011", "LaLiga": 1, "Champions_League": "Campeón", "Copa_del_Rey": "Subcampeón", "Supercopa_Espana": "Campeón", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 3},
    {"Temporada": "2011-2012", "LaLiga": 2, "Champions_League": "Semifinales", "Copa_del_Rey": "Campeón", "Supercopa_Espana": "Campeón", "Supercopa_Europa": "Campeón", "Mundial_Clubes": "Campeón", "Titulos_Totales": 4},
    {"Temporada": "2012-2013", "LaLiga": 1, "Champions_League": "Semifinales", "Copa_del_Rey": "Semifinales", "Supercopa_Espana": "Subcampeón", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 1},
    {"Temporada": "2013-2014", "LaLiga": 2, "Champions_League": "Cuartos", "Copa_del_Rey": "Subcampeón", "Supercopa_Espana": "Campeón", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 1},
    {"Temporada": "2014-2015", "LaLiga": 1, "Champions_League": "Campeón", "Copa_del_Rey": "Campeón", "Supercopa_Espana": "No participó", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 3},
    {"Temporada": "2015-2016", "LaLiga": 1, "Champions_League": "Cuartos", "Copa_del_Rey": "Campeón", "Supercopa_Espana": "Subcampeón", "Supercopa_Europa": "Campeón", "Mundial_Clubes": "Campeón", "Titulos_Totales": 4},
    {"Temporada": "2016-2017", "LaLiga": 2, "Champions_League": "Cuartos", "Copa_del_Rey": "Campeón", "Supercopa_Espana": "Campeón", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 2},
    {"Temporada": "2017-2018", "LaLiga": 1, "Champions_League": "Cuartos", "Copa_del_Rey": "Campeón", "Supercopa_Espana": "Subcampeón", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 2},
    {"Temporada": "2018-2019", "LaLiga": 1, "Champions_League": "Semifinales", "Copa_del_Rey": "Subcampeón", "Supercopa_Espana": "Campeón", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 2},
    {"Temporada": "2019-2020", "LaLiga": 2, "Champions_League": "Cuartos", "Copa_del_Rey": "Cuartos", "Supercopa_Espana": "Semifinales", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 0},
    {"Temporada": "2020-2021", "LaLiga": 3, "Champions_League": "Octavos", "Copa_del_Rey": "Campeón", "Supercopa_Espana": "Subcampeón", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 1},
    {"Temporada": "2021-2022", "LaLiga": 2, "Champions_League": "Fase de Grupos", "Copa_del_Rey": "Octavos", "Supercopa_Espana": "Semifinales", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 0},
    {"Temporada": "2022-2023", "LaLiga": 1, "Champions_League": "Fase de Grupos", "Copa_del_Rey": "Semifinales", "Supercopa_Espana": "Campeón", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 2},
    {"Temporada": "2023-2024", "LaLiga": 2, "Champions_League": "Cuartos", "Copa_del_Rey": "Cuartos", "Supercopa_Espana": "Subcampeón", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 0},
    {"Temporada": "2024-2025", "LaLiga": 1, "Champions_League": "Semifinales", "Copa_del_Rey": "Campeón", "Supercopa_Espana": "Campeón", "Supercopa_Europa": "No participó", "Mundial_Clubes": "No participó", "Titulos_Totales": 3}
]

# Crear el DataFrame
df_temporadas = pd.DataFrame(historial)

# Guardar como CSV limpio y listo para Power BI
ruta_archivo = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Dim_Titulos.csv"
df_temporadas.to_csv(ruta_archivo, index=False, encoding='utf-8-sig')

print(f"¡Éxito! Archivo guardado como: {ruta_archivo}")