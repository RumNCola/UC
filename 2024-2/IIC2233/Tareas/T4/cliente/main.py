import sys
from PyQt5.QtWidgets import QApplication
from backend.cliente import Cliente
from frontend.ventana_inicio_error import VentanaInicio
from frontend.ventana_archivos import VentanaMisArchivos
from frontend.ventana_descargas import VentanaDescargas

if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type) 
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    cliente = Cliente() 
    descargas = VentanaDescargas()
    ventana_inicio = VentanaInicio(descargas) #eventualmente la ventana de misarchivos ira acá
   
    #Enchufar señales
    ventana_inicio.senal_usuario.connect(cliente.validar_usuario)
    cliente.senal_exito_login.connect(ventana_inicio.login_exitoso)
    cliente.senal_error_login.connect(ventana_inicio.login_falso)
    cliente.senal_archivos_disponibles.connect(descargas.actualizar_archivos)
    cliente.senal_usuarios_conectados.connect(descargas.actualizar_usuarios)
    cliente.senal_error.connect(descargas.error)
    descargas.senal_usuarios.connect(cliente.pedir_usuarios_conectados)
    descargas.senal_archivos.connect(cliente.pedir_archivos_disponibles)
    descargas.senal_descarga.connect(cliente.pedir_archivo)
   
    ventana_inicio.show()
    # ventana = VentanaMisArchivos()
    # ventana.show()
    sys.exit(app.exec())