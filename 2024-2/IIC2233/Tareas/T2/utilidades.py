import jardin
import parametros as p
import plantas
import random
from copy import deepcopy

#Funciones auxiliares para incorporacion de plantas.txt y creacion de jardin

def validez_parametros(parametros :list) -> bool:
    """
    Funcion auxiliar que revisa si los parametros de una planta son válidos.
    Si todos los parametros son válidos, retorna True. Si algun parametro no es válido,
    retorna False. Esta función asume que los parametros se entregan en el orden indicado
    en el enunciado.
    """
    if len(parametros[0]) != 1 or parametros[0] not in p.traductor:
        return False
    if int(parametros[1]) > 100 or int(parametros[1]) < 0:
       return False
    if 0 > int(parametros[2]) or int(parametros[2]) > int(parametros[1]):
        return False
    if 0 > int(parametros[3])  or int(parametros[3]) > 40:
        return False
    if -5 > int(parametros[4]) or int(parametros[4]) > 25:
        return False
    if int(parametros[5]) not in [0,1]:
        return False
    if 0 > int(parametros[6]) or int(parametros[6]) > 30:
        return False
    return True

def instanciar_planta(lista_stats: list) -> object:
    """
    instanciar_plantas recibe una lista con 7 parametros de una planta y 
    crea la instancia usando la clase de planta adecuada. Este se asegura
    que toda planta a ser creada no este congelada.
    """
    lista_stats[5] = 0
    if lista_stats[0] == "S":
        return plantas.Solaretillo(*lista_stats)

    elif lista_stats[0] == "D":
        return plantas.Defensauce(*lista_stats)

    elif lista_stats[0] == "P":
        return plantas.Potencilantro(*lista_stats)

    elif lista_stats[0] == "A":
        return plantas.Aresauce(*lista_stats)

    elif lista_stats[0] == "C":
        return plantas.Cilantrillo(*lista_stats)

    elif lista_stats[0] == "F":
        return plantas.Fensaulantro(*lista_stats)

def cargar_plantas(ruta_archivo: str) -> object:
    """
    cargar_plantas recibe una ruta de archivo y carga las plantas 
    válidas presentes en tal archivo.
    """
    archivo = open(ruta_archivo, 'r')
    pool_plantas = []
    for linea in archivo.readlines():
        linea = linea.replace(";", " ").split()
        if validez_parametros(linea):
            linea[1:] = [int(parametro) for parametro in linea[1:]]
            pool_plantas.append(instanciar_planta(linea))
    return pool_plantas  

def crear_jardin(nombre_jardin: str, ruta: str, pool_plantas) -> object:
    """
    crear_jardin recibe una ruta de archivo y crea un jardín. Esta funcion
    crea un jardín de acuerdo a los argumentos entregados
    """
    archivo = open(ruta, "r")
    tablerou = []
    for linea in archivo.readlines():
        linea = linea.replace("!", " ").replace(";", " ").split()
        if str(linea[0]) == nombre_jardin:
            for elemento in linea[1:]:
                elemento = elemento.replace(",", " ").split()
                tablerou.append(elemento)
    for i in range(len(tablerou)):
        for j in range(len(tablerou[i])):
            if tablerou[i][j] == "S":
                for vegetal in pool_plantas:
                    if vegetal.tipo == "S":
                        tablerou[i][j] = deepcopy(vegetal)

            if tablerou[i][j] == "D":
                for vegetal in pool_plantas:
                    if vegetal.tipo == "D":
                        tablerou[i][j] = deepcopy(vegetal)
                
            if tablerou[i][j] == "P":
                for vegetal in pool_plantas:
                    if vegetal.tipo == "P":
                        tablerou[i][j] = deepcopy(vegetal)
                
            if tablerou[i][j] == "A":
                for vegetal in pool_plantas:
                    if vegetal.tipo == "A":
                        tablerou[i][j] = deepcopy(vegetal)
            if tablerou[i][j] == "C":
                for vegetal in pool_plantas:
                    if vegetal.tipo == "C":
                        tablerou[i][j] = deepcopy(vegetal)
            
            if tablerou[i][j] == "F":
                for vegetal in pool_plantas:
                    if vegetal.tipo == "F":
                        tablerou[i][j] = deepcopy(vegetal)
                
    return jardin.Jardin(tablerou, p.TEMP_INICIAL, pool_plantas)

