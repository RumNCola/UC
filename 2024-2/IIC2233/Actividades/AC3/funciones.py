from functools import reduce
from itertools import product
from typing import Generator

from utilidades import Pelicula, Genero

# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------
def cargar_generos(ruta: str) -> Generator:
    with open(ruta, encoding = 'utf-8') as archivo:
        archivo.readline()
        for linea in archivo:
            datos = linea.split(',')
            traductor = lambda d: (d[0], int(d[1]))
            datos = traductor(datos)
            yield Genero(*datos)

def cargar_peliculas(ruta: str) -> Generator:
    with open(ruta, encoding= 'utf-8') as archivo:
        archivo.readline()
        for linea in archivo:
            datos = linea.split(',')
            traductor = lambda d: (int(d[0]), d[1], d[2], int(datos[3]), float(datos[4]))
            datos = traductor(datos)
            yield Pelicula(*datos)

# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------


def obtener_directores(generador_peliculas: Generator) -> Generator:
    """
    Retorna un generador con el nombre de todos los directores.
    """
    return map(lambda x: x.director, generador_peliculas)


def obtener_estrenos(generador_peliculas: Generator, estreno: int) -> Generator:
    """
    Retorna un generador con el título de todas las películas cuyo
    año de entreno sea igual o mayor al entregado.
    """
    resultado = filter(lambda x: x.estreno >= estreno, generador_peliculas)
    return (pelicula.titulo for pelicula in resultado)


def obtener_str_titulos(generador_peliculas: Generator) -> str:
    """
    Genera un str con todos los títulos de las películas separados por ", ".
    """
    titulos = (pelicula.titulo for pelicula in generador_peliculas)
    try:
        return reduce(lambda x, y:( x + ', ' + y), titulos)
    
    except TypeError as error:
        return ''


def filtrar_peliculas(
    generador_peliculas: Generator,
    director: str | None = None,
    rating_min: float | None = None,
    rating_max: float | None = None,
) -> filter:
    """
    Filtra los elementos del generador de Películas según lo indicado en el input.
    """
    peliculas = (pelicula for pelicula in generador_peliculas)
    
    if director != None:
        peliculas = filter(lambda x: x.director == director, peliculas)    
    if rating_min != None:
        peliculas = filter(lambda x: x.rating >= rating_min, peliculas)
    if rating_max != None:
        peliculas = filter(lambda x: x.rating <= rating_max, peliculas)
        
    return (pelicula for pelicula in peliculas)


def filtrar_peliculas_por_genero(
    generador_peliculas: Generator,
    generador_generos: Generator,
    genero: str | None = None,
) -> Generator:
    """
    Crea un generador con todas las combinaciones posibles entre
    el generador de películas y el generador de géneros.
    Después, filtra las pares obtenidos y mantiene únicamente
    los que presentan el mismo id de película.
    Finalmente, retorna una lista con todos los pares pertenecientes
    a la categoría indicada.
    """
    duplas = product(generador_peliculas, generador_generos)

    duplas = filter(lambda x: (x[0].id_pelicula == x[1].id_pelicula), duplas)
    
    if genero == None:
        return (dupla for dupla in duplas)
    else:
        return filter(lambda x : x[1].genero == genero, duplas)


     


def filtrar_titulos(
    generador_peliculas: Generator, director: str, rating_min: float, rating_max: float
) -> Generator:
    """
    Genera un str con todos los títulos de las películas separados
    por ", ". Solo se consideran las peliculas que tengan el mismo
    director que el indicado, tengan un rating igual o mayor al
    rating_min y un rating igual o menor al rating_max.
    """
    peliculas = (pelicula for pelicula in generador_peliculas)

    rating_min = max(rating_min, float('-inf'))
    rating_max = min(rating_max, float('inf'))

    peliculas = filter(lambda x: x.director == director, peliculas)
    peliculas = filter(lambda x: rating_min <= x.rating <= rating_max, peliculas)

    peliculas = (pelicula.titulo for pelicula in peliculas)

    try:
        return reduce(lambda x,y: (x + ', ' + y), peliculas)
    
    except TypeError:
        return ''