from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QApplication, QLineEdit, QListWidget
from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication, QThread
from PyQt5.QtGui import QPixmap, QFont
import sys
import os
import utilidades as u
from frontend.ventana_inicio_error import VentanaError
from frontend.ventana_archivos import VentanaMisArchivos

class VentanaConfirmacionDescargas(QWidget):
    """
    Clase de ventena que solicita confirmación para una descarga
    """

    senal_confirmacion = pyqtSignal(str)

    def __init__(self, archivo):
        super().__init__()
        self.archivo = archivo
        self.init_gui()
        

    def init_gui(self):
        self.botones = {}
        self.botones['confirmar'] = QPushButton('Aceptar')
        self.botones['confirmar'].clicked.connect(self.descargar)

        self.botones['rechazar'] = QPushButton('Rechazar')
        self.botones['rechazar'].clicked.connect(self.close)

        self.label = QLabel(f'Confirmar descarga de {self.archivo}?')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.botones['confirmar'])
        hbox.addStretch(1)
        hbox.addWidget(self.botones['rechazar'])
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.label)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setGeometry(800, 450, 300, 150)
        self.setWindowTitle('Pop-up Confirmación')

    def descargar(self):
        """
        Función que pide la descarga al backend
        """
        self.senal_confirmacion.emit(self.archivo)
        self.salir()
    
    def salir(self):
        self.close() 

# class DescargaArchvios(QThread):
#     """
#     Clase que hereda de thread que se asegura de procesar descargas de archivos en simultaneo
#     """
#     def __init__(self, archivo):
#         super().__init__()
#         self.archivo = archivo
    
#     def run(self):
#         pass

