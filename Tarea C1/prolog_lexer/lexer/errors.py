"""
Representación de los errores léxicos detectados por el analizador.
"""


class ErrorLexico:
    """
    Encapsula un error léxico: un mensaje descriptivo, el fragmento de
    texto problemático y su ubicación (línea y columna de inicio).
    """

    def __init__(self, mensaje, fragmento, linea, columna):
        self.mensaje = mensaje
        self.fragmento = fragmento
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return (
            f"[ERROR LÉXICO] {self.mensaje}: {self.fragmento!r} "
            f"(línea {self.linea}, columna {self.columna})"
        )

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, ErrorLexico):
            return NotImplemented
        return (self.mensaje, self.fragmento, self.linea, self.columna) == (
            other.mensaje, other.fragmento, other.linea, other.columna,
        )

    def __hash__(self):
        return hash((self.mensaje, self.fragmento, self.linea, self.columna))
