"""
Definición de las categorías léxicas (tipos de token) reconocidas por el
analizador léxico del subconjunto de Prolog especificado en el enunciado
de la tarea (Teoría de la Computación, INFO1148, 2do semestre 2026).

Cada valor del enum corresponde a una de las categorías léxicas descritas
en la sección 3 del enunciado ("Categorías léxicas de Prolog").
"""

from enum import Enum, auto


class TipoToken(Enum):
    # --- Identificadores y literales ---
    ATOMO = auto()            # átomo no entrecomillado: padre, persona_1, is, mod
    ATOMO_COMILLAS = auto()   # átomo entrecomillado: 'Juan Pérez', ':-'
    VARIABLE = auto()         # X, Persona, _Temporal, _  (variable anónima)
    ENTERO = auto()           # 123, 0
    REAL = auto()             # 3.14, 6.022e23
    CADENA = auto()           # "texto"

    # --- Operadores de cláusula / consulta ---
    OP_CLAUSULA = auto()      # :-   ?-   -->

    # --- Operadores de unificación / comparación ---
    OP_RELACIONAL = auto()    # =  \=  ==  \==  =..  <  =<  >  >=

    # --- Operadores aritméticos simbólicos (is, mod son ATOMO) ---
    OP_ARITMETICO = auto()    # +  -  *  /  //  **

    # --- Operadores de control ---
    OP_CONTROL = auto()       # \+  !  ;

    # --- Delimitadores ---
    COMA = auto()              # ,
    PUNTO = auto()              # .  (fin de cláusula)
    PARENTESIS_IZQ = auto()    # (
    PARENTESIS_DER = auto()    # )
    CORCHETE_IZQ = auto()      # [
    CORCHETE_DER = auto()      # ]
    LLAVE_IZQ = auto()          # {
    LLAVE_DER = auto()          # }
    BARRA_VERTICAL = auto()    # |

    EOF = auto()


class Token:
    """
    Representa un token reconocido: tipo, lexema, posición (línea/columna
    donde inicia) y, opcionalmente, un valor decodificado (atributo) y el
    índice que ocupa en la tabla de lexemas.
    """

    __slots__ = ("tipo", "lexema", "linea", "columna", "valor", "indice_tabla")

    def __init__(self, tipo, lexema, linea, columna, valor=None, indice_tabla=None):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
        self.valor = valor
        self.indice_tabla = indice_tabla

    def __repr__(self):
        # Formato solicitado en el enunciado: <TIPO, 'lexema', linea, columna>
        return f"<{self.tipo.name}, {self.lexema!r}, {self.linea}, {self.columna}>"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        return (self.tipo, self.lexema, self.linea, self.columna) == (
            other.tipo, other.lexema, other.linea, other.columna,
        )

    def __hash__(self):
        return hash((self.tipo, self.lexema, self.linea, self.columna))
