from dataclasses import dataclass
from typing import Tuple

@dataclass
class UnoConfig:
    NUMEROS_POR_COLOR: Tuple[int, ...] = tuple(range(10))
    CARTAS_ESPECIALES_POR_TIPO: int = 2
    CARTAS_COMODIN_MAS2: int = 4
    CARTAS_COMODIN_MAS4: int = 4
    CARTAS_COMODIN_CAMBIOCOLOR: int = 4
    CARTAS_INICIALES_JUGADOR: int = 7
    CARTAS_ROBAR_MAS2: int = 2
    CARTAS_ROBAR_MAS4: int = 4
    EXTENSION_GUARDADO: str = ".pkl"
    RUTA_GUARDADOS: str = "./"
