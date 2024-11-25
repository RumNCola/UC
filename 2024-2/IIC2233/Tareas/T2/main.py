from sys import exit, argv
import jardin
import plantas
import utilidades
import parametros as p
from copy import deepcopy

def inicio(nombre_jardin: str) -> None:
    """
    inicio crea un jardin segun los parametros entregados y llama a la función
    menu_inicio. Este método revisa si el jardin entregado es válido.
    """
    pool_plantas = utilidades.cargar_plantas('plantas.txt')
    jardins = utilidades.crear_jardin(nombre_jardin, 'jardines.txt', pool_plantas)
    if jardins.tablero == []:
        print('ERROR: Ingrese un nombre de jardin válido y ejecute nuevamete')
        return
    return menu_inicio(jardins)

def menu_inicio(jardins: object, dia= 0) -> None:
    """
    menu_inicio recibe un jardin y un dia y muestra el menu de inicio 
    y todas sus opciones a través de inputs interactivos.
    """
    if dia > p.DURACION:
        print('Fin del Juego!!!')
        print(f'Haz recaudado {jardins.soles} soles! Buen trabajo!')
        print(f'\t *** Asi terminó tu jardin ***')
        print(jardins)
        print('Gracias por jugar!')
        return
    print('----------------------------------')
    print('\t Menu de Inicio ')
    print('----------------------------------')
    print('\n')
    print(f'Soles disponibles: {jardins.soles}')
    print(f'Temperatura: {jardins.temperatura} °C')
    print(f'Día actual: {dia}')
    print('\n')
    print('[1] Menu Jardin')
    print('[2] Laboratorio')
    print('[3] Pasar Día')
    print('\n')

    print(f'[0] Salir del programa \n')
    opcion = (input('Opción: '))

    if opcion == '1':
        return menu_jardin(jardins, dia)
    elif opcion == '2':
        return menu_laboratorio(jardins, dia)
    elif (opcion) == '3':
        return simular_dia(jardins, dia)
    elif (opcion) == '0':
        print('\n Saliste de DCCampesiono, supongo que seguiras tu camino! \n Gracias por'
              f' ayudar a Hernán a combatir los Zombies!! \n')
        exit()
        
    else:
        print('Ingrese una opción válida >:/')
        return menu_inicio(jardins, dia)

def menu_jardin(jardins: object, dia: int) -> None:
    print('----------------------------------')
    print('\t Menu Jardín ')
    print('----------------------------------')

    print(jardins)

    print('\n')
    print('[1] Intercambiar')
    print('[2] Cultivar')
    print('[3] Regar')
    print('\n')
    print(f'[0] Volver al Menu de Inicio \n')
    opcion = (input('Opción: '))

    if opcion == '1':
        pos = input('Ingrese posiciones a intercambiar (formato x,y;w,z): ')
        pos = pos.replace(";", " ").replace(",", " ").split()
        if len(pos) != 4:
            print('Ingrese parametros válidos')
            return menu_jardin(jardins, dia)
        for elemento in pos:
            if not elemento.isdigit():
                print('Ingrese parametros válidos')
                return menu_jardin(jardins, dia)
        pos = [int(x) for x in pos]
        for i in range(len(pos)):
            if i == 0 or i == 2:
                if int(pos[i]) < 0 or pos[i] > len(jardins.tablero) - 1:
                    print('Ingrese parametros válidos')
                    return menu_jardin(jardins, dia) 
            else:
                if pos[i] < 0 or pos[i] > len(jardins.tablero[0]) - 1:
                    print('Ingrese parametros válidos')
                    return menu_jardin(jardins, dia)
        
        pos = [int(x) for x in pos]
        cambiaso = jardins.tablero[pos[0]][pos[1]]
        cambiaso_2 = jardins.tablero[pos[2]][pos[3]]
        jardins.tablero[pos[2]][pos[3]] = cambiaso
        jardins.tablero[pos[0]][pos[1]] = cambiaso_2
        return menu_jardin(jardins, dia)

    elif opcion == '2':
        numero_plantas = jardins.plantas_contar()
        disponibilidad = ([["S", numero_plantas["Solaretillo"]]])
        disponibilidad.append(["D", numero_plantas["Defensauce"]])
        disponibilidad.append(["P", numero_plantas["Potencilantro"]])
        disponibilidad.append(["A", numero_plantas["Aresauce"]])
        disponibilidad.append(["C", numero_plantas["Cilantrillo"]])
        disponibilidad.append(["F", numero_plantas["Fensaulantro"]])
        print(f'Plantas disponibles: ')
        print(f'[1] Solaretillo: {numero_plantas["Solaretillo"]}')
        print(f'[2] Defensauce: {numero_plantas["Defensauce"]}')
        print(f'[3] Potencilantro: {numero_plantas["Potencilantro"]}')
        print(f'[4] Aresauce: {numero_plantas["Aresauce"]}')
        print(f'[5] Cilantrillo: {numero_plantas["Cilantrillo"]}')
        print(f'[6] Fensaulantro: {numero_plantas["Fensaulantro"]}')
        print()
        print('[0] Volver a menu inicio \n')
        numero = input('Escoge el numero de planta a cultivar: ')

        if not numero.isdigit() or int(numero) > 6 or int(numero) < 1:
            print('ingrese un número válido')
            return menu_jardin(jardins, dia)
        elif numero == '0':
            return menu_inicio(jardins, dia)
        else:
            numero = int(numero) - 1

        if int(disponibilidad[numero][1]) == 0:
            print('No tienes esa planta :/')
            return menu_jardin(jardins, dia)
        else:
            ubicacion = input('Escoge la posicion donde quieres cultivar (formato x,y): ')
            ubicacion = ubicacion.replace(",", " ").split()
            if len(ubicacion) != 2:
                print('Ingrese input válido')
                return menu_jardin(jardins, dia)
            elif not ubicacion[0].isdigit() or not ubicacion[1].isdigit():
                print('Ingrese coordenadas válidas')
                return menu_jardin(jardins, dia)
            elif int(ubicacion[0]) > len(jardins.tablero) - 1:
                print('Ingrese coordenadas válidas')
                return menu_jardin(jardins,dia)
            elif int(ubicacion[1]) > len(jardins.tablero) - 1:
                print('Ingrese coordenadas válidas')
                return menu_jardin(jardins,dia)
            elif int(ubicacion[0]) < 0 or int(ubicacion[1]) < 0:
                print('Ingrese coordenadas válidas')
                return menu_jardin(jardins,dia)
            else:
                ubicacion = [int(x) for x in ubicacion]
                jardins.cultivar_planta(disponibilidad[numero][0], ubicacion[0], ubicacion[1])
                return menu_jardin(jardins, dia)
        
    elif opcion == '3':
        jardins.regar_plantas()
        return menu_jardin(jardins, dia)

    elif opcion == '0':
        print('\n Volviendo al menu jardin \n')
        return menu_inicio(jardins, dia)
    else:
        print('Ingrese una opcion válida \n')
        return menu_jardin(jardins, dia)
    
