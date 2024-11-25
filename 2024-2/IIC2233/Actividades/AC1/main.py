import collections
from os.path import join
from utilidades import Anime  # Debes utilizar esta nametupled


#####################################
#       Parte 1 - Cargar datos      #
#####################################
def cargar_animes(ruta_archivo: str) -> list:
    file = open(ruta_archivo, "r", encoding="UTF-8")
    animes = []
    for line in file.readlines():
        line = line.strip()
        line = line.replace(";",",")
        line = line.split(",")
        nombre = str(line[0])
        capitulos = int(line[1])
        puntaje = int(line[2])
        estreno = int(line[3])
        estudio = str(line[4])
        generos = set(line[5:len(line)])
        animes.append(Anime(nombre,capitulos,puntaje,estreno,estudio,generos))
    
    return animes

#####################################
#        Parte 2 - Consultas        #
#####################################
def animes_por_estreno(animes: list) -> dict:
    dict = {}
    for anime in animes:
        estreno = anime[3] 
        if estreno in dict:
            dict[estreno].append(anime[0])
        else:
            dict[estreno] = [anime[0]]
    return dict

def descartar_animes(generos_descartados: set, animes: list) -> list:
    resultado = []
    for anime in animes:
        valido = True
        for genero in anime[5]:
            print(anime[5])
            if genero in generos_descartados:
                valido = False
                break
        if valido:
            resultado.append(anime[0])
    return resultado

def resumen_animes_por_ver(*animes: Anime) -> dict:
    puntajes = []
    capitulos = 0
    generos = set()
    for anime in animes:
        puntajes.append(anime[2])
        capitulos += anime[1]
        for genero in anime[-1]:
            if genero not in generos:
                generos.add(genero)
    
    dict = {}
    if len(puntajes) > 0:
        dict["puntaje promedio"] = sum(puntajes)/len(puntajes)
    else:
        dict["puntaje promedio"] = 0
    dict["capitulos total"] = capitulos
    dict["generos"] = generos

    return dict

def estudios_con_genero(genero: str, **estudios: list) -> list:
    resultado = []
    for llave in estudios:
        exito = False
        for anime in estudios[llave]:
            for genre in anime[-1]:
                if genre == genero:
                    exito = True
        if exito:
            resultado.append(llave)
    return resultado

if __name__ == "__main__":
    #####################################
    #       Parte 1 - Cargar datos      #
    #####################################
    animes = cargar_animes(join("data", "ejemplo.chan"))
    indice = 0
    for anime in animes:
        print(f"{indice} - {anime}")
        indice += 1

    #####################################
    #        Parte 2 - Consultas        #
    #####################################
    # Solo se usará los 2 animes del enunciado.
    datos = [
        Anime(
            nombre="Hunter x Hunter",
            capitulos=62,
            puntaje=9,
            estreno=1999,
            estudio="Nippon Animation",
            generos={"Aventura", "Comedia", "Shonen", "Acción"},
        ),
        Anime(
            nombre="Sakura Card Captor",
            capitulos=70,
            puntaje=10,
            estreno=1998,
            estudio="Madhouse",
            generos={"Shoujo", "Comedia", "Romance", "Acción"},
        ),
    ]

    # animes_por_estreno
    estrenos = animes_por_estreno(datos)
    print(estrenos)

    # descartar_animes
    animes = descartar_animes({"Comedia", "Horror"}, datos)
    print(animes)

    # resumen_animes_por_ver
    resumen = resumen_animes_por_ver(datos[0], datos[1])
    print(resumen)

    # estudios_con_genero
    estudios = estudios_con_genero(
        "Shonen",
        Nippon_Animation=[datos[0]],
        Madhouse=[datos[1]],
    )
    print(estudios)
