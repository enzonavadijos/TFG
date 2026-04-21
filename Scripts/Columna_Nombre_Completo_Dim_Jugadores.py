import pandas as pd
import os

# 1. Configuración de Rutas
ruta_entrada = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Dim_Jugadores_Final.csv"
ruta_salida_excel = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Dim_Jugadores_Definitivo.xlsx"

# 2. Diccionario Maestro de Mapeo (Basado en tu lista de LaLiga)
# Este diccionario traduce tus nombres cortos (incluso los que tienen caracteres rotos)
# al nombre largo oficial que aparece en tus archivos.
mapeo_completo = {
    "Abraham GonzÃ¡lez": "Abraham GonzÃ¡lez Casanova", "Adama TraorÃ©": "Adama TraorÃ© Diarra",
    "Albert Jorquera": "Albert Jorquera FortiÃ ", "Alberto BotÃa": "Alberto BotÃ­a Rabasco",
    "Aleix Garrido": "Aleix GarcÃ­a Serrano", "Alejandro Balde": "Alejandro Balde MartÃ­nez",
    "Alexis Olmedo": "Alexis Ruano Delgado", "Alvaro Sanz": "Ãlvaro Sanz CatalÃ¡n",
    "Ander Astralaga": "Ander Murillo GarcÃ­a", "Andrea Orlandi": "Andrea Orlandi",
    "Andres Cuenca": "AndrÃ©s Cuenca Cejudo", "Andreu FontÃ s": "Andreu FontÃ s Prat",
    "AndrÃ©s Iniesta": "AndrÃ©s Iniesta LujÃ¡n", "Ansu Fati": "Anssumane Fati Vieira",
    "Arnau Comas": "Arnau Comas Freixas", "Arnau Tenas": "Arnau Tenas UreÃ±a",
    "Bojan Krki?": "Bojan KrkÃ­c PÃ©rez", "Borja LÃ³pez": "Borja LÃ³pez MenÃ©ndez",
    "Carles AleÃ±Ã¡": "Carles AleÃ±a Castillo", "Carles PÃ©rez": "Carles PÃ©rez Sayol",
    "Cesc FÃ bregas": "Francesc FÃ bregas i Soler", "Chumi": "Juan Brandariz Movilla",
    "Dani Morer": "Daniel Morer Cabrera", "Dani Olmo": "Daniel Olmo Carvajal",
    "Daniel Rodriguez": "Daniel RodrÃ­guez Crespo", "David Costas": "David Costas Cordal",
    "Denis SuÃ¡rez": "Denis SuÃ¡rez FernÃ¡ndez", "Eric GarcÃa": "Eric GarcÃ­a MartrÃ©t",
    "Estanis": "Estanislao Pedrola Fortuny", "Fali": "Rafael JimÃ©nez Jarque",
    "Fermin LÃ³pez": "FermÃ­n LÃ³pez MarÃ­n", "Ferran JutglÃ ": "Ferran JutglÃ  Blanch",
    "FerrÃ¡n Torres": "FerrÃ¡n Torres GarcÃ­a", "Francisco Martos": "Francisco Javier Martos Espigares",
    "Gabri GarcÃa": "Gabriel Francisco GarcÃ­a de la Torre", "Gavi": "Pablo MartÃ­n PÃ¡ez Gavira",
    "Gerard LÃ³pez": "Gerard LÃ³pez SegÃº", "Gerard MartÃn": "Gerard MartÃ­n Langreo",
    "Gerard PiquÃ©": "Gerard PiquÃ© BernabÃ©u", "Guillem Jaime": "Guillem Jaime Serrano",
    "Guillermo Fernandez": "Guillermo FernÃ¡ndez Casino", "HÃ©ctor BellerÃn": "HÃ©ctor BellerÃ­n Moruno",
    "HÃ©ctor Fort": "HÃ©ctor Fort Nou", "IÃ±aki PeÃ±a": "Ignacio PeÃ±a Sotorres",
    "IÃ±igo MartÃnez": "ÃÃ±igo MartÃ­nez Berridi", "Jandro Orellana": "Alejandro Orellana GÃ³mez",
    "JesÃºs Olmo": "JesÃºs Olmo Lozano", "Jokin Ezkieta": "Jokin Ezkieta Mendiburu",
    "Jorge Cuenca": "Jorge Cuenca Barreno", "JosÃ© Arnaiz": "JosÃ© Manuel Arnaiz DÃ­az",
    "JosÃ© Manuel Pinto": "JosÃ© Manuel Pinto Colorado", "JosÃ© Manuel Rueda": "JosÃ© Manuel Rueda Sampedro",
    "Juan CÃ¡mara": "Juan del Carmen CÃ¡mara Mesa", "Juan Miranda": "Juan Miranda GonzÃ¡lez",
    "Kike Saverio": "Javier Enrique Delgado Saverio", "Lamine Yamal": "Lamine Yamal Nasraoui Ebana",
    "Landry FarrÃ©": "Landry FarrÃ©", "Lucas De Vega": "Lucas de Vega Lima",
    "Luis Enrique": "Luis Enrique MartÃ­nez GarcÃ­a", "Luis GarcÃa": "Luis Javier GarcÃ­a Sanz",
    "Marc Bernal": "Marc Bernal Casas", "Marc Casado": "Marc CasadÃ³ Torras",
    "Marc Crosas": "Marc Crosas Luque", "Marc Guiu": "Marc Guiu Paz",
    "Marcos Alonso": "Marcos Alonso Mendoza", "MartÃ Riverola": "MartÃ­ Riverola Bataller",
    "MartÃn Montoya": "MartÃ­n Montoya Torralbo", "Mika MÃ¡rmol": "Mika MÃ¡rmol Medina",
    "Monchu": "RamÃ³n RodrÃ­guez JimÃ©nez", "NicolÃ¡s GonzÃ¡lez": "NicolÃ¡s GonzÃ¡lez Iglesias",
    "Nili": "Francisco JosÃ© Perdomo Borges", "Nolito": "Manuel Agudo DurÃ¡n",
    "Oier OlazÃ¡bal": "Oier OlazÃ¡bal Paredes", "Oriol Busquets": "Oriol Busquets Mas",
    "Oriol Romeu": "Oriol Romeu Vidal", "Pablo Torre": "Pablo Torre Carral",
    "Paco AlcÃ¡cer": "Francisco AlcÃ¡cer GarcÃ­a", "Paco MontaÃ±Ã©s": "Francisco MontaÃ±Ã©s ClaverÃ­as",
    "Pau CubarsÃ": "Pau CubarsÃ­ Paredes", "Pau Prim": "Pau Prim Coma",
    "Pau Victor": "Pau VÃ­ctor Delgado", "Pedri": "Pedro GonzÃ¡lez LÃ³pez",
    "Pitu": "Josep Maria Comadevall Crous", "RamÃ³n MasÃ³": "RamÃ³n MasÃ³ VallmajÃ³",
    "RamÃ³n Ros": "RamÃ³n Ros Badia", "Riqui Puig": "Ricard Puig MartÃ­",
    "Rodri": "Rodrigo RÃ­os Lozano", "Sandro RamÃrez": "Sandro RamÃ­rez Castillo",
    "Sergi Dominguez": "Sergi DomÃ­nguez Viloria", "Sergio Akieme": "Sergio Akieme RodrÃ­guez",
    "Sergio GarcÃa": "Sergio GarcÃ­a de la Fuente", "Sergio SantamarÃa": "Sergio SantamarÃ­a GonzÃ¡lez",
    "Thiago AlcÃ¡ntara": "Thiago AlcÃ¢ntara do Nascimento", "Toni FernÃ¡ndez": "Antonio FernÃ¡ndez Casino",
    "Unai Hernandez": "Unai HernÃ¡ndez Lorenzo", "VÃctor SÃ¡nchez": "VÃ­ctor SÃ¡nchez Mata",
    "VÃctor ValdÃ©s": "VÃ­ctor ValdÃ©s Arribas", "VÃctor VÃ¡zquez": "VÃ­ctor VÃ¡zquez Solsona",
    "Xavi": "Xavier HernÃ¡ndez Creus", "Xavi Torres": "Xavier Torres Buigues",
    "Ãlex Carbonell": "Ãlex Carbonell VallÃ©s", "Ãlex Collado": "Ãlex Collado GutiÃ©rrez",
    "Ãlex Valle": "Ãlex Valle GÃ³mez", "Ãlvaro CortÃ©s": "Ãlvaro CortÃ©s",
    "Ãngel AlarcÃ³n": "Ãngel AlarcÃ³n Galiot", "Ãscar LÃ³pez": "Ã“scar LÃ³pez HernÃ¡ndez",
    "Ãscar Mingueza": "Ã“scar Mingueza GarcÃ­a", "Abde Ezzalzouli": "Abdessamad Ezzalzouli",
    "Alexander Hleb": "Aliaksandr Hleb", "Alexandre Song": "Alexandre Dimitri Song-Billong",
    "Alexis SÃ¡nchez": "Alexis Alejandro SÃ¡nchez SÃ¡nchez", "Andreas Christensen": "Andreas BÃ¸dtker Christensen",
    "AndrÃ© Gomes": "AndrÃ© Miguel Valente Silva", "Chadi Riad": "Chadi Riad Dnanou",
    "ClÃ©ment Lenglet": "ClÃ©ment Lenglet", "Dani Alves": "Daniel Alves da Silva",
    "Deco": "Anderson LuÃ­s de Souza", "Demetrio Albertini": "Demetrio Albertini",
    "Diego Kochen": "Diego Kochen", "Edgar Davids": "Edgar Steven Davids",
    "EdmÃlson": "JosÃ© EdmÃ­lson Gomes de Moraes", "EiÃ°ur GuÃ°johnsen": "EiÃ°ur SmÃ¡ri GuÃ°johnsen",
    "Francisco TrincÃ£o": "Francisco AntÃ³nio Machado Mota de Castro TrincÃ£o", "Franck KessiÃ©": "Franck Yannick KessiÃ©",
    "Ilaix Moriba": "Moriba Kourouma Kourouma", "Ilias Akhomach": "Ilias Akhomach Chakkour",
    "Ivan Rakiti?": "Ivan RakitiÄ‡", "JeffrÃ©n SuÃ¡rez": "JeffrÃ©n Isaac SuÃ¡rez BermÃºdez",
    "JoÃ£o Cancelo": "JoÃ£o Pedro Cavaco Cancelo", "JoÃ£o FÃ©lix": "JoÃ£o FÃ©lix Sequeira",
    "Jules KoundÃ©": "Jules Olivier KoundÃ©", "JÃ©rÃ©my Mathieu": "JÃ©rÃ©my Mathieu",
    "Konrad De La Fuente": "Konrad de la Fuente", "Lazar Carevi?": "Lazar CareviÄ‡",
    "Ludovic Sylvestre": "Ludovic Sylvestre", "Ludovit Reis": "Ludovit Reis",
    "Luis SuÃ¡rez": "Luis Alberto SuÃ¡rez DÃ­az", "Marc Overmars": "Marc Overmars",
    "Marc-AndrÃ© ter Stegen": "Marc-AndrÃ© ter Stegen", "MartÃn CÃ¡ceres": "JosÃ© MartÃ­n CÃ¡ceres Silva",
    "Matheus Fernandes": "Matheus Fernandes Siqueira", "Maxi LÃ³pez": "Maximiliano GastÃ³n LÃ³pez",
    "Memphis": "Memphis Depay", "Michael Reiziger": "Michael Reiziger",
    "Mikayil Ngor Faye": "Mikayil Ngor Faye", "Miralem Pjani?": "Miralem PjaniÄ‡",
    "Moussa WaguÃ©": "Moussa WaguÃ©", "Noah Darvich": "Noah Darvich",
    "NÃ©lson Semedo": "NÃ©lson Cabral Semedo", "Ousmane DembÃ©lÃ©": "Ousmane DembÃ©lÃ©",
    "Patrick Kluivert": "Patrick Kluivert", "Patrik Andersson": "Patrik Jonas Andersson",
    "Paulinho": "JosÃ© Paulo Bezerra Maciel JÃºnior", "Phillip Cocu": "Phillip John William Cocu",
    "Pierre-Emerick Aubameyang": "Pierre-Emerick Emiliano FranÃ§ois Aubameyang", "Player": "Desconocido",
    "Rafael MÃ¡rquez": "Rafael MÃ¡rquez Ãlvarez", "Rafinha": "Rafael AlcÃ¢ntara do Nascimento",
    "Raphinha": "Raphael Dias Belloli", "Rey Manaj": "Rey Manaj",
    "Ricardo Quaresma": "Ricardo Andrade Quaresma Bernardo", "Robert Lewandowski": "Robert Lewandowski",
    "Ronald AraÃºjo": "Ronald Federico AraÃºjo da Silva", "Ronaldinho": "Ronaldo de Assis Moreira",
    "RÃ¼?tÃ¼ ReÃ§ber": "RÃ¼ÅŸtÃ¼ ReÃ§ber", "Samuel Eto'o": "Samuel Eto''o Fils",
    "Santi Ramos Mingo": "Santiago Ramos Mingo", "Sergio AgÃ¼ero": "Sergio Leonel AgÃ¼ero del Castillo",
    "Seydou Keita": "Seydou Keita", "Sylvinho": "Sylvio Mendes Campos Junior",
    "Vitor Roque": "Vitor Hugo Roque Ferreira", "Wilfrid Kaptoum": "Wilfrid Jaures Kaptoum",
    "Wojciech Szcz?sny": "Wojciech SzczÄ™sny", "Yaya TourÃ©": "GnÃ©gnÃ©ri Yaya TourÃ©",
    "Yusuf Demir": "Yusuf Demir", "Zlatan Ibrahimovi?": "Zlatan IbrahimoviÄ‡",
    "Ãron Yaakobishvili": "Ãron Yaakobishvili", "Ãric Abidal": "Ã‰ric Abidal",
    "?lkay GÃ¼ndo?an": "Ãlkay GÃ¼ndoÄŸan"
}

try:
    # 3. Lectura del CSV original
    print("Leyendo archivo original...")
    df = pd.read_csv(ruta_entrada, sep=';', encoding='latin1')
    
    # 4. Creación de la columna con el mapeo oficial
    # Buscamos en el diccionario, si no está dejamos el nombre corto original
    df['Nombre Completo'] = df['Jugador'].map(mapeo_completo).fillna("")

    # 5. Guardado en formato EXCEL (.xlsx)
    # Esto soluciona los problemas de visibilidad y separadores
    print("Generando archivo Excel definitivo...")
    df.to_excel(ruta_salida_excel, index=False)

    print("\n" + "="*40)
    print("¡PROCESO FINALIZADO CON ÉXITO!")
    print(f"Archivo creado: Dim_Jugadores_Definitivo.xlsx")
    print(f"Total filas: {len(df)}")
    print(f"Nombres completados: {df['Nombre Completo'].ne('').sum()}")
    print("="*40)

    # 6. Intentar abrir el archivo automáticamente
    os.startfile(ruta_salida_excel)

except Exception as e:
    print(f"\n❌ ERROR CRÍTICO: {e}")