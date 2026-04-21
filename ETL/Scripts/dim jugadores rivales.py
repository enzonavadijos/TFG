import pandas as pd

# 1. Lista bruta de Champions
texto_champions = """Aaron Hunt
Abdul Kader Keïta
Abou Diaby
Adrien Rabiot
Alan Kasaev
Alan Virginius
Alberto Aquilani
Alberto Gilardino
Aleksandar Katai
Aleksandar Kolarov
Aleksandr Bukharov
Aleksandr Golovin
Aleksandr Ryazantsev
Aleksei Medvedev
Aleksei Vladislavovich Popov
Alessandro Bastoni
Alessandro Costacurta
Alessandro Nesta
Alex
Alex Teixeira
Alexander Bah
Alexandre Pato
Alexandros Tziolis
Álvaro Arbeloa
Álvaro Carreras
Álvaro Morata
Alyaksandr Valadzko
Alyaksandr Yurevich
Anatoliy Tymoshchuk
Anderson
André Almeida
André Schürrle
Andrea Belotti
Andreas Ottl
Andreas Pereira
Andrey Arshavin
Andriy Pyatov
Andriy Shevchenko
Andrzej Niedzielan
Ángel Di María
Anthony Martial
Anthony Šerić
Antonio Candreva
Antônio da Silva
Antonio Nocerino
António Silva
Antonio Valencia
Antonis Petropoulos
Anwar El Ghazi
Arjen Robben
Arkadiusz Milik
Artem Dzyuba
Artem Milevskiy
Arthur Cabral
Asier del Horno
Bacary Sagna
Bakaye Traoré
Barry Robson
Bastian Oczipka
Bastian Schweinsteiger
Benjamín Rollheiser
Beram Kayal
Bertrand Traoré
Betão
Bibras Natkho
Blaise Matuidi
Borja Valero
Brandão
Branislav Ivanović
Bruno César
Bruno Pereirinha
Cacau
Cafú
Caio Henrique Oliveira Silva
Carlão
Carlos Augusto
Carlos Grossmüller
Carlos Martins
Carlos Tevez
César Delgado
Cheikh Niasse
Cherif Ndiaye
Chris Smalling
Christian Bolaños
Christian Lell
Christian Mawissa
Christian Noboa
Christian Obodo
Christian Pander
Ciprian Marica
Clarence Seedorf
Claudemir de Souza
Claudio Pizarro
Cléber Guedes de Lima
Clément Chantôme
Constantinos Charalambides
Cris
Cristian Ansaldi
Cristian Chivu
Cristian Molinaro
Cristiano Ronaldo
Dálcio
DaMarcus Beasley
Dame N'Doye
Damien Plessis
Daniel Jensen
Daniel Schwaab
Daniel Sturridge
Daniele Bonera
Danny da Costa
Darijo Srna
Darren Fletcher
David Abraham
David Beckham
David Di Michele
David Limberský
David Luiz
David Silva
David Weir
Davide Frattesi
Davide Santon
Dejan Stanković
Denílson
Denzel Dumfries
Derlei
Didier Drogba
Diego Milito
Dimitar Berbatov
Dimitris Papadopoulos
Diogo Dalot
Divock Origi
Djamel Mesbah
Donyell Malen
Douglas Costa
Ebrima Colley
Éderson
Edhar Alyakhnovich
Edinson Cavani
Eduardo da Silva
Eduardo Rubio
Egor Prutsev
Eliesse Ben Seghir
Elini Dimoutsos
Emmanuel Adebayor
Emmanuel Eboué
Emmanuel Emenike
Eren Derdiyok
Eric Dier
Erick Gutiérrez
Érik Lamela
Evander Sno
Ezequiel Garay
Ezequiel Lavezzi
Fabian Ernst
Fabinho
Fabio Grosso
Fábio Rochemback
Fábio Santos
Fabrizio Miccoli
Felipe dal Belo
Felix Nmecha
Fernandinho
Fernando
Fernando Llorente
Fernando Marçal
Fernando Meira
Fernando Tissone
Fernando Torres
Filip Ugrinic
Folarin Balogun
Francesco Acerbi
Franck Ribéry
Franco Costanzo
François Clerc
Frank Fahrenhorst
Frank Lampard
František Ševinský
Gaël Clichy
George Ilenikhena
Georginio Wijnaldum
Georgios Samaras
Geremi
Gérson Magrão
Gio Reyna
Giorgio Scalvini
Giorgos Efrem
Giorgos Karagounis
Gökdeniz Karadeniz
Gonzalo Castro
Gregory van der Wiel
Gustavo Manduca
Hakan Çalhanoğlu
Hamit Altıntop
Harry Kane
Hatem Ben Arfa
Heiko Westermann
Hélder Postiga
Henrikh Mkhitaryan
Hernán Crespo
Houssem Aouar
Ilias Kotsios
Ilsinho
Iván Córdoba
Ivan Perišić
Jack Wilshere
Jaïro Riedewald
Jamal Musiala
James Forrest
Jamie Gittens
Jan Vennegoor of Hesselink
Jano Ananidze
Jardel
Javi Martínez
Javier Pastore
Javier Zanetti
Jean Makoun
Jean-Christophe Bahebeck
Jean-Claude Darcheville
Jens Lehmann
Jérémy Ménez
Jérémy Toulalan
Jesse Lingard
Jesús Navas
João Guilherme
João Rêgo
Joe Cole
Joe Gomez
Joël Matip
Joël Veltman
John Obi Mikel
John Terry
Jonas Martin
Jordan Henderson
Jorrit Hendrix
José Antonio Reyes
José Bosingwa
José Luís Vidigal
José Manuel Jurado
José Sosa
Joshua Kimmich
Juan Bernat
Juan Cuadrado
Juárez
Julian Brandt
Julien Duranville
Julien Le Cardinal
Júlio César
Juninho Pernambucano
Jürgen Gjasula
Karim Adeyemi
Karim Bellarabi
Keita Baldé
Kenneth Zohore
Kenny Lala
Kévin Gameiro
Kevin Thomson
Kim Källström
Kingsley Coman
Kirill Aleksiyan
Kirill Kombarov
Konrad Laimer
Kris Commons
Kyle Walker-Peters
Lamine Camara
Lasha Salukvadze
Lassana Diarra
Laurent Koscielny
Laurent Robert
Lautaro Martínez
Leandro Almeida Silva
Leandro Barreiro Martins
Leo Dubois
Leon Goretzka
Leroy Sané
Liédson
Loïc Rémy
Luca Antonini
Lucas Moura
Lucas Tousart
Lúcio
Ludovic Ajorque
Ludovic Magnin
Luisão
Luiz Adriano
Luiz Gustavo
Luka Ilić
Łukasz Łakomy
Luke Shaw
MacBeth Sibaya
Maghnes Akliouche
Mahdi Camara
Maicon Sisenando
Maksim Skavysh
Mama Samba Baldé
Manuel Almunia
Manuel Fernandes
Manuel Fischer
Marcel Augusto Ortolan
Marcel Sabitzer
Marcelo
Marcelo Brozović
Marcelo Martins Moreno
Marco Brescianini
Marco Caneira
Marco Streller
Marco Verratti
Marcos Gelabert
Marcus Thuram
Marek Suchý
Marek Zieńczuk
Marián Čišovský
Mario Balotelli
Mario Gómez
Mario Götze
Mario Pašalić
Marios Antoniades
Mariusz Lewandowski
Mark Wilson
Marko Perović
Marko Simić
Marten de Roon
Martín Demichelis
Martin Fillo
Massimo Ambrosini
Massimo Donati
Mateja Kežman
Mathias Pereira Lage
Mathieu Bodmer
Mathieu Flamini
Mathieu Gorgelin
Matteo Darmian
Matteo Politano
Matteo Ruggeri
Mauro Cantoro
Mauro Icardi
Maximilian Beier
Maximiliano Romero
Maxwel Cornet
M'Baye Niang
McDonald Mariga
Medhi Benatia
Mehdi Taremi
Mesut Özil
Michael Ballack
Michael Carrick
Michael Essien
Michal Ďuriš
Michal Kadlec
Miguel Veloso
Mikaël Silvestre
Mikhail Gordeichuk
Miku
Milan Baroš
Milan Škriniar
Miloš Ninković
Milson
Mladen Krstajić
Mohamed Aly Camara
Moussa Dembélé
Moussa Sissoko
Mykola Ischenko
Nacho Novo
Nani
Nasief Morris
Nemanja Matić
Nemanja Vidić
Nick Viergever
Nicklas Bendtner
Nicolas Anelka
Nicolas Isimat-Mirin
Nicolás Otamendi
Nicolò Zaniolo
Niklas Moisander
Niklas Süle
Nordin Wooter
Obafemi Martins
Ognjen Vukojević
Oleksandr Hladkyy
Oleksandr Kucher
Óscar Cardozo
Owen Hargreaves
Pablo Aimar
Paolo Maldini
Pape Cheikh Diop
Pascal Groß
Patryk Małecki
Paul Hartley
Paul Pogba
Paul Scholes
Pavel Horváth
Pavel Pogrebnyak
Pepe
Peter Larsson
Peter Løvenkrands
Petr Čech
Petr Jiráček
Philippe Mexès
Piotr Brożek
Piotr Zieliński
Pyotr Bystrov
Radim Řezník
Rafael Carioca
Rafał Boguski
Rafał Murawski
Rafik Djebbour
Ramires
Ramy Bensebaini
Raphael Schäfer
Raul Meireles
Răzvan Raț
Renato Sanches
Ricardo Carvalho
Ricardo van Rhijn
Robert Huth
Roberto Firmino
Roberto Hilbert
Roberto Pereyra
Robin van Persie
Robinho
Romain Del Castillo
Romain Faivre
Roman Pavlík
Romelu Lukaku
Rômulo
Rui Costa
Rui Patrício
Ryan Giggs
Salih Özcan
Salomon Kalou
Salvatore Sirigu
Sami Khedira
Samir Nasri
Samuel Dahl
Sándor Torghelle
Saša Papac
Scott Brown
Scott McDonald
Sead Kolašinac
Sebastian Rode
Sebastian Rudy
Sergei Bryzgalov
Sergei Semak
Sergey Ryzhikov
Sergio Ramos
Serhou Guirassy
Shaun Wright-Phillips
Sidney Govou
Silas Katompa
Silvère Ganvoula M'Boussy
Silvio Meißner
Simon Rolfes
Sol Campbell
Sölvi Ottesen
Søren Larsen
Sotiris Leontiou
Sotiris Ninis
Stefan de Vrij
Stefan Kießling
Stefano Denswil
Stefano Mauri
Stephan El Shaarawy
Steven Naismith
Sulley Muntari
Taras Mykhalyk
Theo Walcott
Thiago Silva
Thomas Delaney
Thomas Müller
Tiago Ferreira
Tiberiu Ghioane
Tim Borowski
Timo Gebhart
Toby Alderweireld
Tomas De Vincenti
Tomáš Hübschman
Tomáš Rosický
Tomasz Dawidowski
Tonel
Tony Watt
Urby Emanuelson
Uroš Spajić
Václav Pilař
Vadim Kurlovich
Valentin Stocker
Vangelis Pavlidis
Vedran Ćorluka
Vicente Sánchez
Victor Wanyama
Vinicius
Vladimír Darida
Wayne Rooney
Welliton
Wesley Sneijder
Wilfried Bony
Willian
Xabi Alonso
Xherdan Shaqiri
Yan Couto
Yann Sommer
Yaroslav Rakitskiy
Yevgeni Makeyev
Yevhen Seleznyov
Yohan Cabaye
Zachary Athekame
Zdeněk Pospěch
Zdravko Kuzmanović
Zeki Amdouni"""

