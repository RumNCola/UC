

class Vehiculo:
    identificador = 1

    def __init__(self, rendimiento: int, marca: str, energia: float = 111.5, *args, **kwargs) -> None:
        self.rendimiento = rendimiento
        self.marca = marca
        self._energia = max(round(energia,1), 0)
        self.identificador = Vehiculo.identificador
        Vehiculo.identificador += 1

    @property
    def autonomia(self) -> float:
        #Getter
        return self._energia * self.rendimiento
    
    @property
    def energia(self) -> float:
        if self._energia < 0:
            self._energia = 0
            return self._energia
        else:
            return self._energia
    @energia.setter
    def energia(self, nueva_energia: float) -> None:
        #Setter
        if nueva_energia <= 0:
            self._energia = 0 
            print(f'Nueva energía registrada: {self._energia}')
        else: 
            self._energia = round(nueva_energia,1)
            print(f'Nueva energía registrada: {self._energia}')

class AutoBencina(Vehiculo):
     def __init__(self, bencina_favorita, *args, **kwargs) -> None:
         self.bencina_favorita = bencina_favorita
         super().__init__(*args, **kwargs)
         pass
     
     def recorrer(self, kilometros: int) -> str:
         if kilometros > self.autonomia:
             N = self.autonomia
             Z = round(N / self.rendimiento, 1)
             texto = f'Anduve {N}Km y eso consume {Z}L de bencina'
             print(texto)
             self.energia = 0 
             return texto
         else:
             N = kilometros
             Z = round(N / self.rendimiento, 1)
             texto = f'Anduve {N}Km y eso consume {Z}L de bencina'
             print(texto) 
             self.energia = self.energia - Z
             return texto

class AutoElectrico(Vehiculo): 
    def __init__(self, vida_util_bateria: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.vida_util_bateria = vida_util_bateria

    def recorrer(self, kilometros: int) -> str:
        if kilometros > self.autonomia:
            N = self.autonomia
            Z = round(N / self.rendimiento, 1)
            self.energia = 0
            texto = f'Anduve {N}Km y eso consume {Z}W de energia electrica'
            print(texto) 
            return texto
        else:
            N = kilometros
            Z = round(N / self.rendimiento, 1)
            self.energia -= Z
            texto = f'Anduve {N}Km y eso consume {Z}W de energia electrica'
            print(texto)
            return texto

class Camioneta(AutoBencina):
    def __init__(self, capacidad_maleta: int, *args, **kwargs):
        self.capacidad_maleta = capacidad_maleta
        super().__init__(*args, **kwargs)
        pass

class Telsa(AutoElectrico):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    def recorrer(self, kilometros: int) -> str:
        return str(super().recorrer(kilometros)) + ' de forma muy inteligente'

class FaitHibrido(AutoBencina, AutoElectrico):
    def __init__(self, *args, **kwargs) -> None:
        self.vida_util_bateria = 5
        super().__init__(vida_util_bateria = self.vida_util_bateria, *args, **kwargs)
        
    def recorrer(self, kilometros: int) -> str:
        if kilometros > 10:
            return AutoBencina.recorrer(self, 10) + ' ' + AutoElectrico.recorrer(self, kilometros - 10)
        else:
            return AutoElectrico.recorrer(self, kilometros)
