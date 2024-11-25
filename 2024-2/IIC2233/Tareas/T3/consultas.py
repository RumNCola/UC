from typing import Any, Generator, Iterable
from utilidades import Pizzas, Locales, ContenidoPedidos, Pedidos
from functools import reduce
from collections import defaultdict

# Carga de datos
def cargar_pizzas(path: str) -> Generator:
    with open(path, 'r', encoding='UTF-8') as archivo:
        archivo.readline()
        for linea in archivo:
            linea = linea.strip().split(',')
            yield Pizzas(linea[0], linea[1], int(linea[2]))

def cargar_locales(path: str) -> Generator:
    with open(path, 'r', encoding='UTF-8') as archivo:
        archivo.readline()
        for linea in archivo:
            linea = linea.strip().split(',')
            yield Locales(int(linea[0]), linea[1], linea[2], linea[3], int(linea[4]))

def cargar_pedidos(path: str) -> Generator:
    with open(path, 'r', encoding='UTF-8') as archivo:
        archivo.readline()
        for linea in archivo:
            linea = linea.strip().split(',')
            yield Pedidos(int(linea[0]), int(linea[1]), int(linea[2]), linea[3], linea[4])

def cargar_contenido_pedidos(path: str) -> Generator:
    with open(path, 'r', encoding='UTF-8') as archivo:
        archivo.readline()
        for linea in archivo:
            linea = linea.strip().split(',')
            yield ContenidoPedidos(int(linea[0]), linea[1], int(linea[2]), float(linea[3]))

def pedidos_con_al_menos_esta_pizza(
        generador_contenido_pedidos: Generator,
        tipo_de_pizza: str
        ) -> Iterable:
    return filter(lambda x: (tipo_de_pizza == x.nombre.split('_')[0]), generador_contenido_pedidos)

# Consultas que ocupan 1 generador
def cantidad_vendida_de_pizza_por_tipo(
        generador_contenido_pedidos: Generator,
        tipo_de_pizza: str
        ) -> int:
    return reduce(lambda x,y: (x + y), 
                  map(lambda x: x.cantidad, 
                      filter(lambda x: (x.nombre.split('_')[0] == tipo_de_pizza), 
                             generador_contenido_pedidos)), 0)

def pedido_con_mayor_descuento_utilizado(
        generador_contenido_pedidos: Generator
        ) -> Iterable:
    pedidos = [pedido for pedido in generador_contenido_pedidos]
    descuento = reduce(lambda x,y: max(x,y), map(lambda x: x.descuento, pedidos), 0)
    return [pedido for pedido in filter(lambda x: x.descuento == descuento, pedidos)]

def ajustar_precio_segun_ingredientes(
        generador_pizzas: Generator,
        ingrediente: str,
        diferencia_precio: int
        ) -> Iterable:
    
    ajuste = lambda x: (max(7000, x + diferencia_precio))
    return [Pizzas(pizza[0], pizza[1], ajuste(pizza[2])) 
            for pizza in generador_pizzas if ingrediente in pizza[1].split(';')]

def clientes_despues_hora(
        generador_pedidos: Generator,
        hora: str
        ) -> str:
    try:
        return reduce(lambda x,y: x + ' ' + y, 
                      map(lambda x: str(x), map(lambda x: (x.id_cliente), 
                                                filter(lambda x: x.hora[:5] >= hora, 
                                                       generador_pedidos))))
    except TypeError:
        return ''
    
def cliente_indeciso(
        generador_pizzas: Generator,
        ingrediente_no_deseado: str,
        cantidad_pizzas: int
        ) -> Iterable:
    resultado = [i for i in 
                 filter(lambda x: ingrediente_no_deseado not in x.ingredientes.split(';'), 
                        generador_pizzas)]
    
    if resultado == []:
        return []
    
    while len(resultado) < cantidad_pizzas:
        resultado.extend(resultado)

    if len(resultado) > cantidad_pizzas:
        return resultado[:cantidad_pizzas]
    
    elif len(resultado) == cantidad_pizzas:
        return resultado

