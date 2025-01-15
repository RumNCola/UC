import os
import time
from datetime import datetime
from threading import Thread
from parametros import TIEMPO_ENTRE_REPRODUCCIONES, RUTA_ARCHIVOS, HORAS_ESPECIALES
from gtts import gTTS
from playsound import playsound

class Reproductor(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True  # Hilo en modo demonio
        self.ruta_archivos = RUTA_ARCHIVOS
        self.tiempo_entre_reproducciones = TIEMPO_ENTRE_REPRODUCCIONES * 60  # Convertir a segundos
        self.horas_especiales = HORAS_ESPECIALES

    def run(self):
        """
        Método principal que ejecuta la reproducción de audios y archivos de texto.
        """
        while True:
            # Obtener los archivos actuales
            archivos = self.obtener_archivos()
            if not archivos:
                print("No hay archivos en la carpeta. Esperando...")
                time.sleep(60)
                continue

            # Calcular el intervalo entre reproducciones
            intervalo = self.tiempo_entre_reproducciones / len(archivos)

            for idx, archivo in enumerate(archivos):
                ahora = datetime.now()
                hora_actual = int(ahora.strftime('%H%M'))

                # Comprobar si el archivo es especial
                if archivo.endswith('.txt') and hora_actual in self.horas_especiales:
                    print(f"Reproduciendo archivo especial: {archivo}")
                    self.reproducir_txt(archivo)
                elif archivo.endswith('.txt'):
                    # Archivos .txt normales
                    print(f"Reproduciendo archivo de texto: {archivo}")
                    self.reproducir_txt(archivo)
                else:
                    # Archivos de audio
                    print(f"Reproduciendo archivo de audio: {archivo}")
                    self.reproducir_audio(archivo)

                # Pausar antes de reproducir el siguiente archivo
                if idx < len(archivos) - 1:
                    print(f"Esperando {intervalo} segundos para el siguiente archivo.")
                    time.sleep(intervalo)

    def obtener_archivos(self):
        """
        Obtiene una lista de los archivos en la carpeta definida.
        """
        if not os.path.exists(self.ruta_archivos):
            os.makedirs(self.ruta_archivos)
        return sorted(os.listdir(self.ruta_archivos))

    def reproducir_txt(self, archivo):
        """
        Convierte un archivo de texto a voz y lo reproduce.
        """
        ruta_completa = os.path.join(self.ruta_archivos, archivo)
        with open(ruta_completa, 'r', encoding='utf-8') as file:
            texto = file.read()

        tts = gTTS(text=texto, lang='es')
        archivo_tts = ruta_completa.replace('.txt', '.mp3')
        tts.save(archivo_tts)
        playsound(archivo_tts)
        os.remove(archivo_tts)  # Opcional: elimina el archivo TTS generado

    def reproducir_audio(self, archivo):
        """
        Reproduce un archivo de audio.
        """
        ruta_completa = os.path.join(self.ruta_archivos, archivo)
        playsound(ruta_completa)

if __name__ == "__main__":
    reproductor = Reproductor()
    reproductor.start()

    # Mantener el programa corriendo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Saliendo del programa...")
