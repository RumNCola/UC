import funciones
import inspect
import re
import unittest
from typing import Generator
from utilidades import Pelicula


class ComandoProhibidoError(BaseException):
    def __init__(self, comandos: list, prohibido: bool = True, *args: object) -> None:
        if prohibido:
            mensaje = 'Se utiliza alguno de estos elementos en la función: '
        else:
            mensaje = 'No se utiliza alguno de estos elementos esperado en la función: '
        mensaje += ', '.join(comandos)
        super().__init__(mensaje, *args[2:])


def usa_comando_prohibido(func, comandos):
    '''
    Comprueba el uso de un comando prohibido en el código.
    En caso de encontrarlo, levanta una excepción.
    '''

    codigo_fuente = inspect.getsource(func).replace('\\', ' ')
    codigo = codigo_fuente.strip()
    for comando in comandos:
        expresion = rf'{comando}([^\n]\s+)'
        if re.search(expresion, codigo):
            raise ComandoProhibidoError(comandos)


def usa_metodo_prohibido(func, comandos):
    '''
    Comprueba el uso de un método prohibido en el código.
    En caso de encontrarlo, levanta una excepción.
    '''

    codigo_fuente = inspect.getsource(func).replace('\\', ' ')
    codigo = codigo_fuente.strip()
    for comando in comandos:
        expresion = rf'{comando}\s*\('
        if re.search(expresion, codigo):
            raise ComandoProhibidoError(comandos)


class TestFiltrarPeliculas(unittest.TestCase):

    def generador_peliculas(self, variacion):
        '''
        Función generadora que retorna distintas instancias de película.
        '''

        if variacion == 1:
            yield Pelicula(5, 'Fight Club', 'David Fincher', 1999, 8.8)
            yield Pelicula(20, 'The Social Network', 'David Fincher', 2010, 7.7)
        elif variacion == 2:
            yield Pelicula(4, 'The Dark Knight', 'Christopher Nolan', 2008, 9.0)
            yield Pelicula(5, 'Fight Club', 'David Fincher', 1999, 8.8)
            yield Pelicula(6, 'Inception', 'Christopher Nolan', 2010, 8.8)
            yield Pelicula(7, 'The Matrix', 'Lana Wachowski', 1999, 8.7)
            yield Pelicula(8, 'Goodfellas', 'Martin Scorsese', 1990, 8.7)
            yield Pelicula(13, 'The Departed', 'Martin Scorsese', 2006, 8.5)
            yield Pelicula(16, 'Interstellar', 'Christopher Nolan', 2014, 8.6)
            yield Pelicula(21, 'The Wolf of Wall Street', 'Martin Scorsese', 2013, 8.2)
        elif variacion == 3:
            yield Pelicula(13, 'The Departed', 'Martin Scorsese', 2006, 8.5)
            yield Pelicula(16, 'Interstellar', 'Christopher Nolan', 2014, 8.6)
            yield Pelicula(21, 'The Wolf of Wall Street', 'Martin Scorsese', 2013, 8.2)

    def test_filtrar_peliculas_por_director(self):
        '''
        Se comprueba que la función "filtrar_peliculas" se aplique correctamente
        cuando solo se le entrega el nombre de un director. Se utilizan las películas
        de la variación 2 (generador_peliculas).
        '''

        datos = funciones.filtrar_peliculas(self.generador_peliculas(2), director='Christopher Nolan')
        peliculas = [
            Pelicula(4, 'The Dark Knight', 'Christopher Nolan', 2008, 9.0),
            Pelicula(6, 'Inception', 'Christopher Nolan', 2010, 8.8),
            Pelicula(16, 'Interstellar', 'Christopher Nolan', 2014, 8.6)
        ]
        self.assertIsInstance(datos, (filter, map, Generator))
        self.assertSequenceEqual(list(datos), peliculas)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_peliculas, ['for', 'while'])
        usa_metodo_prohibido(funciones.filtrar_peliculas, ['list', 'dict', 'set', 'tuple'])

    def test_filtrar_peliculas_por_rating_min(self):
        '''
        Se comprueba que la función "filtrar_peliculas" se aplique correctamente
        cuando solo se le entrega un rating mínimo. Se utilizan las películas
        de la variación 1 (generador_peliculas).
        '''

        datos = funciones.filtrar_peliculas(self.generador_peliculas(1), rating_min=8)
        peliculas = [
            Pelicula(5, 'Fight Club', 'David Fincher', 1999, 8.8)
        ]
        self.assertIsInstance(datos, (filter, map, Generator))
        self.assertSequenceEqual(list(datos), peliculas)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_peliculas, ['for', 'while'])
        usa_metodo_prohibido(funciones.filtrar_peliculas, ['list', 'dict', 'set', 'tuple'])

    def test_filtrar_peliculas_por_rating_max(self):
        '''
        Se comprueba que la función "filtrar_peliculas" se aplique correctamente
        cuando solo se le entrega un rating máximo. Se utilizan las películas
        de la variación 1 (generador_peliculas).
        '''

        datos = funciones.filtrar_peliculas(self.generador_peliculas(1), rating_max=7.7)
        peliculas = [
            Pelicula(20, 'The Social Network', 'David Fincher', 2010, 7.7)
        ]
        self.assertIsInstance(datos, (filter, map, Generator))
        self.assertSequenceEqual(list(datos), peliculas)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_peliculas, ['for', 'while'])
        usa_metodo_prohibido(funciones.filtrar_peliculas, ['list', 'dict', 'set', 'tuple'])

    def test_filtrar_peliculas_todo(self):
        '''
        Se comprueba que la función "filtrar_peliculas" se aplique correctamente
        cuando solo se le entrega el nombre de un director, un rating mínimo y un rating máximo.
        Se utilizan las películas de la variación 2 (generador_peliculas).
        '''

        datos = funciones.filtrar_peliculas(self.generador_peliculas(2), director='Martin Scorsese', rating_min=8.5, rating_max=9)
        peliculas = [
            Pelicula(8, 'Goodfellas', 'Martin Scorsese', 1990, 8.7),
            Pelicula(13, 'The Departed', 'Martin Scorsese', 2006, 8.5)
        ]
        self.assertIsInstance(datos, (filter, map, Generator))
        self.assertSequenceEqual(list(datos), peliculas)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_peliculas, ['for', 'while'])
        usa_metodo_prohibido(funciones.filtrar_peliculas, ['list', 'dict', 'set', 'tuple'])

    def test_filtrar_peliculas_vacio(self):
        '''
        Se comprueba que la función "filtrar_peliculas" se aplique correctamente
        y retorne vacío cuando corresponde. Se utilizan las películas de la
        variación 1 (generador_peliculas).
        '''

        datos = funciones.filtrar_peliculas(self.generador_peliculas(1), director='Lana Wachowski', rating_min=8.5, rating_max=9)
        self.assertIsInstance(datos, (filter, map, Generator))
        self.assertSequenceEqual(list(datos), [])

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_peliculas, ['for', 'while'])
        usa_metodo_prohibido(funciones.filtrar_peliculas, ['list', 'dict', 'set', 'tuple'])
