from PyQt5.QtWidgets import QLabel, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QApplication, QLineEdit, QListWidget, QTextEdit
from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication, QThread, QUrl
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
import sys
import os
import utilidades as u
from frontend.ventana_inicio_error import VentanaError

class VentanaMisArchivos(QWidget):
    def __init__(self, ventana_mis_descargas):
        super().__init__()
        self.init_gui()
        self.ventana_mis_descargas = ventana_mis_descargas

    def init_gui(self):
        """
        Inicializador de la interfaz gráfica
        """
        self.labels = {}
        self.labels['titulo'] = QLabel('Archivos Disponibles', self)
        self.labels['cabeza'] = QLabel('Mis Archivos', self)

        self.archivos = QListWidget()
        self.archivos.itemDoubleClicked.connect(self.abrir_archivo)
        self.archivos.itemClicked.connect(self.mostrar_archivo)

        self.abrir = QPushButton('Abrir', self)
        self.abrir.clicked.connect(self.abrir_archivo)

        self.actualizar = QPushButton('Actualizar Archivos Disponibles', self)
        self.actualizar.clicked.connect(self.actualizar_archivos)

        self.volver = QPushButton('Regresar a \'Mis Descargas\'', self)
        self.volver.clicked.connect(self.regresar)

        self.cuadro = QLabel('Clickee un archivo del QListWidget para abrir', self)

        vbox1 = QVBoxLayout()
        vbox1.addStretch(1)
        vbox1.addWidget(self.labels['titulo'])
        vbox1.addStretch(1)
        vbox1.addWidget(self.archivos)
        vbox1.addStretch(1)

        vbox2 = QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(self.cuadro)
        vbox2.addStretch(1)
        vbox2.addWidget(self.abrir)
        vbox2.addStretch(1)
        vbox2.addWidget(self.actualizar)        
        vbox2.addStretch(1)
        vbox2.addWidget(self.volver)
        vbox2.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox1)
        hbox.addStretch(1)
        hbox.addLayout(vbox2)
        hbox.addStretch(1)

        bocks = QHBoxLayout()
        bocks.addStretch(1)
        bocks.addWidget(self.labels['cabeza'])
        bocks.addStretch(1)

        box = QVBoxLayout()
        box.addStretch(1)
        box.addLayout(bocks)
        box.addStretch(1)
        box.addLayout(hbox)
        box.addStretch(1)

        self.setLayout(box)
        self.setWindowTitle('Mis Archivos')
        self.setGeometry(800, 450, 400, 250)

    def mostrar_archivo(self, archivo):
        """
        Método que muestra el archivo clickeado del Qlistwidget en un Qlabel
        """
        archivo = archivo.text()
        self.cuadro.setText(f'Archivo seleccionado: {archivo}')

    def abrir_archivo(self):
        """
        Método que abre un archivo ingresado cuando se presiona abrir
        """
        archivo = self.archivos.currentItem().text()

        print(f'abriendo archivo {archivo}')

        if archivo:
            extension = archivo.split('.')[1]
        
            if extension == 'txt' or extension == 'csv':
                self.abrir_txt()
        
            elif extension == 'jpeg' or extension == 'png' or extension == 'jpg':
                self.abrir_jpeg()
        
            elif extension == 'mp3':
                self.abrir_mp3()
        

    def abrir_txt(self):
        """
        Método que abre un popup con el archivo de texto seleccionado
        """
        archivo = self.archivos.currentItem().text()
        ruta = os.path.join('./cliente/archivos', archivo)
        
        with open(ruta, 'r') as file:
            contenido = file.read()

        ventana = QWidget()
        ventana.setWindowTitle(f'{archivo}')
        ventana.resize(800, 600)
        
        texto = QTextEdit(ventana)
        texto.setReadOnly(True)
        texto.setText(contenido)
        
        box = QVBoxLayout()
        box.addWidget(texto)

        ventana.setLayout(box)
        self.ventana = ventana
        self.ventana.show()


    def abrir_jpeg(self):
        """
        Método que abre un popup con el archivo imagen seleccionado
        """
        archivo = self.archivos.currentItem().text()
        ruta = os.path.join('./cliente/archivos', archivo)

        ventana = QWidget()
        ventana.setWindowTitle(f'{archivo}')

        label = QLabel(ventana)
        pixmap = QPixmap(ruta)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
                      
        box = QVBoxLayout()
        box.addWidget(label)

        ventana.setLayout(box)
        
        self.ventana = ventana
        self.ventana.show()

    def abrir_mp3(self):
        """
        Método que abre una ventana con el archivo de audio seleccionado
        """
        archivo = self.archivos.currentItem().text()
        ruta = os.path.join('./cliente/archivos', archivo)

        self.player = QMediaPlayer(self)
        cancion = QMediaContent(QUrl.fromLocalFile(ruta))
        self.player.setMedia(cancion)
        self.player.play()

        self.ventana = QWidget()
        self.ventana.setWindowTitle(f'{archivo}')
        self.ventana.resize(300, 100)

        boton = QPushButton('Cerrar', self.ventana)
        boton.clicked.connect(self.player.stop)
        boton.clicked.connect(self.ventana.close)

        box = QHBoxLayout()
        box.addWidget(boton)
        self.ventana.setLayout(box)
        self.ventana.show()
        self.player.play()
    
    def actualizar_archivos(self):
        """
        Método que actualiza el qlsitwidget con los archivos disponibles
        """
        archivos = u.identificador_archivos('./cliente/archivos')
        archivos = u.cargar_nombre_archivos(archivos)
        self.archivos.clear()
        self.archivos.addItems(archivos)
    
    def regresar(self):
        """
        Función que regresa al usuario a mis descargas
        """
        self.hide()
        self.ventana_mis_descargas.show()
