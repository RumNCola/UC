import random
from abc import ABC, abstractmethod
import parametros as p

class Planta(ABC):
    def __init__(self, tipo: str, vida_max: int, vida: int, res: int, 
                 res_termica: int, frozen: bool, altura: int) -> None:
        """
        El inicializador de Planta recibe los parámetros necesarios y se asegura de que sean 
        inicializados correctamente. Esto contempla el ingreso de parámetros no válidos o
        fuera de rango.
        tipo <=> string de largo 1 con el tipo
        vida_max <=> int entre 0 y 100
        vida <=> int entre 0 y vida_max
        res <=> int entre 0 y 30
        res_termica <=> int entre -5 y 25
        frozen <=> True si esta congelado
        altura <=> int entre 0 y 30
        self.status <=> True si la planta esta viva (vida > 0)
        """
        self.tipo = tipo
        if 0 <= vida_max:
            self.vida_max = min(100, vida_max)
        else:
            self.vida_max = 0
        
        if vida <= self.vida_max: 
            self._vida = max(0, vida)
        else:
            self._vida = self.vida_max

        if res <= 40:
            self.res = max(0, res) 
        else:
            self.res = 40

        if res_termica <= 25:
            self.res_termica = max(-5, res_termica)
        else:
            self.res_termica = 25
        #En plantas.txt, frozen se parametriza como [0,1]. Nosotros usaremos booleanos
        if frozen == 1 or frozen == True:
            self.frozen = True
        elif frozen == 0 or frozen == False:
            self.frozen = False

        if altura <= 30:
            self._altura = max(0, altura)
        else:
            self._altura = 30

        if self._vida > 0: 
            self.status = True
        else:
            self.status = False

    @property
    def vida(self) -> int:
        return self._vida
    @vida.setter  
    def vida(self, vida_nueva) -> int:
        """
        vida.setter cambia el valor de vida actual de la planta
        Esta funcion escoge el maximo entre self._vida y 0 para evitar
        problemas como vidas negativas. Además se asegura de que la vida nueva
        no sea mayor a la máxima.
        """
        if 0 < vida_nueva:
            self._vida = min(vida_nueva, self.vida_max)
        else: 
            self._vida = 0
            self.status = False

    @property
    def altura(self) -> int:
        return self._altura
    @altura.setter
    def altura(self, altura_nueva :int) -> None:
        """
        El setter de Altura cambia la altura de una planta, asegurandose
        de que el nuevo valor no sobrepase el máximo (30) o mínimo (0).
        """
        if altura_nueva > 30:
            self._altura = 30
        else:
            self._altura = max(0, altura_nueva)

    #Metodos
    def regarse(self, curacion) -> None:
        """
        El metodo regare cura a una planta según "curacion"
        Este método respeta los rangos de vida y vida maxima
        """
        self.vida = ((self.vida + curacion))
    
    def __repr__(self):
        if self.frozen:
            return "'*" + self.tipo + "*'"
        else:
            return "'" +str(self.tipo) + "'"
        
    def __str__(self):
        if self.frozen:
            return "'*" + self.tipo + "*'"
        else:
            return "'" + str(self.tipo) + "'"
    @abstractmethod
    def recibir_daño(self, daño):
        """
        Este método depende del tipo de planta. Si esta tiene armadura, 
        la planta procesará el daño de otra forma.
        """
        pass

class Solaretillo(Planta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.potencial = random.randint(p.POTENCIAL_SOLARETILLO_MIN, p.POTENCIAL_SOLARETILLO_MAX)
    
    def producir_soles(self, temperatura: int) -> int:
        """
        Este método produce soles segun la temperatura entregada.
        El valor retornado nunca será menor a 0 y si la planta esta congelada
        no hay produccion.
        """
        if self.frozen:
            return 0
        else:
            return max(0, round(p.CONSTANTE_SOLES * self.potencial * (temperatura / 25) * 
                            (self.altura / 30)))

    def recibir_daño(self, daño: int, x: int, y: int) -> None:
        vida_original = self.vida
        self.vida = (max(self.vida - abs(daño), 0))
        perdida = vida_original - self.vida
        if self.vida == 0:
            print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de vida,'
                  f' lo que acabo con su vida')
        else:
            print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de vida')
    