# 2. Lista bruta de LaLiga
texto_laliga = """Aarón Martín Caricol
Aarón Níguez Esclapez
Abdallahi Mohamed Mahmoud
Abdelaziz Barrada
Abdelkader Mohamed Ghezzal
Abdón Prats Bastidas
Abdoul Karim Yoda
Abdoulay Konko
Abdoulaye Ba
Abdoulaye Doucouré
Abel Enrique Aguilar Tapia
Abel Gómez Moreno
Abraham González Casanova
Abraham Minero Fernández
Achille Emaná Edzimbi
Adalberto Peñaranda Maestre
Ádám Pintér
Aderllan Leandro de Jesus Santos
Adil Rami
Adnan Januzaj
Adrià Giner Pedrosa
Adrián Colunga Pérez
Adrián Embarba Blázquez
Adrián González Morales
Adrián Javier Gunino Duque
Adrián López Álvarez
Adrián López Rodríguez
Adrián Marín Gómez
Adrián Sardinero Corpa
Adriano Correia Claro
Adriano Ferreira Martins
Agustín Aranzábal Alkorta
Agustín García Iñiguez
Aïssa Mandi
Aitor López Rekarte
Aitor Núñez Martín
Aitor Ocio Carrión
Aitor Ramos Leniz
Aitor Ruibal García
Aitor Tornavaca Fernández
Akihiro Ienaga
Alain Didier Zokora-Déguy
Albert Celades López
Albert Crusat Domene
Albert Luque Martos
Albert Riera Ortega
Alberto Aquilani
Alberto Botía Rabasco
Alberto Bueno Calvo
Alberto De La Bella Madureño
Alberto Facundo Costa
Alberto Lopo García
Alberto Lora Ramos
Alberto Marcos Rey
Alberto Martín Romo García Adámez
Alberto Mateus Contreiras Gonçalves
Alberto Moreno Pérez
Alberto Perea Correoso
Alberto Rivera Pizarro
Alberto Rodríguez Baró
Alberto Soro Álvarez
Alberto Zapater Arjol
Aldo Pedro Duscher
Aleix García Serrano
Aleix Vidal Parreu
Alejandro Alfaro Ligero
Alejandro Arribas Garrido
Alejandro Barrera García
Alejandro Berenguer Remiro
Alejandro Bergantiños García
Alejandro Blanco Sánchez
Alejandro Campano Hernando
Alejandro Damián Domínguez
Alejandro Darío Gómez
Alejandro Felip Selma
Alejandro Fernández Iglesias
Alejandro Gallar Falguera
Alejandro Gálvez Jimena
Alejandro Granell Nogué
Alejandro López Sánchez
Alejandro Marañón Pérez
Alejandro Menéndez Díez
Alejandro Moreno Lopera
Alejandro Pozuelo Melero
Aleksandar Katai
Aleksandar Pantić
Alen Halilović
Alessio Tacchinardi
Alex Fernandez Sanchez
Alexander Alegría Moreno
Alexander Isak
Alexander Kerzhakov
Alexander Mesa Travieso
Alexander Szymanowski
Alexandre Coeff
Alexandre Geijo Pazos
Alexandre Rodrigues da Silva
Alexandros Tziolis
Alexis Ruano Delgado
Alfa Semedo Esteves
Alfonso Pedraza Sag
Alfreð Finnbogason
Alhassane Bangoura
Alhassane Keita
Allan Romeo Nyom
Álvaro Antón Camarero
Álvaro Arbeloa Coca
Álvaro Arroyo Martínez
Álvaro Borja Morata Martín
Álvaro Cejudo Carmona
Álvaro Domínguez Soto
Álvaro García Rivera
Álvaro Giménez Candela
Álvaro González Soberón
Álvaro José Jiménez Guerrero
Álvaro Juan Cruz Armada
Álvaro Luiz Maior de Aquino
Álvaro Medrán Just
Álvaro Negredo Sánchez
Álvaro Odriozola Arzallus
Álvaro Rubio Robles
Álvaro Vadillo Cifuentes
Álvaro Vázquez García
Amankwaa Akurugu
Amath Ndiaye
Anaitz Arbilla Zabala
Ander Barrenetxea Muguruza
Ander Capa Rodríguez
Ander Guevara Lajo
Ander Herrera Agüera
Ander Iturraspe Derteano
Ander Murillo García
Anderson Luis de Carvalho
Anderson Silva de França
Andoni Gorosabel Espinosa
Andoni Iraola Sagarna
André de Castro Pereira
André Miguel Valente Silva
Andreas Hoelgebaum Pereira
Andreas Ivanschitz
André-Frank Zambo Anguissa
Andrés Eduardo Fernández Moreno
Andrés José Fleurquin Rubio
Andrés Nicolás D''Alessandro
Andrés Palop Cervera
Andreu Fontàs Prat
Andrija Delibašić
Ángel Dealbert Ibáñez
Ángel Domingo López Ruano
Ángel Fabián Di María Hernández
Ángel Javier Arizmendi de Lucas
Ángel Lafita Castillo
Ángel Luis Rodríguez Díaz
Ángel Manuel Vivar Dorado
Ángel Martín Correa
Ángel Martínez Cervera
Ángel Montoro Sánchez
Ángel Morales Cuerva
Ángel Trujillo Canorea
Angelos Basinas
Aníbal Samuel Matellán
Ante Budimir
Anthony Rubén Lozano Colón
Antoine Griezmann
Antolín Alcáraz Viveros
Antoni Lluis Adrover Colom
Antonio Adán Garrido
António Alberto Bastos Pimparel
Antonio Amaya Carazo
Antonio Baltasar Doblas Santana
Antonio Barragán Fernández
Antonio Floro Flores
Antonio Galdeano Benítez
Antonio Hidalgo Morilla
Antonio Latorre Grueso
Antonio López Guerrero
Antonio Manuel Luna Rodríguez
Antonio Manuel Sánchez Gómez
Antonio Moral Segura
Antonio Núñez Tena
Antonio Pacheco D"Agosti
Antonio Pinilla Miranda
Antonio Puerta Pérez
Antonio Ramiro Pérez
Antonio Rodríguez Dovale
Antonio Rodríguez Martínez
Antonio Rukavina
Antonio Tomás González
Anuar Mohamed Tuhami
Arda Turan
Aridane Hernández Umpiérrez
Ariel Gerardo Nahuelpán Osten
Ariel Miguel Santiago Ibagaza
Aritz Aduriz Zubeldia
Aritz Elustondo Irribaria
Arjen Robben
Armando Miguel Correia de Sa
Armindo Tué Na Bangna
Arnaldo Antonio Sanabria Ayala
Arouna Koné
Artem Kravets
Arthur Etienne Boka
Arturo García Muñoz
Asier del Horno Cosgaya
Asier Goiria Etxebarria
Asier Illarramendi Andonegi
Asier Riesgo Unamuno
Asier Villalibre Molina
Augusto Jorge Mateo Solari
Augusto Matías Fernández
Aymen Abdennour
Aymeric Laporte
Ayoze Díaz Díaz
Ayoze García Pérez
Aythami Artiles Oliva
Bartholomew Owogbalor Ogbeche
Bartlomiej Pawłowski
Ben Sahar
Benoît Trémoulinas
Beñat Etxebarria Urkiaga
Bernard Mensah
Bernardo José Espinosa Zúñiga
Blagoy Georgiev
Borja Ekiza Imaz
Borja Fernández Fernández
Borja García Freire
Borja Gómez Pérez
Borja González Tomás
Borja Iglesias Quintas
Borja Mayoral Moya
Borja Oubiña Meléndez
Borja Sainz Eguskiza
Borja Valero Iglesias
Borja Valle Balonga
Borja Viguera Manzanares
Boško Janković
Braian Damián Rodríguez Carballo
Brais Méndez Portela
Braulio Nóbrega Rodríguez
Bruno Alexandre Vilela Gama
Bruno Cirillo
Bruno González Cabrera
Bruno Saltor Grau
Bruno Soriano Llido
Bryan Gil Salvatierra
Bryan Martín Rabello Mella
Carl Medjani
Carles Aleña Castillo
Carles Gil de Pareja Vicent
Carles Planas Antolínez
Carlos Alberto Sánchez Moreno
Carlos Alberto Vela Garrido
Carlos Andrés Diogo Enseñat
Carlos Arturo Bacca Ahumada
Carlos Calvo Sobrado
Carlos Carbonell Gil
Carlos Castro García
Carlos Domínguez Cáceres
Carlos Fernández Luna
Carlos González Peña
Carlos Gurpegi Nausia
Carlos Henrique Casimiro
Carlos Javier Acuña Caballero
Carlos Joaquín Correa
Carlos Jorge Neto Martins
Carlos Marchena López
Carlos Martín Vigaray
Carlos Martínez Díez
Carlos Merino González
Carlos Neva Tey
Carlos Reina Aranda
Carlos Soler Barragán
Carmelo José González Jiménez
Cayetano Bartolomé Bonnín Vásquez
Cédric Bakambu
Cedric Mabwati Gerard
Celso Borges Mora
César Arzo Amposta
César González Navas
César Palacios Chocarro
Charles Días Barbosa de Oliveira
Charly Musonda Junior
Chidozie Collins Awaziem
Christian Alfonso López
Christian Daniel Bravo Araneda
Christian Fernández Salas
Christian Gabriel Oliva Giménez
Christian Koffi Romaric N''Dri
Christian Riganò
Christian Rivera Hernández
Christian Robert Santos Kwasniewski
Christoph Metzelder
Chu-Young Park
Claudio Andrés Bravo Muñoz
Claudio Beauvue
Claudio Matías Kranevitter
Cléber Santana Loureiro
Clemente Juan Rodríguez
Cosmin Marius Contra
Cristhian Ricardo Stuani Curbelo
Cristian Darío Álvarez
Cristian Eduardo Zapata Valencia
Cristian Gabriel Rodríguez Barrotti
Cristian Gómez García
Cristian Hidalgo González
Cristian Lobato Villegas
Cristian Omar Espinoza
Cristian Osvaldo Álvarez
Cristian Portilla Rodríguez
Cristian Portugués Manzanera
Cristian Tello Herrera
Cristiano Biraghi
Cristiano Doni
Cristiano Ronaldo dos Santos Aveiro
Damià Abella Pérez
Damián Ariel Escudero
Damián Marcelo Musto
Damián Nicolás Suárez Suárez
Damiano Tommasi
Dani Castellano Betancor
Daniel Alberto Díaz
Daniel Alejandro Torres Rojas
Daniel Alves da Silva
Daniel Aranzubia Aguado
Daniel Armand N"Gom Komé
Daniel Carvajal Ramos
Daniel Ceballos Fernández
Daniel Escriche Romero
Daniel Estrada Agirrezablaga
Daniel Filipe Martins Carriço
Daniel García Carrillo
Daniel Gómez Alcón
Daniel González Benítez
Daniel González Güiza
Daniel Jarque Gonzalez
Daniel João Santos Candeias
Daniel José Rodríguez Vázquez
Daniel Nieto Vela
Daniel Parejo Muñoz
Daniel Pinillos González
Daniel Raba Antolín
Daniel Wass
Daniele Bonera
Daniele Verde
Danijel Pranjić
Danilo Barbosa da Silva
Darko Brašanac
Darwin Daniel Machís Marcano
David Aganzo Méndez
David Albelda Aliqués
David Barral Torres
David Beckham
David Belenguer Reverter
David Coromina Pararols
David Cortés Caballero
David Cuéllar Tainta
David de Gea Quintana
David Ferreiro Quiroga
David Fuster Torrijos
David García Cubillo
David García De La Cruz
David García Santana
David García Zubiría
David Generelo Miranda
David Josué Jiménez Silva
David Juncà Reñé
David López Moreno
David López Silva
David Mateos Ramajo
David Navarro Pedrós
David Odonkor
David Remeseiro Salgueiro
David Rodríguez Lombán
David Sánchez Rodríguez
David Simón Rodríguez Santana
David Soria Solís
David Timor Copoví
David Villa Sánchez
David Zurutuza Veillet
Dejan Dražić
Dejan Lekić
Delio Cesar Toledo
Denis Cheryshev
Denis Suárez Fernández
Denis Vavro
Derek Owusu Boateng
Deyverson Brum Silva Acosta
Dídac Vilá Rosselló
Didier Digard
Diego Alberto Milito
Diego Alejandro Rolan Silva
Diego Alves Carreira
Diego Ángel Capel Trinidad
Diego Benito Rey
Diego Camacho Quesada
Diego Carlos Santos Silva
Diego Castro Giménez
Diego da Silva Costa
Diego Daniel Colotto
Diego Forlán Corazo
Diego Ifrán Sala
Diego Javier Llorente Ríos
Diego Lainez Leyva
Diego López Rodríguez
Diego Mainz García
Diego Mariño Villar
Diego Mario Buonanotte Rende
Diego Perotti
Diego Rivas Gutiérrez
Diego Roberto Godín Leal
Diego Tardelli Martins
Dimas Delgado Morgado
Dimitri Foulquier
Dimitrios Siovas
Diogo Ferreira Salomão
Diogo José Rosário Gomes Figueiras
Djené Dakonam Ortega
Domingo Cisma González
Domingo Nagore Arbizu
Domingos Sousa Coutinho Meneses Duarte
Dorlan Mauricio Pabón Ríos
Douglas Luiz Soares de Paulo
Douglas Pereira dos Santos
Dudú Aouate
Duje Čop
Ebi Smolarek
Eddy Silvestre Pascual İsrafilov
Edgar Antonio Méndez Ortega
Edgar Patricio De Carvalho Pacheco
Edson Ramos de Silva
Eduardo Antonio Salvio
Eduardo Bedia Peláez
Eduardo César Daude Gaspar
Eduardo Expósito Jaén
Eduardo Jesús Vargas Rojas
Eduardo Moya Castillo
Eduardo Nascimento Costa
Eduardo Nicolás Tuzzio
Eduardo Ramos Gómez
Efraín Juárez Váldez
Eliaquim Mangala
Elias Mendes Trindade
Eliseu Pereira dos Santos
Elton Giovanni Machado
Emanuel Cecchini
Emerson Aparecido Leite de Souza Junior
Émerson Ferreira da Rosa
Emiliano Adrián Insúa Zapata
Emiliano Ariel Rigoni
Emiliano Daniel Armenteros
Emiliano Daniel Velázquez Maldonado
Emiliano Moretti
Emilio José Viqueira Moure
Emilio Nsue López
Emir Spahić
Emmanuel Adebayor
Emmanuel Nosakhare Igiebor
Emmanuel Okyere Boateng
Emre Çolak
Emre Mor
Eneko Bóveda Altube
Enes Ünal
Enis Bardhi
Enric Gallego Puigsech
Enrique Álvarez San Juan
Enrique Barja Afonso
Enrique de Lucas Martínez
Enrique Fernando Ortiz Moruno
Enrique García Martínez
Enrique González Casín
Enrique Mateo Montoya
Enrique Pérez Muñoz
Enrique Sola Clemente
Enzo Alan Zidane Fernández
Enzo Maresca
Enzo Nicolás Pérez
Eric Bertrand Bailly
Erick Cathriel Cabaco Almada
Erik Morán Arribas
Ermedin Demirović
Ersen Martin
Esteban Félix Granero Molina
Esteban Rolón
Etienne Capoue
Éver Maximiliano David Banega
Ewerthon Henrique de Souza
Ezequiel Luna
Ezequiel Marcelo Garay
Fabián Andrés Vargas Rivera
Fabián Ariel Orellana Valenzuela
Fabián Larry Estoyanoff Poggio
Fabian Lukas Schär
Fabián Ruiz Peña
Fabiano Eler dos Santos
Fábio Alexandre da Silva Coentrão
Fabio Cannavaro
Fabio Celestini
Fabricio Coloccini
Facundo Sebastián Roncaglia
Fausto Rossi
Fayçal Fajr
Federico Julián Fazio
Federico Nicolás Cartabia
Federico Piovaccari
Federico Ricca Rostagnol
Federico Santiago Valverde Dipetta
Federico Vico Villegas
Felipe Alejandro Gutiérrez Leiva
Felipe Augusto de Almeida Monteiro
Felipe Guréndez Aldanondo
Felipe Melo de Carvalho
Felipe Salvador Caicedo Corozo
Felix Dja Ettien Yohou
Fernando Amorebieta Mardaras
Fernando Calero Villa
Fernando Damián Tissone
Fernando Ezequiel Cavenaghi
Fernando Francisco Reges
Fernando José Torres Sanz
Fernando Llorente Torres
Fernando Martín Forestieri
Fernando Miguel Fernández Escribano
Fernando Morientes Sánchez
Fernando Navarro i Corbacho
Fernando Niño Rodriguez
Fernando Rubén Gago
Fernando Soriano Marco
Fernando Varela Ramos
Fernando Vega Torres
Ferrán Corominas Telechea
Ferrán Torres García
Fidel Chaves de la Torre
Filip Bradarić
Filipe Augusto Carvalho Souza
Filipe Luís Kasmirski
Flávio Nunes Ferreira
Florent Sinama-Pongolle
Florin Andone
Francesc Aday Benítez Caraballo
Francis Joseph Coquelin
Francisco Alcácer García
Francisco Casilla Cortés
Francisco David Sousa Franquelo
Francisco Esteban Granados
Francisco Femenía Far
Francisco Gámez López
Francisco Javier Casquero Paredes
Francisco Javier Chica Torres
Francisco Javier Farinós Zapata
Francisco Javier García Fernández
Francisco Javier García Guerrero
Francisco Javier Guerrero Martín
Francisco Javier Hidalgo Gómez
Francisco Javier Rodríguez Vílchez
Francisco Javier Yeste Navarro
Francisco Jesús Pérez Malia
Francisco Jiménez Tejada
Francisco Joaquín Pérez Rufete
Francisco José Beltrán Peinado
Francisco José Maldonado Collantes
Francisco José Molinero Calderón
Francisco José Olivas Alba
Francisco José Perdomo Borges
Francisco Manuel Rico Castro
Francisco Medina Luna
Francisco Mérida Pérez
Francisco Montañés Claverías
Francisco Peña Romero
Francisco Portillo Soler
Francisco Puñal Martínez
Francisco Román Alarcón Suárez
Francisco Sebastián Nadal Martorell
Franco Damián Vázquez
Franco Daniel Jara
Franco Zuculini
Frédéric Oumar Kanouté
Fredson Câmara Pereira
Fyodor Smolov
Gabriel Alejandro Milito
Gabriel Andrei Torje
Gabriel Appelt Pires
Gabriel Armando de Abreu
Gabriel Fernández Arenas
Gabriel Iván Mercado
Gabriel Matías Fernández Leites
Gabriel Moisés Antunes da Silva
Gabriel Veiga Novas
Gaël Kakuta
Gaizka Bergara Picaza
Gaizka Garitano Aguirre
Gaizka Toquero Pinedo
Gaku Shibasaki
Gareth Frank Bale
Gary Alexis Medel Soto
Gaspar Gálvez Burgos
Geoffrey Kondogbia
Gerard Autet Serrabasa
Gerard Deulofeu Lázaro
Gerard Gumbau Garriga
Gerard Moreno Balaguero
Gerard Piqué Bernabéu
Germán Alejandro Pezzella
Germán Darío Lux
Germán Sánchez Barahona
Gerónimo Rulli
Gheorghe Craioveanu
Gianni Michel Eugene Zuiverloon
Giorgi Kochorashvili
Giorgios Seitaridis
Giovani dos Santos Ramírez
Giovani Lo Celso
Giuseppe Rossi
Gonçalo Manuel Ganchinho Guedes
Gonzalo Cacicedo Verdú
Gonzalo Castro Irizábal
Gonzalo Colsa Albendea
Gonzalo Escalante
Gonzalo Gerardo Higuaín
Gonzalo Javier Rodríguez
Gonzalo Julián Melero Manzanares
Gonzalo Pablo Castellani
Goran Čaušić
Gorka Brit Gallego
Gorka Elustondo Urkola
Gorka Iraizoz Moreno
Gorka Larrea García
Grzegorz Krychowiak
Guido Hernán Pizarro
Guido Marcelo Carrillo
Guido Rodríguez
Guilherme dos Santos Torres
Guilherme Magdalena Siqueira
Guilherme Oliveira Santos
Guillermo Luis Franco Farquarson
Gustavo Adrián López Pablo
Gustavo Daniel Cabral Cáceres
Gustavo Enrique Reggi
Gustavo Nery De Sá Da Silva
Haris Medunjanin
Haris Seferović
Héctor Alfredo Moreno Herrera
Héctor Berenguel del Piño
Héctor Font Romero
Héctor Hernández Ortega
Héctor Junior Firpo Adames
Héctor Miguel Herrera López
Héctor Rodas Ramírez
Héctor Sánchez Cabrera
Héctor Yuste Cantón
Hedwiges Maduro
Heiko Westermann
Hélder Filipe Oliveira Lopes
Hélder Jorge Leal Rodrigues Barbosa
Hélder Manuel Marques Postiga
Henok Goitom
Henrique Adriano Buss
Henrique Sereno Fonseca
Hernán Arsenio Pérez González
Hernán Daniel Santana Trujillo
Hernán Darío Bernardello
Hernán Darío Toledo
Hernâni Jorge Santos Fortes
Hipólito Fernández Serrano
Hoalid Regragui
Hugo Duro Perales
Hugo Guillamón Sanmartín
Hugo Mallo Novegil
Hugo Mariano Pavone
Hugo Miguel Ferreira Gomes Viana
Hugo Sotelo
Humberto Andrés Suazo Pontivo
Iago Aspas Juncal
Iago Bouzón Amodeo
Iago Herrerín Buisán
Ibai Gómez Pérez
Ibrahim Amadou
Ibrahima Baldé
Iddrisu Baba Mohammed
Idriss Carlos Kameni
Idrissa Doumbia
Ignacio Camacho Barnola
Ignacio Cases Mora
Ignacio Insa Bohigues
Ignacio Javier Gómez Novo
Ignacio Monreal Eraso
Ignacio Pérez Santamaría
Igor Gabilondo del Campo
Igor Zubeldia Elorza
Ikechukwu Uche
Iker Muniain Goñi
Imanol Agirretxe Arruti
Iñaki Descarga Retegi
Iñaki Muñoz Oroz
Iñaki Williams Arthuer
Iñigo Córdoba Kerejeta
Íñigo Díaz de Cerio Conejero
Íñigo Lekue Martínez
Íñigo López Montaña
Íñigo Martínez Berridi
Iñigo Pérez Soto
Íñigo Vélez De Mendizábal Fernández De García
Ion Vélez Martínez
Iriney Santos Da Silva
Isaac Ajayi Success
Isaac Carcelén Valencia
Isaac Gómez Sánchez
Isaías Sánchez Cortés
Ismael López Blanco
Ismael Urzáiz Aranda
Issam El Adoua
Iván Alejo Peralta
Iván Bolado Palacios
Iván Cuéllar Sacristán
Iván Daniel Alonso Vallejo
Iván De la Peña López
Iván Díaz Ruiz
Iván Gabriel Heinze
Iván Helguera Bujía
Iván López Álvarez
Iván López Mendoza
Ivan Marcano Sierra
Iván Márquez Álvarez
Ivan Obradović
Ivan Rakitić
Iván Ramis Barrios
Ivan Ricardo Neves Abreu Cavaleiro
Iván Sánchez Rico Soto
Iván Santiago Pérez Maceira
Iván Villar Martínez
Ivica Dragutinovic
Izet Hajrović
Jackson Arley Martínez Valencia
Jacobo González Rodrigañez
Jaime Asensio De La Fuente
Jaime Gavilán Martínez
Jaime Mata Arnaiz
Jaime Romero Gómez
Jaime Sánchez Fernández
Jaime Seoane Valenciano
Jairo Izquierdo González
Jairo Samperio Bustara
James David Rodríguez Rubio
Jaroslav Plašil
Jaume Doménech Sánchez
Jaume Vicent Costa Jordá
Javad Nekounam
Javi Castellano Betancor
Javier Baraja Vegas
Javier Calleja Revilla
Javier Camuñas Gallego
Javier Casas Cuevas
Javier Del Pino González
Javier Eraso Goñi
Javier Espinosa González
Javier Fuego Martínez
Javier García Portillo
Javier Garrido Behovide
Javier Guerra Rodríguez
Javier Hernández Balcázar
Javier Ignacio Aquino Carmona
Javier Lara Grande
Javier López Rodríguez
Javier Magro Matilla
Javier Márquez Moreno
Javier Martínez Aginaga
Javier Muñoz Jiménez
Javier Ontiveros Parra
Javier Paredes Arango
Javier Pedro Saviola Fernández
Javier Rodríguez Venta
Javier Ros Añón
Javier Sánchez de Felipe
Javier Varas Herrera
Jefferson Andrés Lerma Solís
Jefferson Antonio Montero Vite
Jeffrey Sarpong
Jeison Fabián Murillo Cerón
Jens Jønsson
Jeremie Boga
Jérémy Mathieu
Jérémy Perbet
Jérémy Toulalan
Jermaine Pennant
Jerónimo Figueroa Cabrera
Jesé Rodríguez Ruiz
Jesús Alberto Dátolo
Jesús Capitán Prada
Jesús Gámez Duarte
Jesús Joaquín Fernández Sáez de la Torre
Jesús María Herrero Gómez
Jesús María Lacruz Gómez
Jesús Navas González
Jesús Perera López
Jesús Vallejo Lázaro
Jhon Andrés Córdoba Copete
Jhon Stiven Mondragón Dosman
Jirí Jarošík
Joan Capdevila Méndez
Joan Jordán Moreno
Joan Sastre Vanrell
Joan Verdú Fernández
João Félix Sequeira
João Fernando Nelo
João Pedro Cavaco Cancelo
João Pedro da Silva Pereira
João Pedro Neves Filipe
João Victor de Albuquerque Bruno
Joaquín Fernández Moreno
Joaquín José Marín Ruiz
Joaquín Navarro Jiménez
Joaquín Oscar Larrivey
Joaquín Sánchez Rodríguez
Joel Nathaniel Campbell Samuels
Jofre González Mateu
Johan Andrés Mojica Palacio
Johann Vogel
Johannes Geis
John Aloisi
John Guidetti
Johnny Heitinga
Jon Ander Garrido Moracia
Jon Ansotegi Gorostola
Jon Aurtenetxe Borde
Jon Bautista Orgilles
Jon Dahl Tomasson
Jon Errasti Zabalete
Jon Miquel Toral Harper
Jon Moncayola Tollar
Jon Morcillo Conesa
Jonas Gonçalves Oliveira
Jonás Manuel Gutiérrez
Jonas Martin
Jonás Ramalho Chimeno
Jonatan Soriano Casas
Jônatas Domingos
Jonathan Aspas Juncal
Jonathan Calleri
Jonathan Castro Otto
Jonathan Cristian Silva
Jonathan de Guzmán
Jonathan dos Santos Ramírez
Jonathan Javier Rodríguez Portillo
Jonathan Pereira Rodríguez
Jonathan Rodríguez Menéndez
Jonathan Sesma González
Jonathan Sundy Zongo
Jonathan Viera Ramos
Jonathas Cristian de Jesus
Jonhatan Montiel Caballero
Jordi Alba Ramos
Jordi Amat Maas
Jordi Figueras Montel
Jordi López Felpeto
Jordi Xumetra Feliu
Jorge Andújar Moreno
Jorge De Frutos Sebastián
Jorge Franco Alviz
Jorge Galán Anaut
Jorge García Morcillo
Jorge Gonzalez Diaz
Jorge Larena Avellaneda Roig
Jorge López Marco
Jorge López Montaña
Jorge Meré Pérez
Jorge Miguel Dias Gonçalves
Jorge Miramón Santagertrudis
Jorge Molina Vidal
Jorge Pulido Mayoral
Jorge Resurrección Merodio
Jorge Sammir Cruz Campos
José Alberto Cañas Ruiz Herrera
José Alejandro Suárez Martín
José Andrés Guardado Hernández
José Ángel Alonso Martín
José Ángel Crespo Rincón
José Ángel Gómez Campaña
José Ángel Pozo la Rosa
José Ángel Valdés Díaz
Jose Antonio Culebras Arenas
José Antonio Delgado Villar
José Antonio Dorado Ramírez
José Antonio García Calvo
José Antonio García Rabasco
José Antonio Martínez Gil
José Antonio Miranda Boacho
José Antonio Morente Oliva
José Antonio Reyes Calderón
José Antonio Rodríguez Díaz
José Carlos de Araújo Nunes
José Carlos Fernández Vázquez
José Edmílson Gomes de Moraes
José Eduardo Albácar Gallego
José Eduardo Rosa Vale de Castro
José Emilio Amavisca Gárate
José Ernesto Sosa
José Ignacio Fernández Iglesias
José Ignacio Martínez García
José Ignacio Peleteiro Ramallo
José Isidoro Gómez Torres
José Javier Barkero Saludes
José Joaquín Moreno Verdú
José Luis García del Pozo
José Luis Gayà Peña
Jose Luis Martí Soler
José Luis Morales Nogales
José Luis Moreno Barroso
José Luis Sanmartín Mato
José Manuel Arnáiz Díaz
José Manuel Casado Bizcocho
José Manuel Flores Moreno
José Manuel Fontán Mondragón
José Manuel González Ortiz
José Manuel Jiménez Ortiz
José Manuel Jurado Marín
José Manuel Rodríguez Benito
José María Callejón Bueno
José María Calvo
José María Giménez de Vargas
José Maria Gutiérrez Hernández
José María López de Silva Sánchez
José María Martín-Bejarano Serrano
Jose María Movilla Cubero
José María Romero Poyón
José Martín Cáceres Silva
José Moratón Taeño
José Ortiz Bernal
José Ramiro Funes Mori
José Raúl Baena Urdiales
José Rodríguez Martínez
José Romero Urtasun
José Salomón Rondón Giménez
José Verdú Nicolás
José Vicente Gómez Umpiérrez
José Zahinos
Joseba Andoni Etxeberria Lizardi
Joseba Garmendia Elorriaga
Joseba Llorente Etxarri
Joseba Zaldúa Bengoetxea
Josep Señé Escudero
Joseph Aidoo
Josip Radošević
Josu Sarriegi Zumárraga
Jozabed Sánchez Ruiz
Juan Alberto Andreu Alvarado
Juan Ángel Albín Leites
Juan Antonio Rodríguez Villamuela
Juan Bernat Velasco
Juan Camilo Hernández Suárez
Juan Carlos Pérez López
Juan Carlos Real Ruiz
Juan Carlos Valerón Santana
Juan Cruz Ochoa López
Juan Daniel Forlín
Juan de Dios Prados López
Juan Domínguez Lamas
Juan Emmanuel Culio
Juan Fernando Arango Sáenz
Juan Francisco García García
Juan Francisco Martínez Modesto
Juan Francisco Moreno Fuertes
Juan Francisco Torres Belén
Juan Gutiérrez Moreno
Juan Isaac Cuenca López
Juan Jesús Calatayud Sánchez
Juan Jesús Gutiérrez Robles
Juan José Expósito Ruíz
Juan José Narváez Solarte
Juan Luis Gómez López
Juan Luis Hens Lorite
Juan Manuel Delgado Moreno
Juan Manuel Gómez Sánchez
Juan Manuel Mata García
Juan Manuel Ortiz Palazón
Juan Miguel Jiménez López
Juan Muñoz Muñoz
Juan Pablo Añor Acosta
Juan Pedro Ramírez López
Juan Quero Barraso
Juan Rafael Fuentes Hernández
Juan Rodríguez Martínez
Juan Torres Ruiz
Juan Valera Espín
Jukka Raitala
Julen Guerrero López
Julián Cuesta Díaz
Julián de Guzmán
Julián Luque Conde
Julián Omar Ramos Suárez
Juliano Roberto Antonello
Julien Escudé
Julio Álvarez Mosquera
Júlio César Clement Baptista
Júnior Wakalibille Lago
Kalu Uche
Kanga Gauthier Akalé
Kang-In Lee
Karim Benzema
Karim Rekik
Karl Brillant Toko Ekambi
Kenan Kodro
Kennedy Bakircioglu
Kenneth Josiah Omeruo
Kepa Blanco Gonzalez
Kevin Gameiro
Kévin Manuel Rodrigues
Kevin Martín García Martínez
Kevin-Prince Boateng
Keylor Navas Gamboa
Khouma El Hadji Babacar
Klaas-Jan Huntelaar
Kléper Laveran Lima Ferreira
Knut Olav Rindarøy
Koikili Lertxundi Del Campo
Krisztián Vadócz
Lassad Hassen Nouioui
Lassana Diarra
László Sepsi
Laureano Antonio Villa Suárez
Laureano Sanabria Ruiz
Laurențiu Dumitru Roșu
Leandro Daniel Cabrera Sasía
Leandro Daniel Somoza
Lei Wu
Leonardo Carrilho Baptistão
Leonardo Daniel Ponzio
Lévy Clément Madinda
Liassine Cadamuro-Bentaïba
Lionel Sebastián Scaloni
Ljubomir Fejsa
Lluis Sastre Reus
Lorenzo Enrique Reyes Vicencio
Lorenzo Jesús Morón García
Loukas Vyntra
Luca Sangalli Fuentes
Lucas Alfonso Orbán Alegre
Lucas Antonio Wílchez
Lucas Ariel Boyé
Lucas Ariel Ocampos
Lucas Hernández Pi
Lucas Pérez Martínez
Lucas René Olaza Catrofe
Lucas Silva Borges
Lucas Torró Marset
Lucas Vázquez Iglesias
Luciano Fabián Monzón
Luciano Gabriel Figueroa Herrera
Luciano Martín Galletti
Luciano Vietto
Ludovic Butelle
Ludovic Delporte
Luis Alberto Romero Alconchel
Luis Alberto Suárez Díaz
Luis Amaranto Perea Mosquera
Luis Carlos Correia Pinto
Luis Carlos Pereira Carneiro
Luís Carlos Ramos Martins
Luis Eduardo Delgado Pacheco
Luís Eduardo Schmidt
Luis Ezequiel Ávila
Luís Fabiano Clemente
Luis Fernández Gutiérrez
Luis Fernando Muriel Fruto
Luis García Fernández
Luis Hernández Rodríguez
Luis Javier García Sanz
Luis Javier Suárez Charris
Luis Jesús Rioja González
Luis Manuel Rubiales Béjar
Luis Manuel Villa López
Luís Miguel Afonso Fernandes
Luís Miguel Brito Garcia Monteiro
Luis Miguel Sánchez Benítez
Luis Milla Manzanares
Luis Prieto Zalbidegoitia
Luka Modrić
Luuk de Jong
MacDonald Mariga Wanyama
Mahamadou Diarra
Mamadou Koné
Manuel Agudo Durán
Manuel Alejandro García Sánchez
Manuel Castellano Castro
Manuel del Moral Fernández
Manuel Gaspar Haro
Manuel Henrique Tavares Fernandes
Manuel Javier Vallejo Galván
Manuel Jesús Arana Rodríguez
Manuel Jesús Ortiz Toribio
Manuel Jesús Vázquez Florido
Manuel Lanzarote Bruno
Manuel Martínez Lara
Manuel Morlanes Ariño
Manuel Onwu Villafranca
Manuel Pablo García Díaz
Manuel Pérez Rodrigo
Manuel Rolando Iturra Urrutia
Manuel Torres Caturla
Manuel Trigueros Muñoz
Marc Bertrán Vilanova
Marc Cardona Rovira
Marc Cucurella Saseta
Marc Fernández Gràcia
Marc Navarro Ceciliano
Marc Pedraza Sarto
Marc Roca Junqué
Marc Torrejón Moya
Marc Valiente Hernández
Marcelo Alfonso Díaz Rojas
Marcelo Vieira da Silva Júnior
Marco Andreolli
Marco Antonio Simoes Caneira
Marco Asensio Willemsen
Marco Aurélio Brito Dos Prazeres
Marco Gastón Ruben Rodríguez
Marco Jhonnier Pérez Murillo
Marco Sangalli Fuentes
Marcos André de Sousa Mendonça
Marcos Antonio Senna da Silva
Marcos dos Santos Assunção
Marcos García Barreno
Marcos Llorente Moreno
Marcos Mauro López Gutiérrez
Marcos Sebastián Aguirre
Marcos Tébar Ramiro
Mariano Andrés Pernía
Mariano Díaz Mejía
Mariano Ferreira Filho
Mario Bermejo Castanedo
Mario Gaspar Pérez Martínez
Mario Gutiérrez Cotelo
Mario Mandžukić
Mario Martínez Rubio
Mario Pašalić
Mario Suárez Mata
Maris Verpakovskis
Marius Stankevičius
Mark Dennis González Hoffmann
Markel Bergara Larrañaga
Markel Susaeta Laskurain
Marko Babić
Marko Livaja
Marko Marin
Marko Rog
Markus Rosenberg
Marlos Moreno Durán
Martí Crespí Pascual
Martín Aguirregabiria Padilla
Martin Braithwaite Christensen
Martín Gastón Demichelis
Martín Mauricio Astudillo
Martín Maximiliano Mantovani
Martín Montoya Torralbo
Martin Petrov
Martín Zubimendi Ibáñez
Masoud Shojaei Soleimani
Mate Bilić
Mateo Ezequiel García
Mateo Kovačić
Mateo Pablo Musacchio
Matheus Dória Macedo
Mathías Olivera Miramontes
Mathieu Berson
Mathieu Flamini
Matías Aguirregaray Guruceaga
Matías Ariel Fernández Fernández
Matías Emanuel Lequi
Matías Ezequiel Vargas Martín
Matías Gustavo Alustiza
Matías Lionel Fritzler
Matías Nahuel Leiva Esquivel
Matías Nicolás Pavoni
Matteo Contini
Matuzalém Francelino da Silva
Mauricio Andrés Cuero Castillo
Mauricio Lemos Merladet
Maurizio Lanzaro
Mauro Javier Dos Santos
Mauro Wilney Arambarri Rosa
Maxime Gonalons
Maximilian Wöber
Maximiliano Gómez González
Maximiliano Rubén Rodríguez
Mehdi Lacen
Mehmet Topal
Mesut Özil
Michael Essien
Michael Krohn-Dehli
Michael Nicolás Santos Rosadilla
Michael Olunga Ogada
Michaël Pereira
Míchel Macedo Rocha Machado
Mickaël Malsa
Miguel Alfonso Herrero Javaloyas
Miguel Ángel Angulo Valderrey
Miguel Ángel De las Cuevas Barberá
Miguel Ángel Ferrer Martínez
Miguel Ángel García Pérez Roldán
Miguel Ángel Garrido Cifuentes
Miguel Ángel Guerrero Martín
Miguel Ángel Lozano Ayala
Miguel Ángel Moyà Rumbo
Miguel Ángel Nieto de la Calle
Miguel Ángel Salgado Fernández
Miguel Ángel Sánchez Muñoz
Miguel Arturo Layún Prado
Miguel Baeza Pérez
Miguel Filipe Nunes Cardoso
Miguel Flaño Bezunartea
Miguel Marcos Madera
Miguel Olavide Montes
Miguel Palanca Fernández
Miguel Pallardó González
Miguel Pérez Cuesta
Miguel Torres Gómez
Mikel Aguirregomezkorta Larrea
Mikel Alonso Olano
Mikel Aranburu Eizagirre
Mikel Balenziaga Oruesagasti
Mikel González de Martín Martínez
Mikel Merino Zazón
Mikel Oyarzabal Ugarte
Mikel Rico Moreno
Mikel San José Domínguez
Mikel Vesga Arruti
Milan Smiljanić
Milan Stepanov
Modibo Sagnan
Mohamed El Yaagoubi
Mohamed Gasana Tchité
Mohamed Lamine Sissoko Gillan
Mohamed Salisu
Moisés Gómez Bordonado
Moisés Hurtado Pérez
Moses Daddy-Ajala Simon
Mouctar Diakhaby
Mouhamadou Dabo
Mubarak Wakaso
Munir El Haddadi Mohamed
Nabil Baha
Nabil El Zhar
Nabil Fekir
Nabil Ghilas
Natalio Lorenzo Poquet
Nauzet Alemán Viera
Nehuén Pérez
Nelson Antonio Haedo Valdez
Nélson Miguel Castro Oliveira
Nemanja Gudelj
Nemanja Maksimović
Nemanja Radoja
Nenad Krstičić
Nenad Mirosavljević
Néstor Alejandro Araújo Razo
Néstor Fabián Canobbio Bentaberry
Nicki Niels Bille Nielsen
Nicola Sansone
Nicolás Hernán Otamendi
Nicolás Ladislao Fedor Flores
Nicolás Martín Pareja
Nicolás Santiago Bertolo
Nihat Kahveci
Nikola Vukčević
Nikola Žigić
Nilmar Honorato da Silva
Nivaldo Batista Santana
Nordin Amrabat
Nuno Ricardo de Oliveira Ribeiro
Obafemi Akinwunmi Martins
Odion Jude Ighalo
Oghenekaro Etebo
Ognjen Vranješ
Oier Olazábal Paredes
Oier Sanjurjo Mate
Oihan Sancet Tirapu
Okay Yokuşlu
Olarenwaju Ayoba Kayode
Oliver Burke
Óliver Torres Muñoz
Oliverio Jesús Alvarez González
Omar Mascarell González
Omenuke Mfulu
Omobolaji Habeeb Adekanye
Oriol Riera Magem
Óscar David Romero Villamayor
Óscar de Marcos Arana
Óscar Esau Duarte Gaitán
Óscar Guido Trejo
Óscar Javier González Marcos
Óscar Melendo Jiménez
Óscar Plano Pedreño
Óscar Rodríguez Arnaiz
Óscar Sánchez Fuentes
Óscar Serrano Rodriguez
Óscar Sielva Moreno
Osvaldo Nicolás Fabián Gaitán
Pablo Álvarez Nuñez
Pablo César Aimar Giordano
Pablo César Pintos Cabral
Pablo Daniel Osvaldo
Pablo Daniel Piatti
Pablo Edson Barrera Acosta
Pablo Ezequiel De Blasis
Pablo Fornals Malla
Pablo Gabriel García Pérez
Pablo González Couñago
Pablo Hernández Domínguez
Pablo Hervías Ruiz
Pablo Ibáñez Tébar
Pablo Ínsua Blanco
Pablo Javier Pérez
Pablo Javier Zabaleta Girod
Pablo Maffeo Becerra
Pablo Orbaiz Lesaka
Pablo Pérez Rodríguez
Pablo Pinillos Caro
Pablo Redondo Martínez
Pablo Sarabia García
Pablo Sicilia Roig
Papa Babacar Diawara
Papa Kouly Diop
Pape Cheikh Diop Gueye
Pape Maly Diamanka
Patrick Claude Ekeng Ekeng
Patrick Twumasi
Pau Francisco Torres
Paul Edgar Akouokou
Paulo Afonso Santos Júnior
Paulo André Rodrigues de Oliveira
Paulo Assunção da Silva
Paulo César Da Silva Barrios
Paulo César Wanchope Watson
Paulo Henrique Chagas de Lima
Pedro Alcalá Guirado
Pedro Andrés Morales Flores
Pedro Bigas Rigo
Pedro León Sánchez Gil
Pedro López Muñoz
Pedro Manuel Munitis Álvarez
Pedro Mario Álvarez Abrante
Pedro Mosquera Parada
Pedro Pablo Hernández
Pedro Ríos Maestre
Pedro Roberto Silva Botelho
Pedro Taunausú Domínguez Placeres
Pere Milla Peña
Pere Pons Riera
Peru Nolaskoain Esnal
Pervis Josué Estupiñán Tenorio
Peter Luccin
Petros Matheus dos Santos Araújo
Philippe Coutinho Correia
Pierre Achille Webó Kouamo
Pione Sisto Ifolo Emirmija
Piotr Trochowski
Pol Lozano Vizuete
Przemysław Tytoń
Quincy Owusu-Abeyie
Rachid Aït-Atmane
Radamel Falcao García Zárate
Rafael Alcântara do Nascimento
Rafael Augusto Sóbis do Nascimento
Rafael Barber Rodríguez
Rafael Clavero Prados
Rafael García García
Rafael Jesús Navarro Mazuelos
Rafael López Gómez
Rafael Mir Vicente
Rafael Sastre Reus
Rafael van der Vaart
Rahamat Riga Mustapha
Ramon Olamilekan Azeez
Raoul Cédric Loé
Raphaël Varane
Raúl Albentosa Redal
Raúl Albiol i Tortajada
Raúl de Tomás Gómez
Raúl García Carnero
Raúl García Escudero
Raúl González Blanco
Raúl Miguel Cámara
Raúl Rodríguez Navarro
Raúl Rodríguez Navas
Raúl Tamudo Montero
Renan Augusto Lodi dos Santos
Renato Dirnei Florencio
Renato Fabrizio Tapia Cortijo
Rene Krhin
Ricardo Alberto Silveira de Carvalho
Ricardo de Oliveira
Ricardo Izecson dos Santos Leite
Ricardo Jorge Luz Horta
Ricardo López Felipe
Ricardo Miguel Moreira da Costa
Ricardo Pérez de Zabalza Goytre
Richard Javier Morales Aguirre
Richmond Yiadom Boakye
Ricky van Wolfswinkel
Riza Durmisi
Robert de Pinho de Souza
Robert Ibáñez Castro
Robert Kenedy Nunes do Nascimento
Robert Navarro Muñoz
Robert Pirès
Roberto Antonio Correa Silva
Roberto Canella Suárez
Roberto Carlos Abbondanzieri
Roberto Jiménez Gago
Roberto José Rosales Altuve
Roberto Lago Soto
Roberto López Esquiroz
Roberto Luis Gaspar de Deus Severo
Roberto Martínez Rípodas
Roberto Román Triguero
Roberto Soldado Rillo
Roberto Soriano
Roberto Suárez Álvarez
Roberto Suárez Pier
Roberto Torres Morales
Roberto Trashorras Gayoso
Robin Aime Robert Le Normand
Róbson de Souza
Rodolfo Bodipo Díaz
Rodolfo Martín Arruabarrena
Rodrigo Ely
Rodrigo Hernández Cascante
Rodrigo Javier De Paul
Rodrigo Moreno Machado
Rodrigo Ríos Lozano
Rodrigo Sánchez Rodriguez
Rodrigo Tarín Higón
Rodrygo Silva de Goes
Roger Claver Assalé Djapone
Roger García Junyent
Roger Martí Salvador
Roland Conde Lamah
Román Fernando Martínez
Roque Luis Santa Cruz Cantero
Roque Mesa Quevedo
Rosinei Adolfo
Royston Ricky Drenthe
Rúben Afonso Borges Semedo
Rubén Alcaraz Jiménez
Rubén Baraja Vegas
Rubén Blanco Veiga
Rubén Castro Martín
Rubén de la Red Gutiérrez
Rubén Duarte Sánchez
Rubén García Santos
Rubén González Rocha
Rubén Gracia Calmache
Rubén Martín Pulido
Rúben Micael Freitas da Ressurreição
Rúben Miguel Nunes Vezo
Rubén Navarro Méndez
Rubén Pardo Gutiérrez
Rubén Peña Jiménez
Rubén Rochina Naixes
Rubén Salvador Pérez Del Mármol
Rubén Sobrino Pozuelo
Rubén Suárez Estrada
Rui Pedro da Rocha Fonte
Ruud van Nistelrooy
Ryad Boudebouz
Ryan Donk
Ryan Guno Babel
Sabin Merino Zuloaga
Sabit Abdulai
Saïd Boutahar
Saidy Janko
Salvador Ballesta Vialcho
Salvador Sánchez Ponce
Salvador Sevilla López
Sami Khedira
Samir Nasri
Samuel Castillejo Azuaga
Samuel Chimerenka Chukwueze
Samuel García Sánchez
Samuel Sáiz Alonso
Samuele Longo
Sandro Ramírez Castillo
Sanjin Prcić
Santiago Arias Naranjo
Santiago Cáseres
Santiago Cazorla González
Santiago Mina Lorenzo
Santiago Wilmer Acasiete Ariadela
Saúl Berjón Pérez
Saúl Fernández García
Saúl Ñíguez Esclapez
Sávio Bortolini Pimentel
Savo Milošević
Sebastián Bruno Fernández Miglierina
Sebastián Carlos Cristóforo Pepe
Sebastián Dubarbier
Sebastián Ricardo Nayar
Sebastián Taborda Ramos
Sébastien Squillaci
Sendoa Aguirre Basterretxea
Serdar Gürler
Sergi Darder Moll
Sergi Gómez Solà
Sergi Samper Montaña
Sergio Álvarez Díaz
Sergio Aragoneses Almeida
Sergio Asenjo Andrés
Sergio Canales Madrazo
Sérgio da Silva Pinto
Sergio Enrich Ametller
Sergio Escudero Palomo
Sergio Ezequiel Araújo
Sergio Fernández González
Sergio García De La Fuente
Sergio Gómez Martín
Sergio Gontán Gallardo
Sergio González Soriano
Sergio Guardiola Navarro
Sergio Herrera Pirón
Sergio León Limones
Sergio Leonel Agüero del Castillo
Sergio Martínez Ballesteros
Sergio Matabuena Delgado
Sergio Mora Sánchez
Sergio Ortega González
Sérgio Paulo Barbosa Valente
Sergio Pelegrín López
Sergio Postigo Redondo
Sergio Ramos García
Sergio Reguilón Rodríguez
Sergio Rodríguez García
Sergio Sánchez Ortega
Sergio Tejera Rodríguez
Seung-Ho Paik
Seydou Doumbia
Seydou Kéita
Shinji Okazaki
Shkodran Mustafi
Sidi Yaya Keita
Sidnei Rechel da Silva Júnior
Silvestre Manuel Gonçalves Varela
Sílvio Manuel Azevedo Ferreira Sá Pereira
Simão Mate
Simão Pedro Fonseca Sabrosa
Šime Vrsaljko
Simon Thorup Kjær
Simone Verdi
Simone Zaza
Sisinio González Martínez
Sofiane Boufal
Sofiane Feghouli
Stanislav Lobotka
Stefan Babović
Stefan Savić
Stefan Šćepović
Stephane Dalmat
Stéphane M''Bia Etoundi
Stevan Jovetić
Steve Franck Songo"o
Steven N''Kemboanza Mike Christopher Nzonzi
Stiven Ricardo Plaza Castillo
Stole Dimitrievski
Sulley Ali Muntari
Sylvain N''Diayé
Takashi Inui
Takefusa Kubo
Telmário de Araújo Sacramento
Theo Bernard François Hernández
Théo Bongonda Mbul''Ofeko Batombo
Thibaut Courtois
Thievy Guivane Bifouma Koulossa
Thomas Lemar
Thomas Teye Partey
Tiago Cardoso Mendes
Tiago Filipe Figueiras Gomes
Tiago Manuel Dias Correia
Timothée Kolodziejczak
Tobias Grahn
Tom De Mul
Tomas Franco Tavares
Tomás Pina Isla
Tomáš Ujfaluši
Tomáš Vaclík
Tomer Hemed
Toni Kroos
Unai Bustinza Martínez
Unai Expósito Medina
Unai García Lugea
Unai López Cabrera
Unai Núñez Gestoso
Unai Vencedor Paris
Uroš Račić
Ustaritz Aldekoaotalora Astarloa
Valdet Skënder Rama
Valentín Sergio Pachón Mosquero
Valmiro Lópes Rocha
Vicente Guaita Panadero
Vicente Iborra De La Fuente
Vicente Moreno Peris
Vicente Rodríguez Guillén
Vicente Valcarce Cano
Víctor Camarasa Ferrando
Víctor Campuzano Bonilla
Víctor Casadesús Castaño
Víctor David Díaz Miguel
Víctor Gómez Perea
Víctor Guillermo Álvarez Delgado
Víctor Javier Añino Bermúdez
Víctor Laguardia Cisneros
Víctor Machín Pérez
Víctor Manuel Fernández Gutiérrez
Víctor Mollejo Carpintero
Víctor Rodríguez Romero
Víctor Rubén López
Víctor Ruíz Torre
Víctor Sánchez Mata
Vinícius José Paixão de Oliveira Júnior
Vítor Hugo Gomes Passos
Vladimir Manchev
Vladimír Weiss
Waldo Rubio Martín
Walter Gerardo Pandiani Urquiza
Walter Horacio Peralta Saracho
Wanderson Maciel Sousa Campos
Weligton Róbson Pena de Oliveira
Wellington Alves da Silva
Wesley Sneijder
William Silva de Carvalho
Willian José da Silva
Willian Lanes Lanes de Lima
Wissam Ben Yedder
Xabier Alonso Olano
Xabier Etxeita Gorritxategi
Xabier Prieto Argarate
Xavier Torres Buigues
Yacine Brahimi
Yan Brice Eteki
Yangel Clemente Herrera Ravelo
Yannick Ferreira Carrasco
Yannis Salibur
Yassine Bounou
Yeray Álvarez López
Yeremi Jesús Pino Santos
Yevhen Konoplyanka
Yoel Rodríguez Oterino
Yohan Mollo
Youssef El-Arabi
Youssef En-Nesyri
Yunus Dimoara Musah
Yuri Berchiche Izeta
Yves Hadley Desmarets
Zakaria Bakkali
Zakarya Bergdich
Zouhair Feddal"""