def menu_laboratorio(jardins: object, dia):
    print('=============================')
    print('\t   Laboratorio')
    print('=============================')
    print('\t  |Guía| \n')
    print('Solaretillo + Defensauce     = Aresauce')
    print('Solaretillo + Potencilantro  = Cilantrillo')
    print('Defensauce  + Potencilantro  = Fensaulantro \n')
    print('\t \t |Tienes| \n')
    inventario = jardins.contar_plantas_mutar()
    print('Solaretillo \t Defensauce \t Potencilantro')
    print(f' \t {inventario["S"]} \t    {inventario["D"]}  \t \t {inventario["P"]}')
    print('\t        | Mutaciones | \n')
    print('Aresauce \t Cilantrillo \t Fensaulantro')
    print('  [1]    \t    [2]      \t     [3] \n')
    print('[0] Volver al Menu principal')
    respuesta = input('Indique su mutación a crear: ')
    if respuesta == '1':
        jardins.mutar('S', 'D', 'A')
        return menu_laboratorio(jardins, dia)
    elif respuesta == '2':
        jardins.mutar('S', 'P', 'C')
        return menu_laboratorio(jardins, dia)
    elif respuesta == '3':
        jardins.mutar('D', 'P', 'F')
        return menu_laboratorio(jardins, dia)
    elif respuesta == '0':
        return menu_inicio(jardins, dia)
    else:
        print('Ingrese una opcion válida')
        return menu_laboratorio(jardins, dia)

def simular_dia(jardins, dia):
    dia += 1
    evento = utilidades.eleccion_evento(arg2, jardins)
    if evento == 1: #oleada
        #calcular soles
        temperatura = round(utilidades.calcular_temperatura(1))
        jardins.temperatura = temperatura
        utilidades.helada(jardins)
        utilidades.oleada(jardins)
        produccion_soles = utilidades.calcular_soles(jardins, False)
        jardins.soles += produccion_soles
        jardins.presentarse(temperatura)
        utilidades.llegada_plantas(jardins)
        return menu_inicio(jardins, dia)

    elif evento == 2: #helada
        temperatura = round(utilidades.calcular_temperatura(2))
        jardins.temperatura = temperatura
        utilidades.helada(jardins)
        utilidades.llegada_plantas(jardins)
        produccion_soles = utilidades.calcular_soles(jardins, True)
        jardins.soles += produccion_soles
        jardins.presentarse(temperatura)
        return menu_inicio(jardins, dia)

    elif evento == 0: #dia tranquilo
        temperatura = round(utilidades.calcular_temperatura(0))
        jardins.temperatura = temperatura
        utilidades.helada(jardins)
        produccion_soles = utilidades.calcular_soles(jardins, False)
        jardins.soles += produccion_soles
        utilidades.llegada_plantas(jardins)
        jardins.presentarse(temperatura)
        return menu_inicio(jardins, dia)

if len(argv) != 3:
    print('Error: Ingrese un número de argumentos válidos y ejecute nuevamente.')
else:
    arg0, arg1, arg2 = argv
    if type(arg1) == str:
        if arg2 == 'facil' or arg2 == 'intermedio' or arg2 == 'dificil':
            arg0, arg1, arg2 = argv
            inicio(arg1)
        else:
            print('Error: Ingrese una dificultad válida y ejecute nuevamente.')
    else:
        print('Error: Ingrese un jardin válido y ejecute nuevamente.')