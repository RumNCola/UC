import unittest
from threading import Event
from unittest.mock import patch
from tests_publicos.utils import FakeLock, timeout
from main import Carrera, Jugador, Bandera

N_SECOND = 1


class VerificarCarrera(unittest.TestCase):
    def setUp(self) -> None:
        bandera = Bandera()
        lock_bandera = FakeLock()
        lock_carrera = FakeLock()
        senal_inicio = Event()
        senal_fin = Event()

        # Instancia los corredores y la carrera
        self.j1 = Jugador(
            "Alice", bandera, lock_bandera, senal_inicio, senal_fin, lock_carrera
        )
        self.j2 = Jugador(
            "Shion", bandera, lock_bandera, senal_inicio, senal_fin, lock_carrera
        )
        self.j3 = Jugador(
            "Asuna", bandera, lock_bandera, senal_inicio, senal_fin, lock_carrera
        )

        self.j1.agregar_rival(self.j2)
        self.j1.agregar_rival(self.j3)

        Jugador.TIEMPO_ESPERA = 0
        Jugador.PORCENTAJE_MIN = 100
        Jugador.PORCENTAJE_MAX = 100
        Jugador.PROBABILIDAD_ROBAR = 1

        self.carrera = Carrera(self.j1, self.j2, self.j3, senal_inicio, senal_fin)

    @timeout(N_SECOND)
    def test_carrera_valor_daemon(self):
        """
        Se verifica que el programa espere al thread antes de finalizar
        """
        self.assertFalse(self.carrera.daemon)

    @timeout(N_SECOND)
    @patch("threading.Thread.join")
    def test_run_inicia_threads(self, new_join):
        """
        Se verifica la inicialización de los 3 threads.
        """
        with patch("threading.Thread.start") as mock:
            self.carrera.run()
            self.assertEqual(mock.call_count, 3)

    @timeout(N_SECOND)
    @patch("threading.Thread.join")
    @patch("threading.Thread.start")
    def test_run_senal_inicio(self, new_start, new_join):
        """
        Se verifica el uso de Eventos para avisar el inicio de la carrera.
        """
        with patch("threading.Event.set") as mock:
            self.carrera.run()
            mock.assert_called()

    @timeout(N_SECOND)
    @patch("threading.Thread.join")
    @patch("threading.Thread.start")
    def test_run_senal_inicio_fue_seteada(self, new_start, new_join):
        """
        Se verifica que la señal de inicio fue la seteada y no otra
        """
        self.carrera.run()
        self.assertTrue(self.carrera.senal_inicio.is_set())

    @timeout(N_SECOND)
    @patch("threading.Thread.start")
    def test_run_espera_jugadores(self, new_start):
        """
        Se verifica el uso de join en la carrera.
        """
        with patch("threading.Thread.join") as mock:
            self.carrera.run()
            self.assertEqual(mock.call_count, 3)
