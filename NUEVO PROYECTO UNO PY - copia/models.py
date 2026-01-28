from enum import Enum

class TipoCarta(Enum):
    NUMERO = (False, "")
    REVERSE = (True, "^")
    BLOQUEO = (True, "&")
    MAS2 = (True, "+2")
    MAS4 = (True, "+4")
    CAMBIOCOLOR = (True, "%")

    def __init__(self, es_comodin: bool, simbolo: str) -> None:
        self._es_comodin = es_comodin
        self.simbolo = simbolo

    @property
    def es_comodin(self) -> bool:
        return self._es_comodin

class Color(Enum):
    ROJO = "R"
    AMARILLO = "A"
    VERDE = "V"
    AZUL = "Z"
    NEGRO = "N"
    NINGUNO = ""

    def get_codigo(self) -> str:
        return self.value