try:
    # 3. Convertir textos a listas limpiando espacios
    lista_champions = [x.strip() for x in texto_champions.split('\n') if x.strip()]
    lista_laliga = [x.strip() for x in texto_laliga.split('\n') if x.strip()]

    # 4. La magia: Unimos todo y quitamos duplicados usando 'set'
    # Al usar set(), si un jugador está en ambas listas o repetido en la misma, se fusiona en uno solo
    jugadores_unicos = list(set(lista_champions + lista_laliga))

    # 5. Ordenamos alfabéticamente
    jugadores_unicos.sort()

    # 6. Creamos el DataFrame
    df_rivales = pd.DataFrame({'Nombre_Rival': jugadores_unicos})

    # 7. 🔥 EL DETALLE CLAVE: Generamos el ID_Rival empezando desde 250
    df_rivales.insert(0, 'ID_Rival', range(250, 250 + len(df_rivales)))

    # 8. Guardar el archivo CSV (ajusta la ruta si lo necesitas)
    ruta_salida = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Dim_Jugadores_Rivales.csv"
    df_rivales.to_csv(ruta_salida, index=False, encoding='utf-8')

    # Mensajes de comprobación por consola
    print(f"✅ ¡Éxito! Dimensión creada con {len(df_rivales)} rivales únicos.")
    print(f"📌 El primer ID asignado es el {df_rivales['ID_Rival'].iloc[0]} y el último es el {df_rivales['ID_Rival'].iloc[-1]}.")
    
except Exception as e:
    print(f"❌ Error al crear la tabla: {e}")