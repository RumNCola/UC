import funciones as f
from utilidades import imprimir_peliculas, imprimir_generos, imprimir_peliculas_genero
from os.path import join


RUTA_PELICULAS = join("archivos", "peliculas.csv")
RUTA_GENEROS = join("archivos", "generos.csv")

print("> Cargar películas:")
imprimir_peliculas(f.cargar_peliculas(RUTA_PELICULAS))
print()

print("> Cargar géneros")
imprimir_generos(f.cargar_generos(RUTA_GENEROS), 5)
print()

print("> Obtener directores:")
generador_peliculas = f.cargar_peliculas(RUTA_PELICULAS)
print(list(f.obtener_directores(generador_peliculas)))
print()

print("> Obtener peliculas (1997 en adelante):")
generador_peliculas = f.cargar_peliculas(RUTA_PELICULAS)
print(list(f.obtener_estrenos(generador_peliculas, 1997)))
print()

print("> Obtener string títulos")
generador_peliculas = f.cargar_peliculas(RUTA_PELICULAS)
print(f.obtener_str_titulos(generador_peliculas))
print()

print("> Filtrar películas (por director):")
generador_peliculas = f.cargar_peliculas(RUTA_PELICULAS)
imprimir_peliculas(
    f.filtrar_peliculas(generador_peliculas, director="Hayao Miyazaki")
)
print("\n> Filtrar películas (rating_min=8.1):")
generador_peliculas = f.cargar_peliculas(RUTA_PELICULAS)
imprimir_peliculas(f.filtrar_peliculas(generador_peliculas, rating_min=8.1))

print("\n> Filtrar películas (rating_max=8.7):")
generador_peliculas = f.cargar_peliculas(RUTA_PELICULAS)
imprimir_peliculas(f.filtrar_peliculas(generador_peliculas, rating_max=8.7))
print()

print("> Filtrar películas por género (fantasía)")
generador_peliculas = f.cargar_peliculas(RUTA_PELICULAS)
generador_generos = f.cargar_generos(RUTA_GENEROS)
imprimir_peliculas_genero(
    f.filtrar_peliculas_por_genero(
        generador_peliculas, generador_generos, "fantasía"
    )
)
print()

print("> Filtrar títulos (Hayao Miyazaki, rating_min=8.1, rating_max=8.7)")
generador_peliculas = f.cargar_peliculas(RUTA_PELICULAS)
print(f.filtrar_titulos(generador_peliculas, "Hayao Miyazaki", 8.1, 8.7))
