import os 

class Predio:
    def __init__(self, codigo_predio: str, alto: int, ancho: int) -> None:
        self.codigo_predio = codigo_predio
        self.alto = alto
        self.ancho = ancho
        self.plano = []
        self.plano_riego = []

    def crear_plano(self, tipo: str) -> None:
        #Crear_plano, metodo de predios, recibe un string del tipo "normal" o "riego" y crea un 
        # plano del tipo entregado. 
        #La función usa lista de listas (matrices) donde el numero de listas es las filas y los 
        # elementos de cada sublista es las columnas
        #Esta funcion retorna None, pero altera el parametro self.plano y/o self.plano_riego
        if tipo == "normal":
            matriz = []
            for i in range(self.alto):
                i = []
                for j in range(self.ancho):
                    i.append("X")
                matriz.append(i)
            self.plano = matriz
            
        elif tipo == "riego":
            matriz = []
            for i in range(self.alto):
                i = []
                for j in range(self.ancho):
                    i.append(0)
                matriz.append(i)
            self.plano_riego = matriz
            
        else:
            print("Ingrese un tipo de plano válido")
            

    def plantar(self, codigo_cultivo: int, coordenadas: list, alto: int, ancho: int) -> None:
        #plantar es un metodo que recibe un codigo de planta, una lista de coordeandas, alto 
        # y ancho para realizar una plantacion dentro del predio.
        #Por enunciado, se asume que siempre se entregarán coordenadas, altos y anchos válidos.
        #  Es decir, no se haran plantaciones que excedan el predio
        #Esta funcion no retorna nada, pero cambia self.plano
        disponibilidad = True
        for i in range(alto):
            for j in range(ancho):
                if self.plano[coordenadas[0] + i][coordenadas[1] + j] != "X":
                    disponibilidad = False
        if disponibilidad == False:
            print("Ubicación no disponible para plantar :c")
            
        else:
            for i in range(alto):
                for j in range(ancho):                 
                    self.plano[coordenadas[0] + i][coordenadas[1] + j] = codigo_cultivo
            

    def regar(self, coordenadas: list, area: int) -> None:
        #regar recibe una lista de coordenadas y un int de área.
        #Este metodo riega el self.plano_riego de un predio, elevando en 1 los elementos a_ij 
        # dentro del "circulo" del área entregada
        #Esta funcion retorna None, pero cambia self.plano_riego 
        #Por enunciado, se asume que siempre se entregarán coordenadas válidas

        x = int(coordenadas[0])
        y = int(coordenadas[1])

        for i in range(-area, area + 1):
            for j in range(-area, area + 1):
                if abs(i) + abs(j) < 2 * area and 0 <= x + i < len(self.plano_riego):
                    if 0 <= y + j < len(self.plano_riego[0]):
                        self.plano_riego[x + i][y + j] += 1
        

    def eliminar_cultivo(self, codigo_cultivo: int) -> int:
        #eliminar_cultivo recibe un codigo de cultivo y elimina todos los cultivos del mismo 
        # código dentro del predio
        #Este metodo retorna el numero de cultivos eliminados. Adelante se les describirá como 
        # "bajas". Además, altera self.plano
    
        bajas = 0
        for i in range(self.alto):
            for j in range(self.ancho):
                if self.plano[i][j] == codigo_cultivo:
                    self.plano[i][j] = "X"
                    bajas += 1
        return bajas

    def factibilidad_codigo(self, codigo_cultivo: int) -> bool:
        #Funcion AUXILIAR. Recibe un código de cultivo y revisa si ya existe una plantacion 
        # de tal codigo en el predio.
        #factibilidad_codigo retorna True si es factible hacer una plantacion de codigo_cultivo 
        # en el predio (Esta funcion sirve 
        #para buscar y plantar)
        for i in range(self.alto):
            for j in range(self.ancho):
                if self.plano[i][j] == codigo_cultivo:
                    return False
        return True

