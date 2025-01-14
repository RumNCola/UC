import sys
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QApplication, QLineEdit, QListWidget
from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication, QThread
from PyQt5.QtGui import QPixmap, QFont
from abc import ABC, abstractmethod
import os


class Ventana(ABC):
    """
    Clase abstracta para ventanas
    """
    
    @abstractmethod
    def __init__(self):
        super().__init__()

    @abstractmethod
    def init_gui(self):
        pass

    def salir(self):
        sys.exit()

class VentanaAgregar(Ventana):
    """
    Ventana para agregar un anuncio TTS
    """
    def __init__(self, nombre):
        super().__init__()
        self.init_gui
        self.nombre = nombre

    def init_gui(self):

        self.label = QLabel('Ingrese Mensaje a Transmitir: ')

        self.button['Guardar'] = QPushButton('Guardar')
        self.button['Guardar'].clicked.connect(self.guardar)

        self.button['Cancelar'] = QPushButton('Cancelar')
        self.button['Cancelar'].clicked.connect(self.close)

        self.edit = QLineEdit()

        hbox = QHBoxLayout()
        hbox.addWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addStretch(1)
        vbox.addWidget(self.edit)
        vbox.addStretch(1)
        vbox.addWidget()
        vbox.addStretch

    def guardar(self):
        texto = self.edit.text()
        if texto and self.nombre:
            path = os.path.join('archivos', self.nombre + '.txt')
            with open(path, 'w') as file:
                file.write(texto)
            print(f"Archivo guardado en: {path}")
            
        else:
            print("No se pudo guardar el archivo. Faltan datos.")
            self.close()




class VentanaMain(Ventana):
    """
    Ventana Principal
    """
    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        """
        Inicilaizador de Interfaz
        """
        self.list = QListWidget()

        self.buttons['Agregar'] = QPushButton('Agregar Audio')
        self.buttons['Agregar'].clicked.connect(self.agregar)

        self.buttons['Editar'] = QPushButton('Editar Audio')
        self.buttons['Editar'].clicked.connect(self.editar)

        self.buttons['Eliminar'] = QPushButton('Eliminar Audio')
        self.buttons['Eliminar'].clicked.connect(self.eliminar)

        self.label = QLabel('Audios En Cola')

        VBox = QVBoxLayout()
        VBox.addWidget(self.buttons['Agregar'])
        VBox.addStretch(1)
        VBox.addWidget(self.buttons['Eliminar'])
        VBox.addStretch(1)
        
        ListBox = QVBoxLayout()
        ListBox.addWidget(self.label)
        ListBox.addStretch(1)
        ListBox.addWidget(self.list)
        ListBox.addStretch(1)

        HBox = QHBoxLayout()
        HBox.addWidget(ListBox)
        HBox.addStretch(1)
        HBox.addLayout(VBox)
        HBox.addStretch(1)

        self.setLayout(HBox)
        self.setGeometry(800, 450, 300, 150)
        self.setWindowTitle('Reproductor de Audio')

    def agregar(self):
        pass

    def editar(self):
        pass

    def eliminar(self):
        """
        Método que elimina el archivo seleccionado en el QListWidget
        """
        pass
        

 
