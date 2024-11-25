from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication, QThread
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
import socket
import os
from sys import exit
import pickle
from math import ceil
import parametros as p
from funciones import generar_hash_bloque
from threading import Thread

class EnviarData(QThread):
    """
    Clase hija de QThread que envia archivos
    """
    def __init__(self, cliente_socket, cliente, data):
        super().__init__()
        self.cliente_socket = cliente_socket
        self.data = data
        self.cliente = cliente

        self.pausado = False
        self.detenido = False
    
    def run(self):
        while not self.detenido:
            if not self.pausado:
                self.cliente._enviar(self.data)
                self.detenido = True
    
    def pausa(self):
        self.pausado = True 
    
    def reanudar(self):
        self.pausado = False

    def detener(self):
        self.detenido = True

class Cliente(QObject):
    """
    Procesa solicitudes de la ventana inicial
    """
    #Señal que para indicar login exitoso
    senal_exito_login = pyqtSignal(str) 

    #Señal para indicar login no exitoso
    senal_error_login = pyqtSignal(str)

    #señal para usuarios conectados
    senal_usuarios_conectados = pyqtSignal(list)

    #Señal para archivos disponibles
    senal_archivos_disponibles = pyqtSignal(list)

    #Señal para desplegar popups de errores
    senal_error = pyqtSignal(str)
    

    def __init__(self):
        super().__init__()
        self.server = p.SERVER
        self.port = p.PORT
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectado = False
        self.envios_activos = []
        self.conectar_servidor()

    def desconexion(self):
        """
        Método que al ocurrir la desconexión crea un popup que cierra el cliente.
        """
        ventana = QWidget()
        boton = QPushButton('Cerrar', ventana)
        boton.clicked.connect(exit)
        etiqueta = QLabel('Se ha caido la conexión al server', ventana)

        box = QVBoxLayout()
        box.addStretch(1)
        box.addWidget(etiqueta)
        box.addStretch(1)
        box.addWidget(boton)
        box.addStretch

        ventana.setLayout(box)
        ventana.setWindowTitle('Fatal Error')
        ventana.resize(200,100)
        self.ventana = ventana
        self.ventana.show()
        
    
    def conectar_servidor(self):
        """
        Método básico para conectarse la server
        """
        try:
            self.socket_cliente.connect((self.server, self.port))
            self.conectado = True
            self.thread_escuchar = QThread()
            self.thread_escuchar.run = self.escuchar
            self.thread_escuchar.start()

        except (ConnectionError, BrokenPipeError, EOFError):
            self.socket_cliente.close()
            self.conectado = False
            self.desconexion()
        
    def enviar(self, data):
        """
        Método publico para enviar data. Crea un thread y hace que los envios
        no esten acoplados
        """
        hilo = EnviarData(self.socket_cliente, self, data)
        self.envios_activos.append(hilo)
        hilo.start()

    def _enviar(self, data): 
        """
        Método privado para enviar data. Usa la codifiación del enunciado.
        """
        try:
            print(f'Enviando Mensaje: {data}')
            msg_bytes = pickle.dumps(data) #byte
            msg_id = os.urandom(64) #byte
            msg_largo = len(msg_bytes).to_bytes(4, byteorder = 'big') # byte
            chunks = ceil(len(msg_bytes) / 32) #int

            self.socket_cliente.sendall(msg_id + msg_largo + bytearray([0] * 63)) 

            #Emision del contenido
            for i in range(chunks - 1):
                numero_bloque = i.to_bytes(3, byteorder = 'big')
                tramo = msg_bytes[i * 32: (i + 1) * 32]
                hash = generar_hash_bloque(tramo)
                self.socket_cliente.sendall(numero_bloque + msg_id + hash + tramo) 

            numero_bloque = (chunks - 1).to_bytes(3, byteorder = 'big')
            tramo = msg_bytes[(chunks - 1)*32:]
            complemento = 32 - len(tramo)
            tramo = tramo + bytearray(complemento)
            hash = generar_hash_bloque(tramo)
            self.socket_cliente.sendall(numero_bloque + msg_id + hash + tramo)

        except (ConnectionResetError, OSError, BrokenPipeError, ConnectionError, EOFError) as error:
            print(f'Error al enviar archivo: {error}')
            self.socket_cliente.close()
            self.conectado = False
            self.desconexion()

    def escuchar(self):
        """
        Método para escuchar mensajes. Este estará activo siempre, pero si se cae se 
        cierra el socket y se cambia el estado de conectado a False
        """
        try:
            while self.conectado:
                contexto = self.socket_cliente.recv(131) #131 porque se envia en chunks de 131
                if not contexto:
                    break
                msg_id = contexto[:64]
                largo = int.from_bytes(contexto[64:68], byteorder = 'big')
                chunks = []
                bytes_recibidos = 0

                while bytes_recibidos < largo:
                    chunk = self.socket_cliente.recv(131)
                    
                    if not chunk:
                        break
                    num_bloque = chunk[:3]
                    hash = chunk[67:99]
                    contenido = chunk[99:]

                    if chunk[3:67] != msg_id:
                        continue
                    chunks.append(contenido)
                    bytes_recibidos += len(contenido)
                msg_completo = b''.join(chunks)
                data = pickle.loads(msg_completo)
                print(f'Mensaje: {data.keys()} \n')

                self.interpretar_mensajes(data)

        except (ConnectionResetError, OSError, BrokenPipeError, ConnectionError, EOFError) as error:
            print(f'Error al conectar al servidor: {error}')
            self.socket_cliente.close()
            self.conectado = False
            self.desconexion()

    def conectar_peer(self, peer):
        pass

    def interpretar_mensajes(self, data):
        """
        Método que interpreta mensajes
        """
        if 'valido' in data and data['valido'] == True:
            self.senal_exito_login.emit(data['usuario'])

        elif 'valido' in data and not data['valido']:
            self.senal_error_login.emit(data['usuario'])

        elif 'archivos_disponibles' in data:
            #El archivo emitido es una lista con tuplas
            self.senal_archivos_disponibles.emit(data['archivos_disponibles'])

        elif 'usuarios_conectados' in data:
            #se emite una lista de tuplas (usuario,socket)
            self.senal_usuarios_conectados.emit(data['usuarios_conectados'])

        ####ESTO NO SE DEBERïa emitir
        elif 'archivo_existe' in data:
            if data['archivo_existe']:
                self.guardar_archivo(data)
            else:
                self.senal_error.emit('Archivo no encontrado')


    def validar_usuario(self, usuario: str):
        """
        Función que envia el usuario al servidor para verificar si es válido
        """
        mensaje = {'accion': 'verificar_usuario', 'usuario': usuario}
        if self.conectado:
            self.enviar(mensaje)
        else:
            print(f'Error: no se esta conectado')
    
    def pedir_usuarios_conectados(self):
        """
        Método que pide la lista de usuarios conectados al server
        """
        mensaje = {'accion': 'pedir_usuarios'}
        if self.conectado:
            self.enviar(mensaje)
        else:
            print(f'Error: No se esta conectado')

    def pedir_archivos_disponibles(self):
        """
        Método que pide la lista de archivos disponibles
        """
        mensaje = {'accion': 'pedir_archivos_disponibles'}
        if self.conectado:
            self.enviar(mensaje)
        else:
            print(f'Error: No se está conectado') #Este print no debería ocurrir nunca por
                                #como el server maneja el usuario, pero lo dejo por si acaso

    def pedir_archivo(self, archivo: str):
        """
        Método que pide al servidor un archivo para descargarlo
        """
        data = {'accion': 'enviar_archivo', 'archivo': archivo}
        self.enviar(data)
    
    def cambiar_proceso(self, estado: str):
        """
        Método que cambia el estado de una descarga
        """
        data = {'accion': 'cambiar_proceso', 'estado': estado}
        if estado == 'reanudar' or estado == 'pausa' or estado == 'cancelar':
            self.enviar(data)
       
    def obtener_estado(self):
        """
        Método que obtiene le estado de una descarga
        """
        data = {'accion': 'obtener_estado'}
        self.enviar(data)

    def guardar_archivo(self, data):
        """
        Método que recibe un archivo y lo guarda en la carpeta archivos del cliente
        """
        ruta = os.path.join('./cliente/archivos', data['nombre_archivo'])

        with open(ruta, 'wb') as file:
            file.write(data['archivo_completo'])
    

        
        








