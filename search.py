import pandas as pd
import math

# Read the data from CSV file
data = pd.read_csv('topicos avanzados/spotify_songs.csv')

#Funcion de busqueda por artista 
def serach_track_artist(artis):
    # Busca el artista en el dataset
    artist_song = data[data['track_artist'] == artis]
    if not artist_song.empty:
        return artist_song[['track_name', 'track_artist', 'track_popularity']]
    else:
        return "Artista no encontrado"
    
def search_album(almbum):
    #Canciones por album 
    album_song = data[data['track_album_name'] == almbum]
    if not album_song.empty:
        return album_song[['track_name', 'track_artist', 'track_album_name']]
    else:
        return "Album no encontrado"

# Paginación
def paginar_resultados(resultados, pagina):
    resultados_por_pagina = 10
    inicio = (pagina - 1) * resultados_por_pagina
    fin = inicio + resultados_por_pagina
    return resultados.iloc[inicio:fin]

# Función para manejar la navegación de cualquier resultado
def mostrar_con_navegacion(resultados):
    if isinstance(resultados, str):  
        print(resultados)
        return
    
    pagina_actual = 1
    total_paginas = math.ceil(len(resultados) / 10)
    
    while True:
        # Mostrar página actual
        pagina_datos = paginar_resultados(resultados, pagina_actual)
        print(f"\nPagina {pagina_actual} de {total_paginas}")
        print("-" * 50)
        print(pagina_datos.to_string(index=False))
        
        # Si solo hay una página, terminar
        if total_paginas <= 1:
            break
        
        # Opciones de navegación
        print(f"\nNavegacion: ", end="")
        if pagina_actual > 1:
            print("(a)nterior ", end="")
        if pagina_actual < total_paginas:
            print("(s)iguiente ", end="")
        print("(q)salir")
        
        opcion = input("Seleccione: ").lower()
        
        if opcion == 's' and pagina_actual < total_paginas:
            pagina_actual += 1
        elif opcion == 'a' and pagina_actual > 1:
            pagina_actual -= 1
        elif opcion == 'q':
            break
        else:
            print("Opcion no valida")

# Menú principal
print("Seleccione tipo de busqueda:")
print("1. Buscar por artista")
print("2. Buscar por album")

opcion_busqueda = input("Ingrese opcion (1 o 2): ")

if opcion_busqueda == "1":
    artist_name = input("Ingrese el nombre del artista: ")
    resultados = serach_track_artist(artist_name)
    mostrar_con_navegacion(resultados)
    
elif opcion_busqueda == "2":
    album_name = input("Ingrese el nombre del album: ")
    resultados = search_album(album_name)
    mostrar_con_navegacion(resultados)
    
else:
    print("Opcion no valida")