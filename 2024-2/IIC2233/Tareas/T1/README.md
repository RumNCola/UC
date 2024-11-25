# Tarea 1: DCCultivo 🌱💧 por Fernando Jara G.

## Descripción:
DCCultivo es un juego compuesto por el módulo ```DCCutlivo.py``` y ```main.py```. Este contempla toda funcion, menu y test del enunciado, excepto el de detectar_plagas, donde el output es el mismo al del test pero en otro orden. 

## Cosas Implementadas y no implementadas
Las fucniones marcadas con ✅ son aquellas que corren y aprueban los tests.
### dccultivo.py: 

- clase Predio
    - crear_planos: ✅
    - plantar: ✅
    - regar: ✅
    - eliminar_cultivo: ✅

- clase DCCultivo
    - crear_predios: ✅ # Esta función funciona bien, pero en main.py tuve problemas con que vscode detectara ```predios.txt```, por lo que su direccion quedó como ```RumNCola-iic2233-2024-2\Tareas\T1\predios.txt``` (camino relativo segun vscode).
    - buscar_y_plantar: ✅
    - buscar_y_regar: ✅
    - detectar_plagas:  🟠 #detecta y elimina plagas, pero la lista que retorna tiene otro orden a la de los tests (pese a tener el mismo contenido).

### main.py

- menu(): ✅
La funcion menu muestra el menu de inicio, permitiendole al usuario decidir si cerrar el programa o crear su predio y comenzar el juego.

- menu_acciones(): ✅
menu_acciones muestra el menu de acciones, permitiendole al usuario decidir entre [1] visualizar predios, [2] plantar, [3] regar, [4] detectar plagas y [5] salir. Todas las funciones corren, a no ser que se entreguen parametros invalidos en los inputs. Por enunciado, se asume que solo se entregarán datos válidos.

- Menu de inicio crea predios con éxito y permite el cierre del programa
- El programa permite visualizar los predios con éxito
- El riego de predios funciona correctamente
- La búsqueda y eliminacion de plagas entrega los mismos resultados que los tests pero en otro orden
- Las opciones para cerrar el programa funcionan en el menu de inicio y menu de acciones
- Se incluyen algunos prints de Quality of Life para ver el estado de las acciones
- Se agregó la opcion para visualizar todos los predios ("all") en la opcion [1] del menu de acciones
- buscar_y_plantar aprueba tanto el test dificil como el sin solucion

### Otros:
##### ✅ Consola
##### ✅ Menú de Inicio
##### ✅ Menú de Acciones
##### ✅ Modularización
##### ✅ PEP8

### Posibles errores y aspectos no implementados:
- Todo aspecto fue implementado
- Los menus de acciones asumen que se entregarán datos validos (enunciado). La no entrega de estos puede generar que el programa se corte, dado que no todas las funciones contemplan esos casos.

Nota importante: en la linea 18 de main.py, la direccion ```predios.txt``` parece no funcionar correctamente, por lo que es importante tener esto en cuenta y probar alternativas. personalmente tuve que ser un poco más específico con el camino relativo.

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```predios.txt``` en ```RumNCola-iic2233-2024-2\Tareas\T1\predios.txt```. Este archivo es un txt con los predios a importar en main.py

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```utils.pyc```: contiene las funciones ```plagas()``` e ```imprimir_planos()``` usadas para el menu de acciones
2. ```os```: Se utiliza ```os.path.exists()``` para verificar la existencia de un archivo
3. ```sys```: Se utiliza la funcion ```sys.exit()``` para cerrar ```main.py```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:
1. ```dccultivo.py```: Contiene a ```DCCultivo```, ```Predio```, como clases. ```main.py``` gira en torno a estas clases y sus métodos

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:
1. Por enunciado, en los métodos de dccultivo.py, se asume que los parametros entregados para correr cada método serán válidos. (De todas formas
se agregaron algunas revisiones generales de esto). 
2. En detectar_plagas(...) se asume que el orden de los elementos de la lista de output no es relevante. Eliminar n plagas de P1 y despues eliminar m plagas de P2 es equivalente a hacerlo al revés.
3. No fue posible que main.py detectara predios.txt con su path relativo, por lo que tuve que hard-codearlo para que así fuera.

PD: Todo método y funcion de ```main.py``` y ```dccultivo.py``` contienen una descripción formal dentro de sus archivos respectivos. Esta descripción toma inspiracion de la oficial de python y describe las entradas, salidas, propositos, supuestos importantes y aspectos generales de cada método o funcion.

## Referencias de código externo :book:
1. //
