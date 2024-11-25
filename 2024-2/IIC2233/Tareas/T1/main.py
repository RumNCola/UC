import dccultivo as dc
import sys
import utils

def menu() -> None:
    #Menu es una funcion que no recibe nada y retorna nada. 
    #Menu es un menu interactivo para el "juego" DCCultivo que visualiza el menu inicial, donde 
    # se puede iniciar o salir del juego

    print("""¡Bienvenido a DCCultivo!
          *** Menu de Inicio *** \n
          [1] Crear predios
          [2] Salir del programa \n """)
    opcion = input("Indique su opcion (1, 2): ")

    if opcion == "1":
        print("Creando cultivos! \n")
        cultivo = dc.DCCultivo()
        #No me funciono usando el path relativo
        cultivo.crear_predios("RumNCola-iic2233-2024-2\Tareas\T1\predios.txt") 
        menu_acciones(cultivo)
    
    elif opcion == "2":
        print("Saliendo de DCCultivo. Hasta pronto!")
        sys.exit() 
    else:
        print("Entregue una opcion válida \n")
        menu()

def menu_acciones(cultivo) -> None:
    #Menu_acciones() recibe y retorna None
    #Esta funcion es el menu interactivo del "juego" DCCultivo y lleva a cabo todas las acciones 
    # necesarias para correr el juego
    print()
    print("""¡Bienvenido a DCCultivo! \n Tu terreno está listo para trabajar
          
          ***Menú de Acciones *** \n
          [1] Visualizar predio
          [2] Plantar
          [3] Regar
          [4] Buscar y eliminar Plagas
          [5] Salir del programa \n """)
    opcion = input("Indique su opcion (1, 2, 3, 4, 5): ")

    if opcion == "1":
        codigos = []
        for predio in cultivo.predios:
            codigos.append(predio.codigo_predio)
        print("Predios Disponibles " + str(codigos))
        objetivo = input("Ingrese código de predio a visualizar (\"all\" para ver todos): ")
        if objetivo == "all":
            for predio in cultivo.predios:
                utils.imprimir_planos(predio)
            menu_acciones(cultivo)
        else:
            exito = False
            for predio in cultivo.predios:
                if predio.codigo_predio == objetivo:
                    exito = True
                    utils.imprimir_planos(predio)
            if exito == False:
                print("Ingrese un código de predio válido")
                menu_acciones(cultivo)
            else:
                menu_acciones(cultivo)
    elif opcion == "2":
        codigo_cultivo = input("Ingrese codigo a plantar: ")
        alto = int(input("Ingrese alto de cuadrante a plantar: "))
        ancho = int(input("Ingrese ancho de cuadrante a plantar: "))
        cultivo.buscar_y_plantar(codigo_cultivo, alto, ancho)
        menu_acciones(cultivo)

    elif opcion == "3":
        codigo_predio = input("Ingrese codigo de predio: ")
        x = int(input("Ingrese coordenada x de centro de riego: "))
        y = int(input("Ingrese coordenada y de centro de riego: "))
        coordenadas = [x,y]
        area = int(input("Ingrese area a regar: "))
        cultivo.buscar_y_regar(codigo_predio, coordenadas, area)
        menu_acciones(cultivo)

    elif opcion == "4":
        plagas = utils.plagas(cultivo)
        print("Plagas detectadas: ")
        print(plagas)
        bajas = cultivo.detectar_plagas(plagas)
        print("Plagas purgadas:")
        print(bajas)
        menu_acciones(cultivo)
    elif opcion == "5":
        print("Saliendo de DCCultivo, hasta pronto!")
        sys.exit()
    
    else:
        print("Ingrese una opcion válida")
        menu_acciones(cultivo)

menu()