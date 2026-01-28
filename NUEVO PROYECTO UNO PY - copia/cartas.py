from abc import ABC, abstractmethod
from models import Color, TipoCarta

class Carta(ABC):
    def __init__(self, color: Color, tipo: TipoCarta) -> None:
        self.color = color
        self.tipo = tipo

    @property
    def es_carta_comodin(self) -> bool:
        return self.tipo.es_comodin

    def set_color(self, nuevo_color: Color) -> None:
        self.color = nuevo_color

    def es_compatible(self, otra_carta: 'Carta') -> bool:
        if self.color == Color.NEGRO:
            return True
        return self.color == otra_carta.color

    def get_tipo(self) -> TipoCarta:
        return self.tipo

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.__str__()


class CartaNumerica(Carta):
    def __init__(self, color: Color, numero: int) -> None:
        if not 0 <= numero <= 9:
            raise ValueError(f"Número inválido: {numero}")
        super().__init__(color, TipoCarta.NUMERO)
        self.numero = numero

    def get_numero(self) -> int:
        return self.numero

    def es_compatible(self, otra_carta: Carta) -> bool:
        if super().es_compatible(otra_carta):
            return True
        if isinstance(otra_carta, CartaNumerica):
            return self.numero == otra_carta.numero
        return False

    def __str__(self) -> str:
        return f"{self.color.get_codigo()} {self.numero}"


class CartaEspecial(Carta):
    def __init__(self, color: Color, tipo: TipoCarta) -> None:
        if tipo == TipoCarta.NUMERO:
            raise ValueError("Use CartaNumerica para cartas numéricas")
        super().__init__(color, tipo)

    def es_compatible(self, otra_carta: Carta) -> bool:
        if self.tipo == otra_carta.tipo:
            return True
        if otra_carta.get_tipo().es_comodin:
            return self.color == otra_carta.color
        if self.color == Color.NEGRO:
            return True
        if self.color == otra_carta.color:
            return True
        return False

    def __str__(self) -> str:
        codigo_color = "N" if self.color == Color.NEGRO else self.color.get_codigo()
        return f"{self.tipo.simbolo} {codigo_color}"
