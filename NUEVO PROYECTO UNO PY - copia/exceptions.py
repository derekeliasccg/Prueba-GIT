class UnoException(Exception):
    pass

class CartaIncompatibleError(UnoException):
    pass

class JugadaInvalidaError(UnoException):
    pass

class BarajaVaciaError(UnoException):
    pass

class JugadorNoEncontradoError(UnoException):
    pass
