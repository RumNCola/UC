import socket
from math import ceil
from funciones import generar_hash_bloque
import parametros as p
import utilidades as u
import json
import pickle
import os
from time import sleep
from PyQt5.QtCore import QObject, QThread

class EnviarData(QThread):
    """
    Clase hija de QThread que envia archivos
    """
    def __init__(self, cliente_socket, servidor, data):
        super().__init__()
        self.cliente_socket = cliente_socket
        self.servidor = servidor
        self.data = data

        self.pausado = False
        self.detenido = False
    
    def run(self):
        while not self.detenido:
            if not self.pausado:
                self.servidor._enviar(self.data, self.cliente_socket)
                self.detenido = True
    
    def pausa(self):
        self.pausado = True 
    
    def reanudar(self):
        self.pausado = False

    def detener(self):
        self.detenido = True
    

class ClientHandler(QThread):
    """
    Clase destinada a recibir mensajes del cliente
    """
    def __init__(self, cliente_socket, servidor):
        super().__init__()  
        self.cliente_socket = cliente_socket
        self.servidor = servidor
        self.envios = []

    def interpretar_mensajes(self, data):
        """
        Método que interpreta los mensajes de algún cliente
        """
        if 'verificar_usuario' in data['accion']:
            self.servidor.verificar_usuario(data['usuario'], self.cliente_socket) 

        elif 'pedir_usuarios' in data['accion']:
            self.servidor.enviar_usuarios(self.cliente_socket)

        elif 'pedir_archivos_disponibles' in data['accion']:
            self.servidor.enviar_archivos_disponibles(self.cliente_socket)
        
        elif 'enviar_archivo' in data['accion']:
            self.servidor.enviar_archivo(data['archivo'], self.cliente_socket)
          
    def run(self):
        """
        run del thread. Mientras este activo, recibira mensajes. Si se desactiva o se cae,
        se llama a la función que purga a los usuarios desconectados
        """
        try:
            while True:
                contexto = self.cliente_socket.recv(131) #131 porque se envia en chunks de 131
                if not contexto:
                    break
                msg_id = contexto[:64]
                largo = int.from_bytes(contexto[64:68], byteorder = 'big')
                chunks = []
                bytes_recibidos = 0

                while bytes_recibidos < largo:
                    chunk = self.cliente_socket.recv(131)
                    
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
                print(f'Mensaje entrante: {data.keys()}')

                self.interpretar_mensajes(data)

        except (ConnectionResetError, EOFError, ConnectionAbortedError, ConnectionError) as error:
            print(f'Error de Conexion: {error}')
            self.servidor.actualizar_usuarios_desconectados(self.cliente_socket)

        finally:
            self.cliente_socket.close()