#Funciones auxiliares para eventos y simular dias

def llegada_plantas(jardins: object) -> None:
    """
    llegada_plantas recibe un jardin y de acuerdo a su pool de plantas,
    agrega plantas al inventario de este jardin. Este hace que los 
    Solaretillos que llegan tengan potenciales diferentes y alturas diferentes
    para traer variedad a la produccion solar.
    """
    numero_plantas = random.randint(p.NUM_MIN_PLANTA, p.NUM_MAX_PLANTA)
    for i in range(numero_plantas):
        selector = random.randint(1, 3)
        if selector == 1:
            veggie = jardins.pool_dict["S"]
            potencial = random.randint(p.POTENCIAL_SOLARETILLO_MIN, p.POTENCIAL_SOLARETILLO_MAX)
            veggie.potencial = potencial
            veggie.altura = random.randint(1,30)
            jardins.plantas.append(veggie)
        elif selector == 2:
            jardins.plantas.append(jardins.pool_dict["D"])
        elif selector == 3:
            jardins.plantas.append(jardins.pool_dict["P"])
    print(f'\n \t *** Han llegado {numero_plantas} plantas a tu inventario *** \n')

def calcular_temperatura(evento: int) -> int:
    """
    calcular_temperatura calcula y entrega la temperatura segun parametros.py. 
    Si ocurre una helada, la temperatura se generará de diferente forma.
    """
    if evento == 2:
        return random.uniform(p.TEMP_MIN_HELADA, p.TEMP_MAX_HELADA)
    else:
        return random.randint(p.TEMP_MIN_JARDIN, p.TEMP_MAX_JARDIN)
    
def calcular_reduccion_ataque(jardins: object) -> float:
    """
    calcular_reduccion_ataque cuenta los Fensaulantros plantados y retorna la probabilidad 
    actualizada de que ocurra una oleada de zombies.
    """
    fencilantros = 0
    for i in range(len(jardins.tablero)):
        for j in range(len(jardins.tablero[i])):
            if jardins.tablero[i][j] != "X":
                if jardins.tablero[i][j].tipo == "F":
                    fencilantros += 1
    return (1 - p.RED_ATQ / 100) ** fencilantros
    
def eleccion_evento(dificultad: str, jardins: object ) -> None:
    """
    eleccion_evento elige un evento de acuerdo a la dificultad entregada.
    Si hay oleada, retorna 1. Si hay helada, retorna 2 y si no ocurre nada, retorna 0.
    """
    archivo = open('eventos.txt', 'r')
    lineas = archivo.readlines()
    lineas[0] = lineas[0].replace(";", " ").split()
    lineas[1] = lineas[1].replace(";", " ").split()
    if dificultad == 'facil':
        prob_oleada = float(lineas[0][1])
        prob_helada = float(lineas[1][1])

    elif dificultad == 'intermedio':
        prob_oleada = float(lineas[0][2])
        prob_helada = float(lineas[1][2])

    elif dificultad == 'dificil':
        prob_oleada = float(lineas[0][3])
        prob_helada = float(lineas[1][3])

    debuff_oleada = calcular_reduccion_ataque(jardins)
    prob_oleada *= debuff_oleada

    decision = random.choices([0,1], [1 - prob_oleada, prob_oleada])[0]
    if decision == 1:
        print('==================================================================')
        print('\t Se ha activado el evento Oleada!')
        print('==================================================================')
        print('\t Preparense para el ataque!')
        return 1
    decision_2 = random.choices([0,1], [1 - prob_helada, prob_helada])[0]
    if decision_2 == 1:
        print('==================================================================')
        print('\t Se ha activado el evento Helada!')
        print('==================================================================')
        print('\t Las plantas con baja temperatura verán reducida su producción')
        return 2
    else:
        print('==================================================================')
        print('\t Día tranquilo')
        print('==================================================================')
        return 0

