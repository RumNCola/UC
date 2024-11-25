# Tarea 4: DCComparte Archivos 💻🍃


## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Interfaz Gráfica: 33 pts (28%)
##### ✅ Ventana Inicio de Sesion
##### ✅ Ventana Principal: Seccion "Mis Descargas"
##### ✅ Ventana Principal: Seccion "Mis Archivos"
##### ✅ Flujo

#### Networking: 75 pts (64%)
##### ✅ Networking General
##### ✅ Codificación y decodificación de archivos
##### ❌ Peer2Peer
##### ❌✅🟠 Eventos

#### Archivos: 10 pts (8%)
##### ❌✅🟠 Datos
##### ❌✅🟠 JSON
##### ❌✅🟠 parametros


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```archivo.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```archivo.ext``` en ```ubicación```
2. ```directorio``` en ```ubicación```
3. ...


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```función() / módulo```
2. ```PyQt5```: ```función() / módulo``` 
3. ```sys```: ```función() / módulo``` 
4. ```socket```: ```función() / módulo``` 
5. ```math```: ```función() / módulo``` 
6. ```json```: ```función() / módulo``` 
7. ```pickle```: ```función() / módulo``` 
8. ```time```: ```función() / módulo``` 


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```funciones.pyc```: Contiene a ```ClaseA```, ```ClaseB```, (ser general, tampoco es necesario especificar cada una)...
2. ```utilidades```: Hecha para <insertar descripción **breve** de lo que hace o qué contiene>
3. ...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Para generar un identificador de mensaje, se genera un número al azar entre 1 y 9000 y este se codifica usando .to_bytes(64, byteorder='big')
2. Para el metodo que actualiza los usuarios desconectados, se usa sleep de Time y del de diccionarios. Esto con el proposito de no generar un RunTimeError, es decir, que no se solape la edición del diccionario consigo misma y se caiga el servidor (pase 2 horas arreglando esto).
3. En la ventana de descargas, se debe ingresar el nombre del archivo completo para que se procese la descarga. Esto no contempla la extensión, aunque es indiferente si esta es escrita o no. 
4. Con respecto al punto anterior, el usuario puede clickear el en el QListWidget el archivo que desea descargar y este será automáticamente ingresado al QLineEdit que define que archivo se descarga, haciendo esta dinámica más user friendly.
5. La Ventana mis archivos es capaz de abrir todos los archivos del enunciado y aquellos que son jpg. Cualquier archivo que tenga otra extensión no podrá ser abierto.

PD: <Todas las funciones o métodos contienen una descripción ordenada usando triple cremillas. Se ha mantenido especial consideración en el orden y limpieza de la tarea al desarrollarla.>


-------



**EXTRA:** si van a explicar qué hace específicamente un método, no lo coloquen en el README mismo. Pueden hacerlo directamente comentando el método en su archivo. Por ejemplo:

```python
class Corrector:

    def __init__(self):
          pass

    # Este método coloca un 6 en las tareas que recibe
    def corregir(self, tarea):
        tarea.nota  = 6
        return tarea
```

Si quieren ser más formales, pueden usar alguna convención de documentación. Google tiene la suya, Python tiene otra y hay muchas más. La de Python es la [PEP287, conocida como reST](https://www.python.org/dev/peps/pep-0287/). Lo más básico es documentar así:

```python
def funcion(argumento):
    """
    Mi función hace X con el argumento
    """
    return argumento_modificado
```
Lo importante es que expliquen qué hace la función y que si saben que alguna parte puede quedar complicada de entender o tienen alguna función mágica usen los comentarios/documentación para que el ayudante entienda sus intenciones.

## Referencias de código externo :book:
1. https://stackoverflow.com/questions/18129830/count-the-uppercase-letters-in-a-string-with-python # Código usado para contar mayusculas en validar_usuario.
2. Se usa el comando os.urandom() de la libreria os para generar 64 bytes aleatorios correspondientes al id de un mensaje
3. https://www.geeksforgeeks.org/pyqt5-qlistwidget-python/ #De aquí aprendí a usar QListWidget y .clear() para poner los archivos y usuarios coenctados en la ventana de descargas
4. De las ayudantías se extrajo mútiples cuadros de códigos para el desarrollo de la tarea, especialmente la ayudantía 11.
