# Tarea 3: Little DCCaesars 🧟🍕

#### Por Fernando Jara G. - Github: RumNCola - Sección 4


## Lista de Supuestos/Consideraciones generales :thinking: :
1. Para ganancia_total_de_un_local se realiza el redondeo al final de toda la operación. Esto dado que los tests asi lo revisaban.
2. En gasto_cliente_por_mes se redondea el valor de gasto mensual al final del cálculo.
3. Para consultas anidads, se definio el diccionario funciones y la funcion auxiliar revisar_instrucciones. Todo esto de acuerdo a lo mencionado en el Issue 510.


## Aspectos implementados y posibles erroes ✅:
- El programa pusheado cumple con todos los tests, implementando correctamente todos los aspectos del enunciado.    

## Ejecucion :computer:
- El módulo principal a ejecutar es consultas.py
- utilidades.py contiene las namedtuples necesarias para la ejecucion 
- consultas.py incluye las funciones necesarias para el módulo principal.
- La carpeta data contiene archivos csv con información para las tuplas asociadas a pedidos, locales, contenidos_pedidos y pizzas. Esto de la forma <data/tamaño/archivo.csv>

## Archivos importantes :memo::
- Para la ejecución correcta de consultas.py se debe tener a los siguientes archivos dentro de la misma carpeta que consultas.py:
    * consultas.py
    * utilidades.py

## Librerias :book::
### Librerias Externas
- <functools - reduce>: Esta función se utiliza para simplificar el procesado de funciones que reciben un único generador
- <collections - defaultdict>: Esta función se utiliza para simplificar el procesado de multiples generadores

Para esta tara no se implementaron librerias propias

## Referencias de código externo :book:
Para realizar mi tarea saqué código de:
1. \<https://github.com/IIC2233/Syllabus/issues/510#issuecomment-2411088048>: De acuerdo a esta Issue, se implemento en las lineas <321 - 345> de <consultas.py>, el diccionario <funciones> que contiene todas las funciones de consultas.py. Esto con el objetivo de cargar las consultas anidadas. Además, se desarrolló la funcion auxiliar revisar_instrucciones que permite procesar este diccionario y el argumento entregado en consulta_anidada.
2. \<https://www.w3schools.com/python/ref_list_extend.asp >Para multiples funciones, se usó el método extend de la clase list. Esto con el objetivo de fusionar listas con el menor consumo de memoria posible.