def bajas(jardins: object) -> None:
    """
    bajas edita un jardin, removiendo las plantas muertas.
    """
    for i in range(len(jardins.tablero)):
        for j in range(len(jardins.tablero[i])):
            if jardins.tablero[i][j] != "X":
                if jardins.tablero[i][j].status == False:
                    jardins.tablero[i][j] = "X"

def calcular_robo(jardins: object, ataques_exitosos: int) -> int:
    """
    calcular_robo calcula los soles robados de un jardin dado ataques_exitosos
    """
    aresoces = 0
    for i in range(len(jardins.tablero)):
        for j in range(len(jardins.tablero[i])):
            if jardins.tablero[i][j] != "X":
                if jardins.tablero[i][j].tipo == "A":
                    aresoces += 1
    robo = p.SOLES_ROBADOS * ataques_exitosos * (1 - p.ANTI_ROBO / 100) ** aresoces
    return round(robo)


def oleada(jardins: object) -> None:
    """
    oleada simula una oleada de zombies en un jardin y remueve las plantas
    muertas.
    """
    print('==================================')
    print(f'Durante la noche pasó una oleada de {p.ZOMBIES_DIFICULTAD} zombis!')
    print('==================================')
    exito_ataques = 0
    for i in range(p.ZOMBIES_DIFICULTAD):
        x = random.randint(0, len(jardins.tablero) - 1)
        y = random.randint(0, len(jardins.tablero[x]) - 1)
        veggie = jardins.tablero[x][y]
        if veggie != "X":
            daño = max(1, round(p.ATAQUE * (40 - veggie.res) / 40))
            jardins.tablero[x][y].recibir_daño(daño, x, y)
            exito_ataques += 1
            bajas(jardins)
        else:
            print(f'¡Un zombie intentó atacar la posición ({x},{y}) pero estaba vacía!')
    robo = calcular_robo(jardins, exito_ataques)
    if robo > jardins.soles:
        robo = jardins.soles
    if exito_ataques > 0:
        print(f'Ls zombies lograron atacar {exito_ataques} casillas, robando {robo} soles')
    else:
        print(f' “¡Ninguna de tus plantas fue atacada! No has sufrido robos de soles”')
    jardins.soles -= robo
    
def helada(jardins: object) -> None:
    """
    helada se asegura que las plantas con menor res. termica a la temperatura
    actual se congelen. Además, descongela a las plantas que entren en calor.
    Por esto, este metodo se ejecutará independiente del evento ocurrido.
    """
    for i in range(len(jardins.tablero)):
        for j in range(len(jardins.tablero[i])):
            if jardins.tablero[i][j] != "X":
                if jardins.tablero[i][j].res_termica > jardins.temperatura:
                    jardins.tablero[i][j].frozen = True
                else:
                    jardins.tablero[i][j].frozen = False
    
def hay_potencilantro(jardins: object, x: int, y: int) -> bool:
    """
    hay_potencilantro retorna true si hay un potencilantro o Fensaulantro adyacente a
    la casilla (x,y)
    """
    for i in range(max(x - 1, 0), min(len(jardins.tablero), x + 2)):
        for j in range(max(y - 1, 0), min(len(jardins.tablero[i]), y + 2)):
                if x == i and y == j:
                    continue
                if jardins.tablero[i][j] != "X":
                    if jardins.tablero[i][j].tipo in ("F", "P"): 
                        return True
    return False

def hay_cilantrillo(jardins: object, x: int, y: int) -> bool:
    """
    hay_cilantrillo retorna true si hay un cilantrillo adyacente a a las coordenadas
    x,y del tablero del jardin.
    """
    for i in range(max(x - 1, 0), min(len(jardins.tablero), x + 2)):
        for j in range(max(y - 1, 0), min(len(jardins.tablero[i]), y + 2)):
            if x == i and y == j:
                continue
            if jardins.tablero[i][j] != "X":
                if jardins.tablero[i][j].tipo == "C":
                    return True
    return False