class Defensauce(Planta):
    def __init__(self, *args, **kwargs):
        self.armadura = p.ARMADURA
        super().__init__(*args, **kwargs)
    
    def recibir_daño(self, daño: int, x: int, y: int) -> None:
        if self.armadura > 0:
            armadura = self.armadura
            self.armadura = max(0, armadura - abs(daño))
            perdida = armadura - self.armadura
            print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de armadura')
        else:
            vida_original = self.vida
            self.vida = (max(self.vida - abs(daño), 0))
            perdida = abs(self.vida - vida_original)
            if self.vida == 0:
                print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de vida,'
                      f' lo que acabo con su vida')
            else:
                print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de vida') 

class Potencilantro(Planta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aumento = p.AUMENTO_NUTRIENTE

    def recibir_daño(self, daño: int, x: int, y: int) -> None:
        vida_original = self.vida
        self.vida = (max(self.vida - abs(daño), 0))
        perdida = vida_original - self.vida
        if self.vida == 0:
            print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de vida, '
                  f'lo que acabo con su vida')
        else:
            print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de vida')
    
#Plantas Mutantes#
class Aresauce(Solaretillo, Defensauce):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anti_robo = 1 - p.ANTI_ROBO / 100
    
    def recibir_daño(self, daño: int, x: int, y: int) -> None:
        if self.armadura > 0:
            armadura = self.armadura
            self.armadura = max(0, armadura - abs(daño))
            perdida = armadura - self.armadura
            print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de armadura')
        else:
            vida_original = self.vida
            self.vida = (max(self.vida - abs(daño), 0))
            perdida = abs(self.vida - vida_original)
            if self.vida == 0:
                print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de vida,'
                      f' lo que acabo con su vida')
            else:
                print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de vida') 
    
class Cilantrillo(Solaretillo, Potencilantro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aumento = (1 + p.AUM_AUM_CIL / 100) * (1 + p.AUMENTO_NUTRIENTE / 100) #Es un float
        potencial_original = self.potencial
        self.potencial = potencial_original * (1 + p.AUM_POT_CIL / 100)

    def producir_soles(self, temperatura: int) -> int:
        """
        Este método produce soles segun la temperatura entregada.
        El valor retornado nunca será menor a 0 y si la planta esta congelada
        no hay produccion.
        """
        if self.frozen:
            return 0
        else:
            produccion = p.CONSTANTE_SOLES
            produccion *= self.potencial * (temperatura / 25) * (self.altura / 30)
            return max(0, round(produccion) * self.aumento)

    def recibir_daño(self, daño: int, x: int, y: int) -> None:
        vida_original = self.vida
        self.vida = (max(self.vida - abs(daño), 0))
        perdida = vida_original - self.vida
        if self.vida == 0:
            print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de '
                  f'vida, lo que acabo con su vida')
        else:
            print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de vida')

class Fensaulantro(Defensauce, Potencilantro):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debuff = 1 - p.RED_ATQ / 100 #no porcentual
   
    def recibir_daño(self, daño: int, x: int, y: int) -> None:
        if self.armadura > 0:
            armadura = self.armadura
            self.armadura = max(0, armadura - abs(daño))
            perdida = armadura - self.armadura
            print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de armadura')
        else:
            vida_original = self.vida
            self.vida = (max(self.vida - abs(daño), 0))
            perdida = abs(self.vida - vida_original)
            if self.vida == 0:
                print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de vida,'
                      f' lo que acabo con su vida')
            else:
                print(f'La planta {self.tipo} en ({x},{y}) ha perdido {perdida} puntos de vida') 