def pizzas_con_ingrediente(
        generador_pizzas: Generator,
        ingrediente: str
        ) -> Iterable:
    return [i for i in filter(lambda x: ingrediente in x.ingredientes.split(';'), 
                              generador_pizzas)]

def pizzas_pagables_de_un_tamano(
        generador_pizzas: Generator,
        dinero: int,
        tamano: str
    ) -> Iterable:
    return [i for i in filter(lambda x: x.precio <= dinero, 
                              filter(lambda x: x.nombre.split('_')[1] == tamano, 
                                     generador_pizzas))]

def cantidad_empleados_pais(
        generador_locales: Generator,
        pais: str
        ) -> int:
    return reduce(lambda x,y: x + y, 
                  map(lambda x: x.cantidad_trabajadores, 
                      filter(lambda x: x.pais == pais, generador_locales)), 0)

# Consultas que ocupan 2 Generadores
def ganancias_producidas_en_los_pedidos(
        generador_contenido_pedidos: Generator,
        generador_pizzas: Generator
        ) -> Iterable:
    
    precios = {pizza.nombre: pizza.precio for pizza in generador_pizzas}
    ganancias_pedidos = defaultdict(float)
    for pedido in generador_contenido_pedidos:
        ganancias_pedidos[pedido.id_pedido] += round(pedido.cantidad * precios[pedido.nombre]
                                                      * (1 - pedido.descuento))
    return [(venta[0], int(venta[1])) for venta in ganancias_pedidos.items()]
   
def pizza_mas_vendida_del_dia(
        generador_contenido_pedidos: Generator, 
        generador_pedidos: Generator,
        fecha: str
        ) -> set:
    
    pedidos_validos = set(map(lambda x: x.id_pedido, 
                              filter(lambda x: x.fecha == fecha, generador_pedidos)))
    pizzas_pedidas = defaultdict(int)
    for pedido in filter(lambda x: x.id_pedido in pedidos_validos, generador_contenido_pedidos):
        pizzas_pedidas[pedido.nombre.split('_')[0]] += pedido.cantidad
    try:
        mas_vendida = max(pizzas_pedidas.values())
        return [pizza[0] for pizza in pizzas_pedidas.items() if pizza[1] == mas_vendida]
    except ValueError:
        return []
       
def pizza_del_mes(
        generador_pedidos: Generator,
        generador_contenido_pedidos: Generator,
        mes: str
        ) -> str:
    
    pedidos_validos = set(map(lambda x: x.id_pedido, 
                              filter(lambda x: x.fecha[5:7] == mes, generador_pedidos)))
    pizzas_pedidas = defaultdict(int)
    for pedido in filter(lambda x: x.id_pedido in pedidos_validos, generador_contenido_pedidos):
        pizzas_pedidas[pedido.nombre.split('_')[0]] += pedido.cantidad
    try:
        mas_vendida = max(pizzas_pedidas.values())
        return [pizza[0] for pizza in pizzas_pedidas.items() if pizza[1] == mas_vendida]
    except ValueError:
        return []    

def popularidad_mezcla_de_ingredientes(
        generador_pizzas: Generator,
        generador_contenido_pedidos: Generator,
        ingredientes: set
        ) -> int:
    
    pizzas_validas = set(map(lambda x: x.nombre, 
                             filter(lambda x: ingredientes & 
                                    set(x.ingredientes.split(';')) == ingredientes,
                                      generador_pizzas)))
    resultado = 0
    for pedido in filter(lambda x: x.nombre in pizzas_validas, generador_contenido_pedidos):
        resultado += pedido.cantidad
    return resultado

def total_ahorrado_pedidos(
        generador_contenido_pedidos: Generator,
        generador_pizzas: Generator
        ) -> str:
    
    precios = {pizza.nombre: pizza.precio for pizza in generador_pizzas}
    ganancias_pedidos = defaultdict(int)
    for pedido in generador_contenido_pedidos:
        if pedido.nombre in precios.keys():
            ganancias_pedidos[pedido.id_pedido] += (pedido.cantidad * precios[pedido.nombre]
                                                * (pedido.descuento))
    return round(sum(ganancias_pedidos.values()))

