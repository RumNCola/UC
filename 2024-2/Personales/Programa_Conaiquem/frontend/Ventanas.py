import sys
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QApplication, QLineEdit, QListWidget
from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication, QThread
from PyQt5.QtGui import QPixmap, QFont
from abc import ABC, abstractmethod
import os
from threading import Thread
from time import sleep

ruta_archivos = 'archivos'

class VentanaNombreAgregar(QWidget):

    senal_aceptar = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_gui()
    
    def init_gui(self):
        
        self.label = QLabel('Ingrese nombre del anuncio: ')
        self.edit = QLineEdit()

        self.button = {}
        self.button['Aceptar'] = QPushButton('Aceptar')
        self.button['Aceptar'].clicked.connect(self.aceptar)

        self.button['Cancelar'] = QPushButton('Cancelar')
        self.button['Cancelar'].clicked.connect(self.close)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.button['Aceptar'])
        hbox.addStretch(1)
        hbox.addWidget(self.button['Cancelar'])
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.label)
        vbox.addStretch(1)
        vbox.addWidget(self.edit)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setGeometry(800, 450, 300, 150)
    
    def aceptar(self):
        nombre = self.edit.text()
        self.senal_aceptar.emit(nombre)
        
        # self.popup = VentanaAgregar(nombre)
        # self.popup.show()
        # self.close()


class VentanaAgregar(QWidget):
    """
    Ventana para agregar un anuncio TTS
    """

    senal_guardar = pyqtSignal(str, str)

    def __init__(self, nombre):
        super().__init__()
        self.init_gui()
        self.nombre = nombre

    def init_gui(self):

        self.label = QLabel('Ingrese Mensaje a Transmitir: ')

        self.button = {}
        self.button['Guardar'] = QPushButton('Guardar')
        self.button['Guardar'].clicked.connect(self.guardar)

        self.button['Cancelar'] = QPushButton('Cancelar')
        self.button['Cancelar'].clicked.connect(self.close)

        self.edit = QLineEdit()

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.button['Guardar'])
        hbox.addStretch(1)
        hbox.addWidget(self.button['Cancelar'])
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.label)
        vbox.addStretch(1)
        vbox.addWidget(self.edit)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setGeometry(800, 450, 300, 150)

    def guardar(self):
        texto = self.edit.text()
        if texto and self.nombre:
            self.senal_guardar.emit(self.nombre, texto)

        
        #     print(self.nombre)
        #     path = os.path.join(ruta_archivos, self.nombre + '.txt')
        #     print(path)
        #     with open(path, 'w', encoding='utf-8') as file:
        #         file.write(texto)
            print(f"Archivo guardado en: {self.nombre}")

        else:
            print("No se pudo guardar el archivo. Faltan datos.")
            self.close()

# class VentanaEditar(VentanaAgregar):

#     def __init__(self):
#         super().__init__()
#         self.init_gui
 
class VentanaMain(QWidget):
    """
    Ventana Principal
    """

    senal_agregar = pyqtSignal()

    senal_eliminar = pyqtSignal(str)

    senal_editar = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_gui()
        self.hilo = Thread(target= self.actualizar_lista)
        self.hilo.start()

    def init_gui(self):
        """
        Inicilaizador de Interfaz
        """
        self.list = QListWidget()

        self.buttons = {}
        self.buttons['Agregar'] = QPushButton('Agregar Audio')
        self.buttons['Agregar'].clicked.connect(self.agregar)

        self.buttons['Editar'] = QPushButton('Editar Audio')
        self.buttons['Editar'].clicked.connect(self.editar)

        self.buttons['Eliminar'] = QPushButton('Eliminar Audio')
        self.buttons['Eliminar'].clicked.connect(self.eliminar)

        self.label = QLabel('Audios En Cola')

        VBox = QVBoxLayout()
        VBox.addStretch(1)
        VBox.addWidget(self.buttons['Agregar'])
        VBox.addStretch(1)
        VBox.addWidget(self.buttons['Eliminar'])
        VBox.addStretch(1)
        
        ListBox = QVBoxLayout()
        ListBox.addStretch(1)
        ListBox.addWidget(self.label)
        ListBox.addStretch(1)
        ListBox.addWidget(self.list)
        ListBox.addStretch(1)

        HBox = QHBoxLayout()
        HBox.addStretch(1)
        HBox.addLayout(ListBox)
        HBox.addStretch(1)
        HBox.addLayout(VBox)
        HBox.addStretch(1)

        self.setLayout(HBox)
        self.setGeometry(800, 450, 300, 150)
        self.setWindowTitle('Reproductor de Audio')

    def agregar(self):
        self.popup = VentanaNombreAgregar()
        self.popup.show()

    def editar(self):
        archivo = self.list.currentItem().text()
        self.senal_editar.emit(archivo)

    def eliminar(self):
        """
        Método que elimina el archivo seleccionado en el QListWidget
        """
        archivo = self.list.currentItem().text()
        if archivo:
            ruta = os.path.join('archivos/' + archivo)
            
            if os.path.exists(ruta):
                os.remove(ruta)
                print(f'Archivo eliminado {ruta}')
            
        else:
            print(f'El archivo no existe')
        
    def actualizar_lista(self):
        while True:
            for archivo in os.listdir(ruta_archivos):
                self.list.addItem(archivo)
            sleep(2)

        

        

 
