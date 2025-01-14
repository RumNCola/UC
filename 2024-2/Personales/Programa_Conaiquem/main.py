from frontend.Ventanas import VentanaMain, VentanaAgregar, VentanaNombreAgregar
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type) 
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    ventana = VentanaMain()
    ventana.show()
    sys.exit(app.exec())