def pizza_favorita_cliente(
        generador_pedidos: Generator, 
        generador_contenido_pedidos: Generator,
        id_cliente: int,
        ) -> tuple:
    
    pedidos_cliente = set(map(lambda x: x.id_pedido, 
                              filter(lambda x: x.id_cliente == id_cliente, generador_pedidos)))
    pizzas_compradas = defaultdict(int)
    
    for pizza in filter(lambda x: x.id_pedido in pedidos_cliente, generador_contenido_pedidos):
        pizzas_compradas[pizza.nombre.split('_')[0]] += pizza.cantidad
    try:
        numero_favorito = max(pizzas_compradas.values())
        return [(pizza, numero_favorito) for pizza in pizzas_compradas.keys() 
                if pizzas_compradas[pizza] == numero_favorito]
    
    except ValueError:
        return []

# Consultas que ocupan 3 o mas Generadores

def local_mas_pizzas_vendidas_por_tipo_de_pizza(
        generador_contenido_pedidos: Generator, 
        generador_pedidos: Generator,
        generador_locales: Generator,
        tipo_de_pizza: str
        ) -> Iterable:
    cantidad_por_pedido = defaultdict(int)
    for pedido in filter(lambda x: tipo_de_pizza == x.nombre.split('_')[0],
                          generador_contenido_pedidos):
        cantidad_por_pedido[pedido.id_pedido] += pedido.cantidad 

    pedido_por_local = defaultdict(int)
    for pedidos in filter(lambda x: x.id_pedido in cantidad_por_pedido.keys(),
                           generador_pedidos):
        pedido_por_local[pedidos.id_local] += cantidad_por_pedido[pedidos.id_pedido]
    
    try:
        maximo_pedido = max(pedido_por_local.values())
        return [local for local in generador_locales 
        if pedido_por_local[local.id_local] == maximo_pedido]
    except ValueError:
        return []

def ganancia_total_de_un_local(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator, 
        generador_pizzas: Generator,
        id_local: int
        ) -> int:
    
    pedidos_validos = set(map(lambda x: x.id_pedido, 
                              filter(lambda x: id_local == x.id_local, generador_pedidos)))
    precios_pizzas = defaultdict(int, {pizza.nombre: pizza.precio for pizza in generador_pizzas})
    resultado = 0
    for pedido in filter(lambda x: x.id_pedido in pedidos_validos, generador_contenido_pedidos):
        resultado += round(pedido.cantidad * precios_pizzas[pedido.nombre] *
                            (1 - pedido.descuento))
    return resultado

def promedio_ventas_con_descuento_de_un_pais(
        generador_contenido_pedidos: Generator, 
        generador_pedidos: Generator,
        generador_locales: Generator,
        pais: str
        ) -> float:
    
    locales_validos = {x.id_local for x in filter(lambda x: x.pais == pais, generador_locales)}
    pedidos_validos = {x.id_pedido for x in filter(lambda x: x.id_local in locales_validos,
                                                    generador_pedidos)}
    len_resultado = 0
    descuentos = defaultdict(int)
    for pedido in filter(lambda x: x.id_pedido in pedidos_validos, generador_contenido_pedidos):
        descuentos[pedido.id_pedido] = pedido.descuento
    len_resultado = len(descuentos.keys())

    if len_resultado == 0:
        return 0.0
    else:
        return round(sum(descuentos.values()) * len_resultado ** (-1), 2)

