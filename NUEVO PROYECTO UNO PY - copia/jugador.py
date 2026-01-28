from typing import List
from models import Color
from cartas import Carta
from baraja import Baraja


class Jugador:
    def __init__(self, nombre: str, baraja: Baraja) -> None:
        self.nombre = nombre
        self.mano: List[Carta] = []
        
        for _ in range(7):
            carta = baraja.robar_carta()
            if carta:
                self.mano.append(carta)

    @property
    def nombre_jugador(self) -> str:
        return self.nombre

    @property
    def mano_actual(self) -> List[Carta]:
        return self.mano.copy()

    @property
    def cantidad_cartas(self) -> int:
        return len(self.mano)

    def get_mano(self) -> List[Carta]:
        return self.mano

    def get_nombre(self) -> str:
        return self.nombre

    def agregar_carta(self, carta: Carta) -> None:
        if carta:
            self.mano.append(carta)

    def jugar_carta(self, indice: int) -> Carta:
        if not 0 <= indice < len(self.mano):
            raise IndexError(f"Índice {indice} fuera de rango")
        
        return self.mano.pop(indice)

    def tiene_jugada_posible(self, carta_en_mesa: Carta) -> bool:
        for carta in self.mano:
            if carta.es_compatible(carta_en_mesa):
                return True
        return False

    def obtener_indice_carta_compatible(self, carta_en_mesa: Carta) -> int:
        for indice, carta in enumerate(self.mano):
            if carta.es_compatible(carta_en_mesa):
                return indice
        return -1

    def mostrar_mano(self) -> None:
        print(f"\nMano de {self.nombre}:")
        for i, carta in enumerate(self.mano):
            print(f"[{i}] {carta}")
