import pandas as pd
import os

# --- RUTAS ---
CARPETA_BASE = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
ruta_tactica = os.path.join(CARPETA_BASE, "Fact_Tactica_Avanzada.csv")
ruta_sb = os.path.join(CARPETA_BASE, "Fact_Tacticas_Oficiales_SB.csv")

def sanar_formaciones():
    print("--- 🩺 INICIANDO CIRUGÍA DE FORMACIONES ---")
    
    # 1. Leer los dos archivos
    df_tactica = pd.read_csv(ruta_tactica)
    df_sb = pd.read_csv(ruta_sb)
    
    desconocidas_antes = len(df_tactica[df_tactica['Formacion'] == 'Desconocida'])
    print(f"⚠️ Formaciones 'Desconocida' ANTES del cruce: {desconocidas_antes}")
    
    # 2. Hacemos el cruce (Merge) usando la FECHA como llave maestra
    df_merged = df_tactica.merge(
        df_sb[['fecha', 'formacion_oficial']], 
        left_on='Fecha', 
        right_on='fecha', 
        how='left'
    )
    
    # 3. LA REGLA QUE ME HAS PEDIDO: 
    # Solo cambiamos si pone "Desconocida" en el CSV 1 Y hay algo escrito en el CSV 2
    mascara = (df_merged['Formacion'] == 'Desconocida') & (df_merged['formacion_oficial'].notna())
    df_merged.loc[mascara, 'Formacion'] = df_merged.loc[mascara, 'formacion_oficial']
    
    # 4. Limpiamos las columnas de StatsBomb que ya no nos sirven (ya hemos copiado el dato)
    df_merged = df_merged.drop(columns=['fecha', 'formacion_oficial'])
    
    desconocidas_despues = len(df_merged[df_merged['Formacion'] == 'Desconocida'])
    recuperadas = desconocidas_antes - desconocidas_despues
    
    print(f"✅ Formaciones 'Desconocida' DESPUÉS del cruce: {desconocidas_despues}")
    print(f"🎉 ¡Has recuperado y sobrescrito {recuperadas} formaciones históricas!")
    
    # 5. Sobrescribir el archivo original para que Power BI lo lea limpio
    df_merged.to_csv(ruta_tactica, index=False, encoding='utf-8-sig')
    print("📍 Archivo 'Fact_Tactica_Avanzada.csv' curado y sobrescrito con éxito.")

if __name__ == "__main__":
    sanar_formaciones()