def gasto_cliente_por_mes(
        generador_contenido_pedidos: Generator,  
        generador_pedidos: Generator, 
        generador_pizzas: Generator, 
        id_cliente: int,
        year: int,
        ) -> list:
    
    pedidos_validos = {pedido.id_pedido: pedido.fecha for pedido in generador_pedidos 
                       if pedido.id_cliente == id_cliente and pedido.fecha[0:4] == str(year)}
    precios_pizzas = {pizza.nombre: pizza.precio for pizza in generador_pizzas}
    gasto_meses = defaultdict(int)
    
    for pedido in filter(lambda x: x.id_pedido in pedidos_validos, generador_contenido_pedidos):
        mes_pedido = int(pedidos_validos[pedido.id_pedido][5:7])
        aumento_gasto = pedido.cantidad * (1 - pedido.descuento) * precios_pizzas[pedido.nombre]
        gasto_meses[mes_pedido] += aumento_gasto 

    return [round(gasto_meses[mes]) for mes in range(1,13)]

def pizzas_vendidas_mes_pais(
        generador_contenido_pedidos: Generator,
        generador_pedidos: Generator, 
        generador_locales: Generator, 
        pais: str,
        mes: int,
        year: int,
        ) -> int:
    
    locales_validos = {local.id_local for local in generador_locales if local.pais == pais}
    pedidos_validos = {pedido.id_pedido for pedido in generador_pedidos 
                       if pedido.id_local in locales_validos and 
                       int(pedido.fecha[0:4]) == year and int(pedido.fecha[5:7]) == mes}
    pizzas_vendidas = 0
    for pedido in filter(lambda x: x.id_pedido in pedidos_validos, generador_contenido_pedidos):
        pizzas_vendidas += pedido.cantidad
    return pizzas_vendidas

#Diccionario usado para consultas anidads según el issue n° 510 del foro.
funciones = {
        'cargar_pedidos': cargar_pedidos,
        'cargar_pizzas': cargar_pizzas,
        'cargar_contenido_pedidos': cargar_contenido_pedidos,
        'cargar_locales': cargar_locales,
        'pedidos_con_al_menos_esta_pizza': pedidos_con_al_menos_esta_pizza,
        'cantidad_vendida_de_pizza_por_tipo': cantidad_vendida_de_pizza_por_tipo,
        'pedido_con_mayor_descuento_utilizado': pedido_con_mayor_descuento_utilizado,
        'ajustar_precio_segun_ingredientes': ajustar_precio_segun_ingredientes,
        'clientes_despues_hora': clientes_despues_hora,
        'cliente_indeciso': cliente_indeciso,
        'pizzas_con_ingrediente': pizzas_con_ingrediente,
        'pizzas_pagables_de_un_tamano': pizzas_pagables_de_un_tamano,
        'cantidad_empleados_pais': cantidad_empleados_pais,
        'pizza_mas_vendida_del_dia': pizza_mas_vendida_del_dia,
        'pizza_del_mes': pizza_del_mes,
        'popularidad_mezcla_de_ingredientes': popularidad_mezcla_de_ingredientes,
        'total_ahorrado_pedidos': total_ahorrado_pedidos,
        'pizza_favorita_cliente': pizza_favorita_cliente,
        'local_mas_pizzas_vendidas_por_tipo_de_pizza': local_mas_pizzas_vendidas_por_tipo_de_pizza,
        'ganancia_total_de_un_local': ganancia_total_de_un_local,
        'promedio_ventas_con_descuento_de_un_pais': promedio_ventas_con_descuento_de_un_pais,
        'gasto_cliente_por_mes': gasto_cliente_por_mes,
        'pizzas_vendidas_mes_pais': pizzas_vendidas_mes_pais
        }
def revisar_instrucciones(instrucciones: dict) -> dict:
    """
    función auxiliar que revisa diccionarios, reemplazando funciones en forma str por funciones
      en forma "funcion"
    """
    funcion = funciones[instrucciones.pop('funcion')]
    for llave, valor in instrucciones.items():
        if isinstance(valor, dict):
            instrucciones[llave] = revisar_instrucciones(valor)
    return funcion(**instrucciones)

# Consulta anidada
def consulta_anidada(instrucciones: dict) -> Any:
    return revisar_instrucciones(instrucciones)
