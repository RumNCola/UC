# Tarea 2: DCCampesino 🌻🧟
#### Por Fernando Jara G. - Github: RumNCola - Sección 4

## Consideraciones generales :octocat:
- los *buffs* asociados a plantas mutantes Aresauce y Fensaulantro fueron definidos dentro de su inicializador. Para ahorrar código y chequeos mas tediosos,
tales *buffs* se llaman directamente desde parametros.py. 
- Todas las plantas siguene estrictamente su configuración entregada en plantas.txt, excepto Solaretillos con el valor altura y potencial. Esto implica que si un atributo de planta es entregado en plantas.txt, todas las plantas de la misma clase compartiran exactamente este valor.
- Dentro de parametros.py se incorpora un diccionario de nombre "traductor" que permite usar planta.tipo para obtener su nombre completo. Se usa este forma, puesto que __str__ ya esta en uso para otra cosa. Ejemplo: traductor['S'] - Solaretillo.
## Cosas implementadas y no implementadas
### Programación Orientada a Objetos: 16 pts (10%)
Se implementa la clase Jardin y la clase abstracta Planta. Planta se implementa como clase padre de Solaretillo, 
Defensauce y Potencilantro. Adicionalmente, se implementan las clases de cada planta mutante a través de multiherencia de sus respectivas plantas de origen. Cada clase contiene *properties* *Getter* y *Setter* para atributos dinámicos y se emplea polimorfismo dentro de la familia de clases Planta.
##### ✅ Definición de clases, herencia y *properties*

#### Preparación del programa: 6 pts (4%)
Dentro de main.py se implementan funciones dedicadas a la creación correcta de un jardin de acuerdo a los parametros entregados por el usuario. utilidades.py apoya este proceso
a través de funciones auxiliares.
##### ✅ Inicio de la partida 

#### Entidades: 64 pts (39%)
##### ✅ Jardín
##### ✅ Plantas

#### Flujo del programa: 40 pts (24%)
##### ✅ Menú de Inicio
##### ✅ Menú Jardín
##### ✅ Laboratorio
##### ✅ Fin del juego
##### ✅ Robustez

#### Simular día: 23 pts (14%)
Se implementa un metodo para determinar la temperatura en funcion de parametros.py y si hay una helada.
##### ✅ Temperatura
En utlidades.py se definen varios métodos que permiten implementar eventos. Estos abordan heladas, oleadas y dias tranquilos. Las plantas reciben daño, se congelan y mueren en función del evento que ocurra durante el dia
##### ✅ Eventos
Se define un metodo en utilidades.py para calcular los soles. Este método contempla los diferentes tipos de generadores, el bono (o no generacion) por congelacion, los soles robados, entre otros.
##### ✅ Calcular soles
Se implementa un metodo simple que realiza la llegada de plantas
##### ✅ Llegada de plantas
##### ✅ Presentación

#### Archivos: 15 pts (9%)
Se implementa una extracción funcional de la información de ambos archivos. Dentro de utilidades.py se definen funciones dedicadas a manejar esto. 
##### ✅ Archivos.txt
##### ✅ parametros.py

## Ejecucion :computer:
- El módulo principal a ejecutar es main.py
- parametros.py contiene todos los parametros necesarios para la ejecucion. 
- plantas.py incluye la familia de clases asociadas a las Planta y sus métodos.
- jardin.py contiene a la clase Jardin y sus métodos.
- utilidades.py tiene diferentes funciones dedicadas al manejo de archivos txt, eventos, creacion de Jardines, Plantas, entre otras utilidades.

## Archivos importantes:
- Para la ejecución correcta de main.py se debe tener a los siguientes archivos dentro de la misma carpeta que main.py:
    * eventos.txt: archivo txt que trae la probabilidad de que ocurran heladas o oleadas de zombis
    * jardines.txt: archivo txt que tiene los jardines y sus tableros
    * planta.txt: documento txt que posee los atributos de las plantas del juego

## Librerias:
### Librerias Externas
- random - randint
- copy - deepcopy
- abc - abstractmethod & ABC
- sys- exit & argv
### Librerias Propias
- parametros - Contiene parámetros variables para la ejecución del programa
- plantas - Contiene la familia de clases Planta y los métodos relacionados 
- jardin - Contiene la clase Jardin y elementos relacionados
- utilidades - Realiza carga de archivos txt, define eventos, calculo de soles entre otras funciones para facilitar implementacion de main


## Lista de Supuestos:
1. Armadura no lleva getter ni setter dado que es un valor muy de nicho que se ocupa solo dentro de la funcion recibir daño.
2. Se implementa un atributo oculto self.status para cada planta. Este es un booleano que sera *True* si la planta esta viva.
3. El inicializador de plantas, para los argumentos numéricos, recibe cualquier numero. Si este esta dentro de un intervalo invalido (por ejemplo
resistencia = 10000), este se asegurará de que el valor correspondiente de la instancia sea el correcto.
4. Métodos tales como recibir_daño y el setter de vida se aseguran que en caso de recibir una vida negativa o un daño muy grande, la vida siempre respete el intervalo [0, vida_max].
5. En el enunciado no se dice nada respecto al como definir el parametro armadura, por lo que este se agrego a parametros.py.
6. Cada función no trivial tiene una descripición que detalla supuestos adicionales/específicos. 
7. Los valores armadura, potencial y otros valores de las plantas mutantes no chequean si los parametros entregados son válidos, ya que esto depende del archivo parametros
8. Al usar recibir_daño, se pueden ingresar daño positivos o negativos. Esto no cambiará el output, dado que se usa el valor absoluto de daño para calcular la reducción de vida.
9. Dentro de Jardin, el atributo pool no lleva getter ni setter, pues parametro no es dinamico.
10. Se asume que una planta nunca partira en estado congelado. Esta solo se congelará en caso de una helada.
11. Las dificultades disponibles son unicamente facil, intermedio y dificil. 
12. Se asume que los buffs de Potencilantro y Cilantrillo no son stackeables. Es decir, poner dos potencilantros junto a un solaretillo generará el mismo efecto que poner solo uno. Además, se dará prioridad al buff más fuerte, es decir el de Cilantrillo.
13. El dia 0 no ocurrira ningun evento. Este es el dia de planificacion, por lo que no tiene sentido la ocurrencia de uno.



## Referencias:
En utilidades.py, se extrajo informacion del siguiente sitio para usar random.choices.
1. https://www.geeksforgeeks.org/random-choices-method-in-python/
En jardin.py, se extrajo info. del siguiente sitio para usar del y remove para eliminar elementos de listas
2. https://www.w3schools.com/python/python_lists_remove.asp 
Dentro de todo archivo, se emplea el modulo copy y su funcion deepcopy para que las plantas sean realmente únicas y asi resolver varios errores.
3. https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/ 
