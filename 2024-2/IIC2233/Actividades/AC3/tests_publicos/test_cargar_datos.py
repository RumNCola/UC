import funciones
import unittest

from os import remove
from typing import Generator
from utilidades import Pelicula, Genero


class TestCargarDatos(unittest.TestCase):
    '''
    Test orientado a comprobar las funciones:
    - cargar_peliculas
    - cargar_generos
    '''

    data_peliculas = [
        # peliculas_1.csv
        'id,titulo,director,año_estreno,rating_promedio\n'
        '20,The Social Network,David Fincher,2010,7.7',
        # peliculas_2.csv
        'id,titulo,director,año_estreno,rating_promedio\n'
        '14,The Lion King,Roger Allers,1994,8.5\n'
        '15,The Avengers,Joss Whedon,2012,8.0\n'
        '16,Interstellar,Christopher Nolan,2014,8.6\n'
        '17,Gone with the Wind,Victor Fleming,1939,8.1\n'
        '18,Casablanca,Michael Curtiz,1942,8.5\n'
        '19,The Great Gatsby,Baz Luhrmann,2013,7.2',
        # peliculas_3.csv
        'id,titulo,director,año_estreno,rating_promedio\n'
        '7,The Matrix,Lana Wachowski,1999,8.7\n'
        '8,Goodfellas,Martin Scorsese,1990,8.7\n'
        '9,Schindler\'s List,Steven Spielberg,1993,8.9',
        # peliculas_4.csv
        'id,titulo,director,año_estreno,rating_promedio\n'
        '1,The Shawshank Redemption,Frank Darabont,1994,9.3\n'
        '2,The Godfather,Francis Ford Coppola,1972,9.2\n'
        '3,Pulp Fiction,Quentin Tarantino,1994,8.9\n'
        '4,The Dark Knight,Christopher Nolan,2008,9.0\n'
        '5,Fight Club,David Fincher,1999,8.8\n'
        '6,Inception,Christopher Nolan,2010,8.8\n'
        '10,Forrest Gump,Robert Zemeckis,1994,8.8\n'
        '11,The Silence of the Lambs,Jonathan Demme,1991,8.6\n'
        '12,The Lord of the Rings: The Fellowship of the Ring,Peter Jackson,2001,8.8\n'
        '13,The Departed,Martin Scorsese,2006,8.5'
    ]
    data_generos = [
        # generos_1.csv
        'genero,id_pelicula\n'
        'Drama,20',
        # generos_2.csv
        'genero,id_pelicula\n'
        'Animation,14\n'
        'Action,15\n'
        'Adventure,16\n'
        'Drama,17\n'
        'War,18\n'
        'Romance,19',
        # generos_3.csv
        'genero,id_pelicula\n'
        'Action,7\nSci-Fi,7\n'
        'Biography,8\nCrime,8\nDrama,8\n'
        'Biography,9\nDrama,9\nHistory,9',
        # generos_4.csv
        'genero,id_pelicula\n'
        'Drama,1\nCrime,1\n'
        'Drama,2\nCrime,2\n'
        'Drama,3\nCrime,3\n'
        'Action,4\nDrama,4\nCrime,4\n'
        'Drama,5\n'
        'Action,6\nDrama,6\n'
        'Action,7\nSci-Fi,7\n'
        'Biography,8\nCrime,8\nDrama,8\n'
        'Biography,9\nDrama,9\nHistory,9\n'
        'Drama,10\nRomance,10\n'
        'Drama,11\n'
        'Crime,12\nAdventure,12\nDrama,12\n'
        'Crime,13\nDrama,13'
    ]

    @classmethod
    def setUpClass(cls):
        '''
        Al inicio de la ejecución de los tests se crean los archivos
        necesarios para comprobar las función que cargan datos.
        '''

        for i in range(len(cls.data_peliculas)):
            with open(f'peliculas_{i + 1}.csv', 'w', encoding="UTF-8") as file:
                file.write(cls.data_peliculas[i])

            with open(f'generos_{i + 1}.csv', 'w', encoding="UTF-8") as file:
                file.write(cls.data_generos[i])

    @classmethod
    def tearDownClass(cls):
        '''
        Al finalizar la ejecución de los tests se eliminan
        los archivos creados anteriormente.
        '''

        for i in range(len(cls.data_peliculas)):
            remove(f'peliculas_{i + 1}.csv')
            remove(f'generos_{i + 1}.csv')

    def test_cargar_peliculas_1(self):
        '''
        Se comprueba que la función "cargar_peliculas" cargue correctamente
        las peliculas del archivo "peliculas_1.csv". Se puede revisar el contenido
        del archivo en el atributo de clase "data_peliculas".
        '''

        datos = funciones.cargar_peliculas('peliculas_1.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        pelicula = Pelicula(20, 'The Social Network', 'David Fincher', 2010, 7.7)
        self.assertSequenceEqual(lista_datos[0], pelicula)
        self.assertSequenceEqual(lista_datos[-1], pelicula)

    def test_cargar_peliculas_2(self):
        '''
        Se comprueba que la función "cargar_peliculas" cargue correctamente
        las peliculas del archivo "peliculas_2.csv". Se puede revisar el contenido
        del archivo en el atributo de clase "data_peliculas".
        '''

        datos = funciones.cargar_peliculas('peliculas_2.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        pelicula_1 = Pelicula(14, 'The Lion King', 'Roger Allers', 1994, 8.5)
        pelicula_2 = Pelicula(15, 'The Avengers', 'Joss Whedon', 2012, 8.0)
        pelicula_3 = Pelicula(16, 'Interstellar', 'Christopher Nolan', 2014, 8.6)
        pelicula_4 = Pelicula(17, 'Gone with the Wind', 'Victor Fleming', 1939, 8.1)
        pelicula_5 = Pelicula(18, 'Casablanca', 'Michael Curtiz', 1942, 8.5)
        pelicula_6 = Pelicula(19, 'The Great Gatsby', 'Baz Luhrmann', 2013, 7.2)
        self.assertSequenceEqual(lista_datos[0], pelicula_1)
        self.assertSequenceEqual(lista_datos[1], pelicula_2)
        self.assertSequenceEqual(lista_datos[2], pelicula_3)
        self.assertSequenceEqual(lista_datos[3], pelicula_4)
        self.assertSequenceEqual(lista_datos[4], pelicula_5)
        self.assertSequenceEqual(lista_datos[5], pelicula_6)

    def test_cargar_peliculas_3(self):
        '''
        Se comprueba que la función "cargar_peliculas" cargue correctamente
        las peliculas del archivo "peliculas_3.csv". Se puede revisar el contenido
        del archivo en el atributo de clase "data_peliculas".
        '''

        datos = funciones.cargar_peliculas('peliculas_3.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        pelicula_1 = Pelicula(7, 'The Matrix', 'Lana Wachowski', 1999, 8.7)
        pelicula_2 = Pelicula(8, 'Goodfellas', 'Martin Scorsese', 1990, 8.7)
        pelicula_3 = Pelicula(9, 'Schindler\'s List', 'Steven Spielberg', 1993, 8.9)
        self.assertSequenceEqual(lista_datos[0], pelicula_1)
        self.assertSequenceEqual(lista_datos[1], pelicula_2)
        self.assertSequenceEqual(lista_datos[2], pelicula_3)

    def test_cargar_peliculas_4(self):
        '''
        Se comprueba que la función "cargar_peliculas" cargue correctamente
        las peliculas del archivo "peliculas_4.csv". Se puede revisar el contenido
        del archivo en el atributo de clase "data_peliculas".
        '''

        datos = funciones.cargar_peliculas('peliculas_4.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        pelicula_2 = Pelicula(2, 'The Godfather', 'Francis Ford Coppola', 1972, 9.2)
        pelicula_13 = Pelicula(13, 'The Departed', 'Martin Scorsese', 2006, 8.5)
        self.assertSequenceEqual(lista_datos[1], pelicula_2)
        self.assertSequenceEqual(lista_datos[-1], pelicula_13)

    def test_cargar_generos_1(self):
        '''
        Se comprueba que la función "cargar_generos" cargue correctamente
        las peliculas del archivo "generos_1.csv". Se puede revisar el contenido
        del archivo en el atributo de clase "data_generos".
        '''

        datos = funciones.cargar_generos('generos_1.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        categoria = Genero('Drama', 20)
        self.assertSequenceEqual(lista_datos[0], categoria)
        self.assertSequenceEqual(lista_datos[-1], categoria)

    def test_cargar_generos_2(self):
        '''
        Se comprueba que la función "cargar_generos" cargue correctamente
        las peliculas del archivo "generos_2.csv". Se puede revisar el contenido
        del archivo en el atributo de clase "data_generos".
        '''

        datos = funciones.cargar_generos('generos_2.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        genero_1 = Genero('Animation', 14)
        genero_2 = Genero('Action', 15)
        genero_3 = Genero('Adventure', 16)
        genero_4 = Genero('Drama', 17)
        genero_5 = Genero('War', 18)
        genero_6 = Genero('Romance', 19)

        self.assertSequenceEqual(lista_datos[0], genero_1)
        self.assertSequenceEqual(lista_datos[1], genero_2)
        self.assertSequenceEqual(lista_datos[2], genero_3)
        self.assertSequenceEqual(lista_datos[3], genero_4)
        self.assertSequenceEqual(lista_datos[4], genero_5)
        self.assertSequenceEqual(lista_datos[5], genero_6)
        self.assertSequenceEqual(lista_datos[-1], genero_6)

    def test_cargar_generos_3(self):
        '''
        Se comprueba que la función "cargar_generos" cargue correctamente
        las peliculas del archivo "generos_3.csv". Se puede revisar el contenido
        del archivo en el atributo de clase "data_generos".
        '''

        datos = funciones.cargar_generos('generos_3.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        genero_1 = Genero('Action', 7)
        genero_2 = Genero('Sci-Fi', 7)
        genero_6 = Genero('Biography', 9)
        genero_7 = Genero('Drama', 9)
        genero_8 = Genero('History', 9)
        self.assertSequenceEqual(lista_datos[0], genero_1)
        self.assertSequenceEqual(lista_datos[1], genero_2)
        self.assertSequenceEqual(lista_datos[5], genero_6)
        self.assertSequenceEqual(lista_datos[6], genero_7)
        self.assertSequenceEqual(lista_datos[7], genero_8)
        self.assertSequenceEqual(lista_datos[-1], genero_8)

    def test_cargar_generos_4(self):
        '''
        Se comprueba que la función "cargar_generos" cargue correctamente
        las peliculas del archivo "generos_4.csv". Se puede revisar el contenido
        del archivo en el atributo de clase "data_generos".
        '''

        datos = funciones.cargar_generos('generos_4.csv')

        # Verificar tipo de dato pedido
        self.assertIsInstance(datos, Generator)
        lista_datos = list(datos)

        # Verificar resultados
        genero_1 = Genero('Drama', 1)
        genero_n = Genero('Drama', 13)
        self.assertSequenceEqual(lista_datos[0], genero_1)
        self.assertSequenceEqual(lista_datos[27], genero_n)
        self.assertSequenceEqual(lista_datos[-1], genero_n)
