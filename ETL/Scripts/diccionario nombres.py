import pandas as pd

# Rutas exactas
ruta_dat2 = r"C:\Users\enson\Documents\dat2.csv"
ruta_salida = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Diccionario_Nombres.csv"

# Leemos con latin1
df_short = pd.read_csv(ruta_dat2, encoding='latin1')
df_short = df_short.drop_duplicates(subset=['Jugador']).dropna(subset=['Jugador'])

# 1. El diccionario normal (los que funcionan a la primera)
diccionario_normal = {
    "Abel Ruiz": "Abel Ruiz Ortega",
    "Adriano": "Adriano Correia Claro",
    "Aleix Vidal": "Aleix Vidal Parreu",
    "Álex Collado": "Álex Collado Gutiérrez",
    "Alexandre Song": "Alexandre Dimitri Song-Billong",
    "Alexis Sánchez": "Alexis Alejandro Sánchez Sánchez",
    "Alexander Hleb": "Aliaksandr Hleb",
    "Deco": "Anderson Luís de Souza",
    "André Gomes": "André Filipe Tavares Gomes",
    "Andrés Iniesta": "Andrés Iniesta Luján",
    "Andreu Fontàs": "Andreu Fontàs Prat",
    "Ansu Fati": "Anssumane Fati",
    "Antoine Griezmann": "Antoine Griezmann",
    "Arda Turan": "Arda Turan",
    "Arthur Melo": "Arthur Henrique Ramos de Oliveira Melo",
    "Arturo Vidal": "Arturo Erasmo Vidal Pardo",
    "Carles Aleñá": "Carles Aleña Castillo",
    "Carles Pérez": "Carles Pérez Sayol",
    "Carles Puyol": "Carles Puyol i Saforcada",
    "Claudio Bravo": "Claudio Andrés Bravo Muñoz",
    "Clément Lenglet": "Clément Lenglet",
    "Cristian Tello": "Cristian Tello Herrera",
    "Damià Abella": "Damià Abella Pérez",
    "Dani Alves": "Daniel Alves da Silva",
    "David Villa": "David Villa Sánchez",
    "Denis Suárez": "Denis Suárez Fernández",
    "Dmytro Chygrynskiy": "Dmytro Chygrynskiy",
    "Douglas": "Douglas Pereira dos Santos",
    "Eiður Guðjohnsen": "Eiður Smári Guðjohnsen",
    "Éric Abidal": "Eric-Sylvain Bilal Abidal",
    "Fernando Navarro": "Fernando Navarro i Corbacho",
    "Cesc Fàbregas": "Francesc Fàbregas i Soler",
    "Paco Alcácer": "Francisco Alcácer García",
    "Frenkie de Jong": "Frenkie de Jong",
    "Gabriel Milito": "Gabriel Alejandro Milito",
    "Gabri García": "Gabriel Francisco García de la Torre",
    "Gerard Deulofeu": "Gerard Deulofeu Lázaro",
    "Gerard Gumbau": "Gerard Gumbau Garriga",
    "Gerard Piqué": "Gerard Piqué Bernabéu",
    "Gianluca Zambrotta": "Gianluca Zambrotta",
    "Giovani dos Santos": "Giovani dos Santos Ramírez",
    "Giovanni van Bronckhorst": "Giovanni van Bronckhorst",
    "Yaya Touré": "Gnégnéri Yaya Touré",
    "Junior Firpo": "Héctor Junior Firpo Adames",
    "Henrik Larsson": "Henrik Larsson",
    "Ibrahim Afellay": "Ibrahim Afellay",
    "Jasper Cillessen": "Jasper Cillessen",
    "Javier Mascherano": "Javier Alejandro Mascherano",
    "Jean Marie Dongou": "Jean Marie Dongou Tsafack",
    "Jean-Clair Todibo": "Jean-Clair Todibo",
    "Jeffrén Suárez": "Jeffren Isaac Suárez Bermúdez",
    "Jérémy Mathieu": "Jérémy Mathieu",
    "Jonathan dos Santos": "Jonathan dos Santos Ramírez",
    "Jordi Alba": "Jordi Alba Ramos",
    "Jordi Masip": "Jordi Masip López",
    "Edmílson": "José Edmílson Gomes de Moraes",
    "José Manuel Pinto": "José Manuel Pinto Colorado",
    "José Manuel Rueda": "José Manuel Rueda Sampedro",
    "Martín Cáceres": "José Martín Cáceres Silva",
    "Paulinho": "José Paulo Bezzera Maciel Júnior",
    "Isaac Cuenca": "Juan Isaac Cuenca López",
    "Juliano Belletti": "Juliano Haus Belletti",
    "Kevin-Prince Boateng": "Kevin-Prince Boateng",
    "Lilian Thuram": "Lilian Thuram",
    "Lionel Messi": "Lionel Andrés Messi Cuccittini",
    "Lucas Digne": "Lucas Digne",
    "Ludovic Giuly": "Ludovic Giuly",
    "Luis Suárez": "Luis Alberto Suárez Díaz",
    "Malcom": "Malcom Filipe Silva de Oliveira",
    "Nolito": "Manuel Agudo Durán",
    "Marc Bartra": "Marc Bartra Aregall",
    "Marc Muniesa": "Marc Muniesa Martínez",
    "Marc-André ter Stegen": "Marc-André ter Stegen",
    "Mark van Bommel": "Mark van Bommel",
    "Marlon": "Marlon Santos da Silva Barbosa",
    "Martin Braithwaite": "Martin Braithwaite Christensen",
    "Martín Montoya": "Martín Montoya Torralbo",
    "Maxi López": "Maximiliano Gastón López",
    "Maxwell": "Maxwell Scherrer Cabelino Andrade",
    "Neto": "Norberto Murara Neto",
    "Nélson Semedo": "Nélson Cabral Semedo",
    "Oleguer Presas": "Oleguer Presas Renom",
    "Óscar Mingueza": "Óscar Mingueza García",
    "Ousmane Dembélé": "Ousmane Dembélé",
    "Rodri": "Sergio Rodríguez García",
    "Philippe Coutinho": "Philippe Coutinho Correia",
    "Rafinha": "Rafael Alcântara do Nascimento",
    "Rafael Márquez": "Rafael Márquez Álvarez",
    "Gerard Martín": "Ricard Puig Martí",
    "Ronald Araújo": "Ronald Federico Araújo da Silva",
    "Ronaldinho": "Ronaldo de Assis Moreira",
    "Rubén": "Rubén Iván Martínez Andrade",
    "Samuel Eto'o": "Samuel Eto'o Fils",
    "Samuel Umtiti": "Samuel Yves Umtiti",
    "Sandro Ramírez": "Sandro Ramírez Castillo",
    "Santiago Ezquerro": "Santiago Ezquerro Marín",
    "Sergi Roberto": "Sergi Roberto Carnicer",
    "Sergi Samper": "Sergi Samper Montaña",
    "Sergiño Dest": "Sergino Dest",
    "Sergio Busquets": "Sergio Busquets i Burgos",
    "Seydou Keita": "Seydou Kéita",
    "Sylvinho": "Sylvio Mendes Campos Junior",
    "Thiago Alcántara": "Thiago Alcântara do Nascimento",
    "Thiago Motta": "Thiago Motta",
    "Thierry Henry": "Thierry Henry",
    "Thomas Vermaelen": "Thomas Vermaelen",
    "Víctor Sánchez": "Víctor Sánchez Mata",
    "Víctor Valdés": "Víctor Valdés Arribas",
    "Víctor Vázquez": "Víctor Vázquez Solsona",
    "Xavi": "Xavier Hernández Creus",
    "Yerry Mina": "Yerry Fernando Mina González",
    "Pedro": "Pedro Eliezer Rodriguez Ledesma",
    "Pedri": "Pedro González López"
}

# 2. Función infalible para asignar el nombre
def asignar_nombre(nombre_corto):
    nc_lower = str(nombre_corto).lower()
    
    # --- LOS REBELDES (Ignoramos si terminan en ?, ć, o lo que sea) ---
    if "bojan" in nc_lower: return "Bojan Krkíc Pérez"
    if "rakiti" in nc_lower: return "Ivan Rakitić"
    if "pjani" in nc_lower: return "Miralem Pjanić"
    if "ibrahimovi" in nc_lower: return "Zlatan Ibrahimović"
    if "saviola" in nc_lower: return "Javier Pedro Saviola Fernández"
    if "fali" in nc_lower: return "Rafael Romero Serrano"
    if "arnaiz" in nc_lower or "arnáiz" in nc_lower: return "José Manuel Arnáiz Díaz"
    
    # --- EL RESTO DE LA PLANTILLA ---
    return diccionario_normal.get(nombre_corto, "")

# 3. Aplicamos la regla y guardamos
df_short['Nombre_Completo'] = df_short['Jugador'].apply(asignar_nombre)
df_short.to_csv(ruta_salida, index=False, encoding='utf-8-sig')

print("¡AHORA SÍ! Diccionario perfecto guardado en:", ruta_salida)