class Servidor(QObject):
    def __init__(self):
        super().__init__()
        print('Booting')
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
        self.host = p.SERVER
        self.port = p.PORT
        self.usuarios = dict()
        self.hilos = []
        self.conectar_escuchar()
    
    def conectar_escuchar(self):
        """
        Método básico para que el server se conecte y escuche
        """
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        self.aceptar_conexiones()
    
    def aceptar_conexiones(self):
        """
        método básico para que el server acepte conexiones
        """
        while True:
            client_socket, _ = self.socket_server.accept()
            if client_socket: 
                print('Conexión Entrante') ######
            client_thread = ClientHandler(client_socket, self)
            client_thread.finished.connect(lambda: self.hilos_activos.remove(client_thread))
            self.hilos.append(client_thread)
            client_thread.start()

    def enviar(self, data, socket_cliente):
        """
        Método que crea un thread que envia data
        """
        hilo = EnviarData(socket_cliente, self, data)
        self.hilos.append(hilo)
        hilo.start()

    def _enviar(self, data, socket_cliente): 
        """
        método "oculto" que es usado por un thread para enviar data
        """
        try:
            print(f'Enviando Mensaje: {data}')
            msg_bytes = pickle.dumps(data) #byte
            msg_id = os.urandom(64) #byte
            msg_largo = len(msg_bytes).to_bytes(4, byteorder = 'big') # byte
            chunks = ceil(len(msg_bytes) / 32) #int

            socket_cliente.sendall(msg_id + msg_largo + bytearray([0] * 63)) #Emision del conetxto

            #Emision del contenido
            for i in range(chunks - 1):
                numero_bloque = i.to_bytes(3, byteorder = 'big')
                tramo = msg_bytes[i * 32: (i + 1) * 32]
                hash = generar_hash_bloque(tramo)
                socket_cliente.sendall(numero_bloque + msg_id + hash + tramo) 

            numero_bloque = (chunks - 1).to_bytes(3, byteorder = 'big')
            tramo = msg_bytes[(chunks - 1)*32:]
            complemento = 32 - len(tramo)
            tramo = tramo + bytearray(complemento)
            hash = generar_hash_bloque(tramo)
            socket_cliente.sendall(numero_bloque + msg_id + hash + tramo)

        except (ConnectionError, EOFError, BrokenPipeError) as e:
            print(f'Error de Conexión: {e}')
            
            self.actualizar_usuarios_desconectados(socket_cliente)
    
    def actualizar_usuarios_desconectados(self, socket_cliente):
        """
        Funcion que desconecta a todos los usuarios que se hayan caido.
        Este usa sleeps para evitar que se solape con sigo misma y usa del para el mismo
        proposito.
        """
        sleep(1)
        usuarios_a_desconectar = []
        for key in self.usuarios:
            if self.usuarios[key] == socket_cliente:
                print(f'{key} se ha desconectado!')
                usuarios_a_desconectar.append(key)

        for usuario in usuarios_a_desconectar:
            del self.usuarios[usuario]
            sleep(1)
        print(f'Usuarios conectados: {self.usuarios.keys()}')
        sleep(1) 
    
   
    def verificar_usuario(self, usuario, socket_cliente):
        """
        Función que verifica que un usuario cumpla la sintaxis y que no esté repetido
        """
        valido = True
        if usuario in self.usuarios.keys():
            valido = False
        if not usuario.isalnum():
            valido = False
        elif len(usuario) < 3 or len(usuario) > 16:
            valido = False
        elif sum(map(str.isupper, usuario)) < 1:
            valido = False
        elif sum(map(str.isdigit, usuario)) < 1:
            valido = False
        if valido:
            self.usuarios[usuario] = socket_cliente
        
        print(f'Verificación Iniciada. Estado: {valido}')
        mensaje = {'valido': valido, 'usuario': usuario}
        self.enviar(mensaje, socket_cliente)

    def enviar_archivos_disponibles(self, socket_cliente):
        """
        Función que envia los archivos disponibles la cliente 
        """ 
        data = {'archivos_disponibles': u.identificador_archivos('./servidor/archivos')}
        self.enviar(data, socket_cliente)
    
    def enviar_usuarios(self, socket_cliente):
        """
        función que envia una lista con tuplas de usuarios/sockets al cliente
        """
        usuarios = []
        for usuario in self.usuarios.keys():
            usuarios.append(usuario)
        data = {'usuarios_conectados': usuarios}
        self.enviar(data, socket_cliente)
    
    def es_valido_archivo(self, archivo: str) -> bool:
        """
        Método Auxiliar que revisa si un archivo existe en los archivos de servidor
        y retorna un booleano de acuerdo a la existencia
        """
        archivo = archivo.split('.')[0] 
        directorio = (u.identificador_archivos('./servidor/archivos'))
        for file in directorio:
            if file[0] in archivo:
                return True         
        return False

    def enviar_archivo(self, archivo: str, socket_cliente: socket):
        """
        Método que recibe un nombre de archivo y lo envia a un socket
        """
        if self.es_valido_archivo(archivo):
            nombre_archivo = u.nombre_completo(archivo)
            print(nombre_archivo)
            ruta = os.path.join('./servidor/archivos', nombre_archivo)
            print(ruta)

            with open(ruta, 'rb') as file:
                archivo = file.read()

            data = {'archivo_existe': True, 'archivo_completo': archivo, 
                    'nombre_archivo': nombre_archivo }
        else:
            data = {'archivo_existe': False}

        self.enviar(data, socket_cliente) 

            
if __name__ == '__main__':
    servidor = Servidor()