def calcular_soles(jardins: object, helada: bool) -> int:
    """
    calcular_soles recibe un jardin y retorna los soles producidos.
    """
    print('======================================')
    print('\t Se ha iniciado la producción de soles')
    print('======================================')
    soles = 0

    for i in range(len(jardins.tablero)):
        for j in range(len(jardins.tablero[i])):
            veggie = jardins.tablero[i][j]

            if veggie != "X" and helada == False:
                #1. Hay un solaretillo o un aresauce
                if veggie.tipo == "S" or veggie.tipo == "A":
                    nombre = p.traductor[veggie.tipo]
                    if hay_cilantrillo(jardins, i, j):
                        buff = (1 + p.AUM_AUM_CIL / 100) 
                        buff *= (1 + p.AUMENTO_NUTRIENTE / 100)
                        generacion = jardins.tablero[i][j].producir_soles(jardins.temperatura)   
                        generacion *= buff
                        soles += round(generacion)
                        print(f'Un {nombre} ({i},{j}) ha producido {round(generacion)} soles.')              
                    elif hay_potencilantro(jardins, i, j):
                        buff = (1 + p.AUMENTO_NUTRIENTE / 100)
                        generacion = jardins.tablero[i][j].producir_soles(jardins.temperatura)
                        generacion *= buff 
                        soles += round(generacion)
                        print(f'Un {nombre} ({i},{j}) ha producido {round(generacion)} soles.')
                    else: #Caso 3: No hay ningun tipo de cilantro
                        generacion = jardins.tablero[i][j].producir_soles(jardins.temperatura)
                        soles += round(generacion)
                        print(f'Un {nombre} ({i},{j}) ha producido {round(generacion)} soles.')
                #Hay un Cilantrillo
                if veggie.tipo == "C":
                        #Caso 2: hay un potencilantro o Aresauce
                        generacion = jardins.tablero[i][j].producir_soles(jardins.temperatura)
                        soles += round(generacion)
                        print(f'Un Cilantrillo ({i},{j}) ha producido {round(generacion)} soles.')

            elif veggie != "X" and helada == True:
                 #1. Hay un solaretillo o un aresauce
                if veggie.tipo == "S" or veggie.tipo == "A":
                    nombre = p.traductor[veggie.tipo]
                    if not veggie.frozen:   
                        if hay_cilantrillo(jardins, i, j):
                            buff = (1 + p.AUM_AUM_CIL / 100) * (1 + p.AUMENTO_NUTRIENTE / 100)
                            generacion = jardins.tablero[i][j].producir_soles(jardins.temperatura) 
                            generacion *= buff  
                            soles += round(generacion + p.SOLES_EXTRA_HELADA)
                            print(f'Un {nombre} ({i},{j}) no se ha congelado y producido'
                                  f'{round(generacion)} soles.')
                        elif hay_potencilantro(jardins, i, j):
                            buff = (1 + p.AUMENTO_NUTRIENTE / 100)
                            generacion = jardins.tablero[i][j].producir_soles(jardins.temperatura)
                            generacion *= buff
                            soles += round(generacion + p.SOLES_EXTRA_HELADA)
                            print(f'Un {nombre} ({i},{j}) ha producido {round(generacion)}' 
                                  f'soles.')
                        else: #Caso 3: No hay ningun tipo de cilantro
                            generacion = jardins.tablero[i][j].producir_soles(jardins.temperatura)
                            soles += round(generacion + p.SOLES_EXTRA_HELADA)
                            print(f'Un {nombre} ({i},{j}) ha producido {round(generacion)}'
                                  f' soles.')
                    else:
                        print(f'Un {nombre} ({i},{j}) congelado no ha producido soles.')
                #Hay un Cilantrillo
                if veggie.tipo == "C":
                        if not veggie.frozen:
                            #Caso 2: hay un potencilantro o Aresauce
                            generacion = jardins.tablero[i][j].producir_soles(jardins.temperatura)
                            soles += round(generacion + p.SOLES_EXTRA_HELADA)
                            print(f'Un Cilantrillo ({i},{j}) ha producido {round(generacion)}'
                                  f' soles.')
                        else:
                            print(f'Un Cilantrillo ({i},{j}) congelado no ha producido soles.')

    soles_cielo = random.randint(p.MIN_SOLES, p.MAX_SOLES)
    soles += soles_cielo
    print(f'Han caido {soles_cielo} del cielo')
    return round(soles)