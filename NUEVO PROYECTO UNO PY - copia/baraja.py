import random
from typing import Optional, List
from models import Color, TipoCarta
from cartas import Carta, CartaNumerica, CartaEspecial


class Baraja:
    def __init__(self) -> None:
        self.cartas: List[Carta] = []
        self.descarte: List[Carta] = []
        self._inicializar()

    def _inicializar(self) -> None:
        colores = [Color.ROJO, Color.AMARILLO, Color.VERDE, Color.AZUL]

        for color in colores:
            for numero in range(10):
                self.cartas.append(CartaNumerica(color, numero))

        for color in colores:
            for _ in range(2):
                self.cartas.append(CartaEspecial(color, TipoCarta.REVERSE))
                self.cartas.append(CartaEspecial(color, TipoCarta.BLOQUEO))
                self.cartas.append(CartaEspecial(color, TipoCarta.MAS2))

        for _ in range(4):
            self.cartas.append(CartaEspecial(Color.NEGRO, TipoCarta.MAS4))
            self.cartas.append(CartaEspecial(Color.NEGRO, TipoCarta.CAMBIOCOLOR))

        random.shuffle(self.cartas)

    def robar_carta(self) -> Optional[Carta]:
        if not self.cartas:
            self._reciclar_descarte()
        
        if not self.cartas:
            return None
        
        return self.cartas.pop(0)

    def descartar(self, carta: Carta) -> None:
        self.descarte.append(carta)

    def _reciclar_descarte(self) -> None:
        if not self.descarte:
            return
        
        print("--- Reciclando descarte ---")
        self.cartas.extend(self.descarte)
        self.descarte.clear()
        random.shuffle(self.cartas)

    def contar_cartas(self) -> int:
        return len(self.cartas) + len(self.descarte)