class DCCultivo:
    def __init__(self) -> None:
        self.predios = []

    def crear_predios(self, nombre_archivo: str) -> str:
        #Esta funcion recibe un nombre de archivo y crea los predios definidos dentro de
        #  tal documento.
        #crear_predios returna un string indicando el exito o fracaso de la operacion. Además, 
        # este método verifica si el archivo 
        #entregado existe o no
        #Además, crear_predios evita los casos triviales donde alto o ancho es 0 
        if os.path.exists(nombre_archivo):
            file = open(nombre_archivo, "r")
            grilla = []

            for linea in file:
                predio = linea.strip().split(",")
                codigo_predio = predio[0]
                alto = int(predio[1])
                ancho = int(predio[2])
                if alto > 0 and ancho > 0: 
                    predius = Predio(codigo_predio, alto, ancho)
                    predius.crear_plano("normal")
                    predius.crear_plano("riego")
                    grilla.append(predius)
            self.predios = grilla
            return "Predios de DCCultivo cargados exitosamente"
        else:
            return "Fallo en la carga de DCCultivo"

    def buscar_y_plantar(self, codigo_cultivo: int, alto: int, ancho: int) -> bool:
        #Buscar_y_plantar recibe un codigo de planta, alto y ancho y revisa todos los predios
        #  de un DCCultivo para plantar.
        #Esta funcion retorna un booleano que será vedadero si se planta con exito y 
        # será falso en otro caso
        #Esta funcion busca a_ij disponibles para plantar, para despues evaluar su vecindad. 
        # Si la vecindad esta dentro del predio y esta totalmente disponible, se planta
        #Además, esta funcion revisa con factibilidad_codigo que no se repitan codigos_cultivo
        #  en cada predio

        for predio in self.predios:
            if predio.factibilidad_codigo(codigo_cultivo):
                for i in range(predio.alto - alto + 1):
                    for j in range(predio.ancho - ancho + 1):
                        if predio.plano[i][j] == "X":
                            vecindad_disponible = True

                            for k in range(alto):
                                for m in range(ancho):
                                    if predio.plano[i + k][j + m] != "X":
                                        vecindad_disponible = False
                                        break
                                if not vecindad_disponible:
                                    break
                            if vecindad_disponible:
                                predio.plantar(codigo_cultivo, [i,j], alto, ancho)
                                print("Plantado con exito c:")
                                return True
        print("No se pudo plantar :C")
        return False
    
    def buscar_y_regar(self, codigo_predio: str, coordenadas: list, area: int) -> None:
        #buscar_y_regar recibe un codigo_predio, coordenadas (en forma de lista) y un area.
        #  Este metodo riega el predio segun los parametros entregados
        #el metodo retorna None pero altera el parametro predio.plano_riego
        for predio in self.predios:
            if predio.codigo_predio == codigo_predio:
                predio.regar(coordenadas, area)
        return

    def detectar_plagas(self, lista_plagas: list[list]) -> list[list]:
        #Detectar_plagas recibe una lista de listas que contiene el predio donde esta la plaga 
        # y la coordenada donde esta. Esta funcion encuentra la plaga y elimina todos los
        #  cultivos del mismo codigo al cultivo que tiene la plaga.
        #el metodo retorna una lista de listas que contiene el numero de bajas por cada predio
        #Si hay una plaga en un lugar donde no hay cultivo (hay "X"), el metodo no eliminará nada

        #NOTA IMPORTANTE: Este metodo funciona, pero es rechazado por los tests porque retorna la 
        # misma lista pero en otro orden.
        resultado = []

        for predio in self.predios:
            bajas = 0
            for plaga in lista_plagas:
                id_predio = plaga[0]
                ubicacion_plaga = plaga[1]
                if id_predio == predio.codigo_predio:
                    cultivo_envenenado = predio.plano[ubicacion_plaga[0]][ubicacion_plaga[1]]
                    if cultivo_envenenado != "X":
                        bajas += predio.eliminar_cultivo(cultivo_envenenado)
            resultado.append([predio.codigo_predio, bajas])
        return resultado