class VentanaDescargas(QWidget):
    """
    Clase para la ventana de descargas del programa
    """
    #señal para solicitar la descarga de un archivo
    senal_descarga = pyqtSignal(str)
    
    #señal para solicitar la lista de usuarios
    senal_usuarios = pyqtSignal()

    #señal para actualizar los archivos
    senal_archivos = pyqtSignal()

    #Señal para cambiar el estado de una descarga activa
    senal_proceso = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_gui()
        self.mis_archivos = VentanaMisArchivos(self)
    
    def init_gui(self):
        """
        Inicializador de la interfaz gráfica
        """
        self.boton = {}
        self.boton['actualizar'] = QPushButton('Actualizar archivos disponibles', self)
        self.boton['actualizar'].clicked.connect(self.actualizar_disponibles)

        self.boton['iniciar'] = QPushButton('Iniciar Descarga', self)
        self.boton['iniciar'].clicked.connect(self.iniciar_descarga)

        self.boton['pausa'] = QPushButton('Pausar', self)
        self.boton['cancelar'] = QPushButton('Cancelar', self)
        self.boton['reanudar'] = QPushButton('Reanudar', self)

        self.boton['mis archivos'] = QPushButton('Ir a Mis Archivos', self)
        self.boton['mis archivos'].clicked.connect(self.mis_archivos)

        self.label = {}
        self.label['descargas'] = QLabel('Archivos Disponibles: ', self)
        self.label['usuarios'] = QLabel('Usuarios Conectados', self)

        self.buscar = QLineEdit('Nombre de archivo', self)

        self.conectados = QListWidget()
        
        self.archivos_disponibles = QListWidget()
        self.archivos_disponibles.itemClicked.connect(self.actualizar_seleccion)
        self.archivos_disponibles.itemDoubleClicked.connect(self.actualizar_seleccion)
        
        #hbox de la barra de búsqueda/actualización
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.boton['actualizar'])
        hbox.addStretch(1)
        hbox.addWidget(self.buscar)
        hbox.addStretch(1)
        hbox.addWidget(self.boton['iniciar'])
        hbox.addStretch(1)

        vbox_botones = QVBoxLayout()
        vbox_botones.addStretch(1)
        vbox_botones.addWidget(self.boton['reanudar'])
        vbox_botones.addStretch(1)
        vbox_botones.addWidget(self.boton['pausa'])
        vbox_botones.addStretch(1)
        vbox_botones.addWidget(self.boton['cancelar'])
        vbox_botones.addStretch(1)

        vbox_archivos = QVBoxLayout()
        vbox_archivos.addStretch(1)
        vbox_archivos.addWidget(self.label['descargas'])
        vbox_archivos.addStretch(1)
        vbox_archivos.addWidget(self.archivos_disponibles)
        vbox_archivos.addStretch(1)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addLayout(vbox_archivos)
        hbox1.addStretch(1)
        hbox1.addLayout(vbox_botones)
        hbox1.addStretch(1)

        vbox_usuarios = QVBoxLayout()
        vbox_usuarios.addStretch(1)
        vbox_usuarios.addWidget(self.label['usuarios'])
        vbox_usuarios.addStretch(1)
        vbox_usuarios.addWidget(self.conectados)
        vbox_usuarios.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addLayout(vbox_usuarios)
        hbox2.addStretch(1)
        hbox2.addWidget(self.boton['mis archivos'])
        hbox2.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addStretch(1)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setWindowTitle('Mis Descargas')
        self.setGeometry(800, 450, 600, 500)

        self._actualizar_disponibles()

    def pausa(self):
        """
        Método que envía un mensaje al server para pausar la descarga
        """
        self.senal_proceso.emit('pausa')

    def reanudar(self):
        """
        Método que envía un mensaje al server para reanudar la descarga
        """
        self.senal_proceso.emit('reanudar')

    def cancelar(self):
        """
        Método que envía un msg al server para cancelar la descarga
        """
        self.senal_proceso.emit('cancelar')

    def iniciar_descarga(self):
        """
        Función que se encarga de pedir al usuario que confirme una descarga
        """
        archivo = self.buscar.text()
        self.popup = VentanaConfirmacionDescargas(archivo)
        self.popup.senal_confirmacion.connect(self.procesar_descarga)
        self.popup.show()
    
    def procesar_descarga(self, archivo):
        """
        Función que procesa una descarga ya aceptada
        """
        self.senal_descarga.emit(archivo)
        
    def actualizar_usuarios(self, data):
        """
        función que obitene la lista de usuarios conectados
        """
        self.conectados.clear()
        print('iniciando actualizacion de usuarios')
        if len(data) > 0:
            self.conectados.addItems(data)
        
    def actualizar_archivos(self, data):
        """
        Funcion que actualiza la lista de archivos disponibles
        """
        print('iniciando actualizacion de archivos')
        self.archivos_disponibles.clear()
        data = u.cargar_nombre_archivos(data)
        if len(data) > 0:
            self.archivos_disponibles.addItems(data)
    
    def _actualizar_disponibles(self):
        """
        Método oculto que hace que se actualize constantemente el estado
        """
        self.hilo_actualizar = QThread()
        self.hilo_actualizar.run = self.actualizar_disponibles
        self.hilo_actualizar.start()
        
        if not self.hilo_actualizar.isRunning():
            self._actualizar_disponibles()

    def actualizar_disponibles(self):
        """
        función que actualiza los archivos y usuarios disponibles
        """
        self.senal_usuarios.emit()
        self.senal_archivos.emit()
    
    def actualizar_seleccion(self):
        """
        función que actualiza el archivo seleccionado a descargar si este es clickeado
        en el qlistwidget de archivos disponibles
        """
        archivo = self.archivos_disponibles.currentItem().text()
        self.buscar.setText(archivo)

    def error(self, error):
        self.error = VentanaError(error)
        self.error.show()
    
    def mis_archivos(self):
        """
        Métood que abre la ventana mis_archivos
        """
        self.hide()
        self.mis_archivos.show()
    
    def salir(self):
        """
        método que cierra la ventana
        """
        self.close()