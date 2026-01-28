import random
import pickle
import os
from typing import Optional
from models import Color, TipoCarta
from cartas import Carta
from baraja import Baraja
from jugador import Jugador


class JuegoUno:
    def __init__(self) -> None:
        self.baraja = Baraja()
        self.humano = Jugador("Jugador", self.baraja)
        self.maquina = Jugador("Máquina", self.baraja)
        self.carta_en_mesa: Optional[Carta] = None
        self.saltar_turno = False
        
        self._inicializar_carta_mesa()

    def _inicializar_carta_mesa(self) -> None:
        while True:
            self.carta_en_mesa = self.baraja.robar_carta()
            if self.carta_en_mesa and not self.carta_en_mesa.es_carta_comodin:
                break
            if self.carta_en_mesa:
                self.baraja.descartar(self.carta_en_mesa)
        
        self.baraja.descartar(self.carta_en_mesa)

    def procesar_turno(self, actual: Jugador, oponente: Jugador) -> bool:
        print("\n" + "-"*40)
        print(f"Carta en mesa: {self.carta_en_mesa}")

        if actual == self.humano:
            actual.mostrar_mano()
            print(f"Oponente tiene {len(oponente.get_mano())} cartas.")
        else:
            print("Turno de la Máquina...")

        if not actual.tiene_jugada_posible(self.carta_en_mesa):
            print(f"{actual.get_nombre()} no tiene jugadas. Roba una carta.")
            robada = self.baraja.robar_carta()
            if robada:
                actual.agregar_carta(robada)
                if actual == self.humano:
                    print(f"Robaste: {robada}")
            return True

        if actual == self.humano:
            indice = self._pedir_entrada_jugador()
            if indice == -999:
                return False
        else:
            indice = self._obtener_jugada_ia()

        if indice == -1:
            return True

        carta_jugada = actual.jugar_carta(indice)
        print(f"{actual.get_nombre()} jugó: {carta_jugada}")

        if carta_jugada.color == Color.NEGRO:
            nuevo_color = self._pedir_color() if actual == self.humano else self.elegir_color_random()
            carta_jugada.set_color(nuevo_color)
            print(f"Color cambiado a: {nuevo_color.get_codigo()}")

        self.baraja.descartar(self.carta_en_mesa)
        self.carta_en_mesa = carta_jugada

        self._aplicar_efectos(carta_jugada, oponente)
        return True

    def _pedir_entrada_jugador(self) -> int:
        while True:
            print("Elige índice de carta (o 'G' para Guardar y Salir): ", end="")
            entrada = input().strip().upper()
            
            if entrada == 'G':
                self.guardar_partida("partida_guardada")
                print("Partida guardada. ¡Hasta luego!")
                return -999

            try:
                idx = int(entrada)
                if 0 <= idx < len(self.humano.get_mano()):
                    carta = self.humano.get_mano()[idx]
                    if carta.es_compatible(self.carta_en_mesa):
                        return idx
                    print("Carta no compatible.")
                else:
                    print("Índice fuera de rango.")
            except ValueError:
                print("Entrada inválida.")

    def _obtener_jugada_ia(self) -> int:
        return self.maquina.obtener_indice_carta_compatible(self.carta_en_mesa)

    def _aplicar_efectos(self, carta: Carta, oponente: Jugador) -> None:
        tipo = carta.get_tipo()
        cartas_a_robar = 0

        if tipo == TipoCarta.MAS2:
            cartas_a_robar = 2
        elif tipo == TipoCarta.MAS4:
            cartas_a_robar = 4

        if cartas_a_robar > 0:
            print(f"{oponente.get_nombre()} roba {cartas_a_robar} cartas!")
            for _ in range(cartas_a_robar):
                c = self.baraja.robar_carta()
                if c:
                    oponente.agregar_carta(c)

        if tipo in [TipoCarta.BLOQUEO, TipoCarta.REVERSE] or cartas_a_robar > 0:
            self.saltar_turno = True

    def _pedir_color(self) -> Color:
        while True:
            entrada = input("Elige color (R, A, V, Z): ").strip().upper()
            if entrada == "R":
                return Color.ROJO
            elif entrada == "A":
                return Color.AMARILLO
            elif entrada == "V":
                return Color.VERDE
            elif entrada == "Z":
                return Color.AZUL
            else:
                print("Color inválido.")

    def elegir_color_random(self) -> Color:
        return random.choice([Color.ROJO, Color.AMARILLO, Color.VERDE, Color.AZUL])

    def verificar_ganador(self, jugador: Jugador) -> bool:
        if len(jugador.get_mano()) == 1:
            print(f"{jugador.get_nombre()}: ¡UNO!")
        if not jugador.get_mano():
            print(f"¡{jugador.get_nombre()} HA GANADO!")
            return True
        return False

    def guardar_partida(self, nombre_archivo: str) -> None:
        if not nombre_archivo.endswith(".pkl"):
            nombre_archivo += ".pkl"
        
        try:
            with open(nombre_archivo, "wb") as f:
                pickle.dump(self, f)
            print(f"Partida guardada: {nombre_archivo}")
        except Exception as e:
            print(f"Error al guardar: {e}")

    @staticmethod
    def cargar_partida(nombre_archivo: str) -> Optional['JuegoUno']:
        if not os.path.exists(nombre_archivo):
            return None
        
        try:
            with open(nombre_archivo, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error al cargar: {e}")
            return None

    def iniciar(self) -> None:
        print("\n--- ¡COMIENZA EL JUEGO! ---")
        print(f"Carta inicial: {self.carta_en_mesa}")
        
        while True:
            if not self.saltar_turno:
                continuar = self.procesar_turno(self.humano, self.maquina)
                if not continuar:
                    return
                if self.verificar_ganador(self.humano):
                    break
            else:
                print("¡Tu turno fue saltado!")
                self.saltar_turno = False

            if not self.saltar_turno:
                self.procesar_turno(self.maquina, self.humano)
                if self.verificar_ganador(self.maquina):
                    break
            else:
                print("¡Turno de Máquina saltado!")
                self.saltar_turno = False
