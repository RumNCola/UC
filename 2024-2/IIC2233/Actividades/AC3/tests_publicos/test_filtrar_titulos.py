import funciones
import inspect
import re
import unittest

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


class TestFiltrarTitulos(unittest.TestCase):

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

    def test_filtrar_titulo(self):
        '''
        Se comprueba que la función "filtrar_titulos" se aplique correctamente
        y luego retorne, como str, las películas que cumplen el filtro. Variación 1.
        '''

        respuesta = funciones.filtrar_titulos(self.generador_peliculas(1), 'David Fincher', 8, 9)
        self.assertIsInstance(respuesta, str)
        self.assertEqual(respuesta, 'Fight Club')

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_titulos, ['for', 'while'])
        usa_metodo_prohibido(funciones.filtrar_titulos, ['list', 'dict', 'set', 'tuple'])

    def test_filtrar_titulo_1(self):
        '''
        Se comprueba que la función "filtrar_titulos" se aplique correctamente
        y luego retorne, como str, las películas que cumplen el filtro. Variación 2
        '''
        datos = funciones.filtrar_titulos(self.generador_peliculas(2), 'Christopher Nolan', 8.5, 9.2)
        self.assertIsInstance(datos, str)

        peliculas = ['The Dark Knight', 'Inception', 'Interstellar']
        self.assertCountEqual(datos.split(", "), peliculas)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_titulos, ['for', 'while'])
        usa_metodo_prohibido(funciones.filtrar_titulos, ['list', 'dict', 'set', 'tuple'])

    def test_filtrar_titulo_2(self):
        '''
        Se comprueba que la función "filtrar_titulos" se aplique correctamente
        y luego retorne, como str, las películas que cumplen el filtro. Variación 1
        '''

        respuesta = funciones.filtrar_titulos(self.generador_peliculas(1), 'David Fincher', 1, 7.7)
        self.assertIsInstance(respuesta, str)
        self.assertEqual(respuesta, 'The Social Network')

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_titulos, ['for', 'while'])
        usa_metodo_prohibido(funciones.filtrar_titulos, ['list', 'dict', 'set', 'tuple'])

    def test_filtrar_titulo_3(self):
        '''
        Se comprueba que la función "filtrar_titulos" se aplique correctamente
        y luego retorne, como str, las películas que cumplen el filtro. Variación 2
        '''

        datos = funciones.filtrar_titulos(self.generador_peliculas(2), 'Martin Scorsese', 8.5, 9)
        self.assertIsInstance(datos, str)

        peliculas = ['Goodfellas', 'The Departed']
        self.assertCountEqual(datos.split(", "), peliculas)

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_titulos, ['for', 'while'])
        usa_metodo_prohibido(funciones.filtrar_titulos, ['list', 'dict', 'set', 'tuple'])

    def test_filtrar_titulos_sin_peliculas(self):
        '''
        Se comprueba que la función "filtrar_titulos" retorne str vacio cuando no hay peliculas
        en el generador
        '''

        respuesta = funciones.filtrar_titulos(self.generador_peliculas(5), 'Lana Wachowski', 8.5, 9)
        self.assertIsInstance(respuesta, str)
        self.assertEqual(respuesta, '')

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_titulos, ['for', 'while'])
        usa_metodo_prohibido(funciones.filtrar_titulos, ['list', 'dict', 'set', 'tuple'])

    def test_filtrar_titulos_filtro_vacio(self):
        '''
        Se comprueba que la función "filtrar_titulos" retorne str vacio cuando no
        queda ninguna película post filtrar.
        '''

        respuesta = funciones.filtrar_titulos(self.generador_peliculas(1), 'Lana Wachowski', 8.5, 9)
        self.assertIsInstance(respuesta, str)
        self.assertEqual(respuesta, '')

        # No usa for, while o loop
        usa_comando_prohibido(funciones.filtrar_titulos, ['for', 'while'])
        usa_metodo_prohibido(funciones.filtrar_titulos, ['list', 'dict', 'set', 'tuple'])
