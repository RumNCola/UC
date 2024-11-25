import entities
import pretty_print as pp
import random

def cargar_nombres(lista):
    nombre = []
    for elemento in lista:
        if elemento.isalpha() == True:
            nombre.append(elemento)
    nombre = " ".join(nombre)
    print(type(nombre))
    return nombre


def cargar_items():
    list = []
    file = open(r"Syllabus\Actividades\AC0\utils\items.dcc", "r", encoding="UTF-8")
    for linea in file.readlines():
        linea = linea.replace(",", " ")
        linea = linea.split()
        #print(linea)

        nombre = cargar_nombres(linea)
        precio = int(linea[-2])
        puntos = int(linea[-1])
        print("Item: " + str(nombre) + ", " + str(precio) + ", " + str(puntos))
        Item = entities.Item(nombre,precio,puntos)
        list.append(Item)

    return list

def crear_usuario(tiene_suscripcion):
    usuario = entities.Usuario(tiene_suscripcion)
    pp.print_usuario(usuario)
    return usuario

#La suscripción se tira al azar
codigo = random.randint(1,2)
tiene_suscripcion = False
if codigo == 1:
    tiene_suscripcion = True


if __name__ == "__main__": ##CAMBIAR !
        
    #se crea el usuario              1
    usuario = crear_usuario(tiene_suscripcion)

    #Se cargan los Items             2
    items = cargar_items()

    #Se imprimen todos los items usando pp 3
    pp.print_items(items)
    print("\n")

    #Se agregan todos litems a la canasta del usuario 4
    for item in items: 
        #print(item)
        usuario.agregar_item(item)

    #Se imprime la canasta dle usuario 5
    pp.print_canasta(usuario)

    #Se genera la compra del usuario 6
    usuario.comprar()

    #se imprime el usuairo usando pp 7
    pp.print_usuario(usuario)


    






