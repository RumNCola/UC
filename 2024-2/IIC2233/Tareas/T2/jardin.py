import parametros as p
import random
from copy import deepcopy

class Jardin:
    def __init__(self, tablero: list[list], temperatura: int, pool: list[object], plantas= []):
        """
        inicializador recibe un tablero, temperatura un pool y en algunos casos una lista de
        plantas (inventario). Pool es una lista que contiene a las plantas importadas de 
        plantas.txt y self.pool_dict es la versión diccionario de este parametro. plantas
        es el inventario de plantas disponibles para plantar.
        """
        self._tablero = tablero
        self._plantas = plantas
        self._soles = p.SOLES_INICIO 
        if temperatura > 25:
            self._temperatura = 25
        else: 
            self._temperatura = max(-5, temperatura)
        self.pool = pool
        self.pool_dict = {}
        for i in range(len(self.pool)):
            self.pool_dict[self.pool[i].tipo] = self.pool[i]
    
    def __str__(self) -> str:
        """
        __str__  retorna como str el tablero e inventario de plantas de un jardins.
        """
        texto = ''
        for fila in self.tablero:
            texto += str(fila) + '\n'
        texto += 'Te quedan: \n'
        return f'{texto} \n {self.contar_plantas()} \n Inventario Plantas: \n {self.plantas}'
    
    @property
    def tablero(self) -> list[list]:
        return self._tablero
    @tablero.setter
    def tablero(self, matriz: list[list]) -> None:
        self._tablero = matriz
    
    @property
    def plantas(self) -> list:
        return self._plantas
    @plantas.setter
    def plantas(self, plantas_nuevas: list) -> None:
        """
        Cambia la lista de plantas. Tambien se empleará jardin.plantas.append(...)
        para cambios muy pequeños de ese estilo.
        """
        self._plantas = plantas_nuevas

    @property
    def temperatura(self) -> int:
        return self._temperatura
    
    @temperatura.setter
    def temperatura(self, nueva_temperatura: int) -> None:
        """
        temperatura.setter cambia la temperatura asegurandose que esta se mantenga en
        el intervalo [-5, 25].
        """
        if nueva_temperatura > 25:
            self._temperatura = 25
        else:
            self._temperatura = max(-5, nueva_temperatura)
    
    @property
    def soles(self) -> int:
        return self._soles
    
    @soles.setter
    def soles(self, nuevos_soles: int) -> None:
        """
        SETTER, edita los soles y se asegura que este valor nunca sea negativo
        """
        self._soles = max(0, nuevos_soles)

    def cultivar_planta(self, planta: str, coord_x, coord_y ) -> None:
        """
        cultivar_plantas recive un tipo de planta (str) y dos coordenadas.
        El método accede a pool para planar el tipo de planta en la ubicacion
        entregada.
        """
        if coord_x < 0 or coord_y < 0:
            print('Ingrese coordenadas válidas')
            return
        if coord_x > len(self.tablero) - 1 or coord_y > len(self.tablero[0]) - 1:
            print('Ingrese coordenadas válidas')
            return
        planta = self.pool_dict[planta]
        if planta in self.plantas:
            indice = self.plantas.index(planta)
            self.tablero[coord_x][coord_y] = deepcopy(self.plantas[indice])
            self.plantas.remove(planta) #CAMBIADO POR DEL; CHEQUEAR
        else:
            print('Cuidado! No posees es planta en tu inventario.')

    def regar_plantas(self) -> None:
        """
        regar_plantas riega todas las plantas del jardin, regenerando su vida.
        Esta funcion tira una moneda (indicatriz) y dependiendo del resultado, cura 
        a las plantas segun el parametro p.RIEGO_1 o p.RIEGO_2. Finalmente, se printea
        las plantas regadas, sus ubicaciones y el aumento de vida que cursaron.
        """
        indicatriz = random.randint(0,1)
        plantas_regadas = []
        if indicatriz == 1:
            for i in range(len(self.tablero)):
                for j in range(len(self.tablero[i])):

                    if self.tablero[i][j] != "X":
                        veggie = []
                        veggie.append(p.traductor[self.tablero[i][j].tipo])
                        veggie.append(self.tablero[i][j].vida)
                        self.tablero[i][j].vida += p.RIEGO_1
                        veggie.append(self.tablero[i][j].vida)
                        veggie.append(i)
                        veggie.append(j)
                        plantas_regadas.append(veggie)
        else:
            for i in range(len(self.tablero)):
                for j in range(len(self.tablero[i])):
                    if self.tablero[i][j] != "X":
                        veggie = []
                        veggie.append(p.traductor[self.tablero[i][j].tipo])
                        veggie.append(self.tablero[i][j].vida)
                        self.tablero[i][j].vida += p.RIEGO_2
                        veggie.append(self.tablero[i][j].vida)
                        veggie.append(i)
                        veggie.append(j)
                        plantas_regadas.append(veggie)
        print('\t ============================')
        print('\t  Se han regado tus plantas')
        print('\t ============================')
        for veggie in plantas_regadas:
            print(f'Se ha regado un {veggie[0]} en ({veggie[3]},{veggie[4]}) ha '\
                  f'subido su salud de {veggie[1]} a {veggie[2]}')

    def mutar(self, planta_1: str, planta_2: str, planta_output: str) -> None:
        """
        Mutar recibe dos nombres de planta y un str y agrega una planta nueva 
        al inventario. Esta chequea si planta_1 y planta_2 estan en el inventario y si 
        cumplen los requisitos para funcionarse en una planta_output.
        """
        if self.pool_dict[planta_1] not in self.plantas:
            print('Error: No cumples con los requisitos para la fusion')
        elif self.pool_dict[planta_2] not in self.plantas:
            print('Error: No cumples con los requisitos para la fusion')
        else:
            for veggie in self.plantas:
                if veggie.tipo == planta_1:
                    veggie1 = veggie
                    planta_1 = deepcopy(veggie)
                if veggie.tipo == planta_2:
                    veggie2 = veggie
                    planta_2 = deepcopy(veggie)
            tipo1 = planta_1.tipo
            tipo2 = planta_2.tipo

            if planta_output == "A":
                if (tipo1 == "S" and tipo2 == "D") or (tipo1 == "D" and tipo2 == "S"):
                    self.plantas.remove(veggie1)
                    self.plantas.remove(veggie2)
                    self.plantas.append((self.pool_dict['A']))
                else:
                    print('Esta fusión no es válida')

            elif planta_output == "C":
                if (tipo1 == "S" and tipo2 == "P") or (tipo1 == "P" and tipo2 == "S"):
                    self.plantas.remove(veggie1)
                    self.plantas.remove(veggie2)
                    self.plantas.append((self.pool_dict['C']))
                else:
                    print('Esta fusión no es válida')

            elif planta_output == "F":
                if (tipo1 == "D" and tipo2 == "P") or (tipo1 == "P" and tipo2 == "D"):
                    self.plantas.remove(veggie1)
                    self.plantas.remove(veggie2)
                    self.plantas.append((self.pool_dict['F']))
                else:
                    print('Esta fusión no es válida')
            
    def contar_plantas(self) -> str:
        """
        contar_plantas cuenta y printea las plantas del inventario. Si no se tienen
        plantas de cierto tipo, no se muestran.
        """
        dict = {}
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                if self.tablero[i][j] != "X":
                    if self.tablero[i][j].tipo not in dict:
                        dict[self.tablero[i][j].tipo] = 1
                    else:
                        dict[self.tablero[i][j].tipo] += 1
        texto = ''
        for llave in dict:
            texto += f'{dict[llave]} {p.traductor[str(llave)]} \n'
        return texto
    
    def plantas_contar(self) -> dict:
        """
        plantas_contar cuenta las plantas en self.plantas
        Este método si muestra las plantas que no tienes y
        returna un diccionario.
        """
        dict = {}
        dict["S"] = 0
        dict["D"] = 0
        dict["P"] = 0
        dict["P"] = 0
        dict["A"] = 0
        dict["C"] = 0
        dict["F"] = 0
        for veggie in self.plantas:
            dict[veggie.tipo] += 1
        nuevo_dict = {}
        for llave in dict:
            nuevo_dict[p.traductor[str(llave)]] = dict[llave]
        return nuevo_dict

    def contar_plantas_mutar(self) -> dict:
        """
        contar_plantas_mutar cuenta las plantas basicas para el menu
        de mutacion (laboratorio)
        """
        dict = {'S': 0, 'D': 0, 'P': 0}
        for veggies in self.plantas:
            if veggies.tipo == "S" or veggies.tipo == "D" or veggies.tipo == "P":
                dict[veggies.tipo] += 1
        return dict
    def contar_plantas_congeladas(self) -> int:
        plantas_congeladas = 0
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                if self.tablero[i][j] != "X":
                    if self.tablero[i][j].frozen == True:
                        plantas_congeladas += 1
        return plantas_congeladas

    def presentarse(self, temperatura) -> str:
        print('\t *** Este es tu Jardín actual ***')
        print(f'Temperatura: {temperatura} °C \n')
        print(self)
        congeladas = int(self.contar_plantas_congeladas())
        if congeladas == 0:
            print(f' Ninguna planta esta congelada!')
        else:
            print(f'Hay {congeladas} plantas congeladas!')
