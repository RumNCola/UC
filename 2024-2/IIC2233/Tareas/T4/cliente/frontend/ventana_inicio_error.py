# import cliente.backend.backend as back
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QApplication, QLineEdit, QListWidget
from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication, QThread
from PyQt5.QtGui import QPixmap, QFont
import sys
import os
import utilidades as u

class VentanaInicio(QWidget):
    """
    Clase destinada para usar una ventana de inicio
    """
    #Señal para enviar el usuario al backend
    senal_usuario = pyqtSignal(str) 

    #Señal para abrir el programa dado inicio exitoso
    senal_inicio_exitoso = pyqtSignal()

    #señal para soliciar usuarios conectados y archivos disponibles
    senal_setup = pyqtSignal()

    def __init__(self, ventana_descargas):
        super().__init__()
        self.init_gui()
        self.ventana_descargas = ventana_descargas
        
    def init_gui(self):
        """
        Inicializador de la interfaz
        """
        self.etiquetas = {}
        self.etiquetas['etiqueta1'] = QLabel('Bienvenido a DCComparte!', self)
        self.etiquetas['etiqueta1'].setFont(QFont('Arial', 14))
        self.etiquetas['etiqueta2'] = QLabel('Ingrese su nombre de usuario:', self)
        self.etiquetas['etiqueta2'].setFont(QFont('Arial', 12))
        self.etiquetas['foto'] = QLabel(self)

        ruta_foto = os.path.join('cliente/frontend/imagenes', 'logo_dccomparte.png')
        pixeles = QPixmap(ruta_foto)
        self.etiquetas['foto'].setPixmap(pixeles)
        self.etiquetas['foto'].setScaledContents(True)

        self.botones = {}
        self.botones['salir'] = QPushButton('Salir', self)
        self.botones['salir'].resize(self.botones['salir'].sizeHint())
        self.botones['salir'].clicked.connect(self.salir)

        self.botones['login'] = QPushButton('Iniciar Sesion', self)
        self.botones['login'].resize(self.botones['login'].sizeHint())
        self.botones['login'].clicked.connect(self.verificar_usuario)

        self.cuadro_texto = QLineEdit('', self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.etiquetas['etiqueta1'])
        vbox.addStretch(1)
        vbox.addWidget(self.etiquetas['etiqueta2'])
        vbox.addWidget(self.cuadro_texto)
        vbox.addStretch(1)
        vbox.addWidget(self.botones['login'])
        vbox.addWidget(self.botones['salir'])
        vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.etiquetas['foto'])
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.setLayout(hbox)
        
        self.setGeometry(600, 300, 450, 300)
        self.setWindowTitle('DCComparte - Login') 
   
    def verificar_usuario(self):
        """
        Método que emite una señal para iniciar la verificación de usuario
        """
        self.senal_usuario.emit(self.cuadro_texto.text())
    
    def login_exitoso(self):
        """
        Método que cierra la ventana y muestra la de descargas si el login es exitoso
        """
        self.close()
        self.ventana_descargas.show()
    
    def login_falso(self):
        """
        Metodo que raisea una ventana de error si el login falló
        """
        self.error = VentanaError('Usuario Inválido')
        self.error.show()

    def salir(self):
        self.close()
    
class VentanaError(QWidget):
    def __init__(self, error):
        super().__init__()
        self.error = error
        self.init_gui()

    def init_gui(self: str):
       """
       Inicializador de l ainterfaz
       """
       self.boton = QPushButton('Cerrar', self)
       self.boton.clicked.connect(self.salir)
       
       self.texto = QLabel(f'Error: {self.error}')
       vbox = QVBoxLayout()

       vbox.addStretch(1)
       vbox.addWidget(self.texto)
       vbox.addStretch(1)
       vbox.addWidget(self.boton)
       vbox.addStretch(1)

       self.setLayout(vbox)

       self.setGeometry(800, 450, 300, 150)
       self.setWindowTitle('Error') 

    def salir(self):
        self.close()


        
if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    ventana = VentanaInicio()
    # procesador_inicio = ProcesadorInicio()
    # ventana.senal_usuario.connect(procesador_inicio.validar_usurio)
    ventana.show()
    sys.exit(app.exec())

    
    
    
