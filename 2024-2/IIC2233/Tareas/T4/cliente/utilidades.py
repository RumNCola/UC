import os

def identificador_archivos(ruta: str) -> list:
    """
    Función que identifica los archivos en una ruta y los retorna como tuplas, donde se incluye
    el nombre del archivo y su extensión. Esto no funciona con archivos que no sean git (.keep) o 
    archivos que tengan el punto en su nombre
    """
    archivos = []
    for archivo in os.listdir(ruta):
        archivo_separado = archivo.split('.')
        if len(archivo_separado) == 1:
            archivos.append((archivo, 'carpeta'))
        else:
            archivos.append((archivo_separado[0], archivo_separado[1]))
    return archivos

def cargar_nombre_archivos(archivos: list) -> list:
    """
    Función que recibe archivos en formato identificador_archivos y los devuelve con nombre
    completo
    """
    return [archivo for archivo in map(lambda x: x[0] + '.' + x[1], archivos)]


# resultado = identificador_archivos('./servidor/archivos')
# print(resultado)
# print('==============')
# print(cargar_nombre_archivos(resultado))

