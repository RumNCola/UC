from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication, QThread
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from frontend.Ventanas import VentanaMain, VentanaNombreAgregar, VentanaAgregar
import os
from sys import exit
from threading import Thread


class Audio:
    def __init__(self, ruta):
        self.ruta = ruta 

class Client:
    def __init__(self):
        self.ventana_main = VentanaMain()

    def agregar_a_nombre(self):
        """
        metodo para cuando VentanaMain envia señal para abrir VentanaNombre
        """
        self.ventana_main.hide()
        self.popup = VentanaNombreAgregar()
        self.popup.show()

    def agregar_con_nombre(self, nombre: str):
        """
        metodo para cuando VentanaNombreAgregar registra un nombre correcto
        """
        self.popup2 = VentanaAgregar
        
        try:
            self.popup.hide()
        except:
            pass
        
        self.popup2.show()

    def agregar(self, nombre: str, texto: str):
        """
        Método para agregar el mensaje con VetanaAgregar
        """

        if self.popup2:
            archivo = 'archivos/' + nombre + '.txt'
            with open(archivo, 'w', encoding='utf-8') as file;
                file.write(texto)

        self.popup2.hide()
        self.ventana_main.show()
    
    def eliminar(self, nombre: str):
        """
        Metodo activado por VentanaMain para eliminar el archivo de nombre 'nombre'
        """
        archivos = [archivo for archivo in os.listdir('archivos')]
        for archivo in archivos:
            if nombre in archivo:
                os.remove('archivos/' + archivo)



        

