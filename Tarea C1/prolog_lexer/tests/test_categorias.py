"""
Pruebas de reconocimiento de cada categoría léxica definida en la
sección 3 del enunciado. Constituyen el corpus de "pruebas válidas"
(> 20 casos) solicitado en la sección 6.
"""

import pytest

from conftest import tokenizar, T


CASOS_VALIDOS = [
    # Átomos no entrecomillados
    ("padre", [(T.ATOMO, "padre")]),
    ("persona_1", [(T.ATOMO, "persona_1")]),
    ("is", [(T.ATOMO, "is")]),
    ("mod", [(T.ATOMO, "mod")]),

    # Átomos entrecomillados
    ("'Juan Pérez'", [(T.ATOMO_COMILLAS, "'Juan Pérez'")]),
    ("':-'", [(T.ATOMO_COMILLAS, "':-'")]),

    # Variables
    ("X", [(T.VARIABLE, "X")]),
    ("Persona", [(T.VARIABLE, "Persona")]),
    ("_Temporal", [(T.VARIABLE, "_Temporal")]),
    ("_", [(T.VARIABLE, "_")]),

    # Números
    ("42", [(T.ENTERO, "42")]),
    ("0", [(T.ENTERO, "0")]),
    ("3.14", [(T.REAL, "3.14")]),
    ("6.022e23", [(T.REAL, "6.022e23")]),
    ("1E10", [(T.REAL, "1E10")]),

    # Cadenas
    ('"hola"', [(T.CADENA, '"hola"')]),
    ('"linea\\ncon escape"', [(T.CADENA, '"linea\\ncon escape"')]),

    # Operadores de cláusula/consulta
    (":-", [(T.OP_CLAUSULA, ":-")]),
    ("?-", [(T.OP_CLAUSULA, "?-")]),
    ("-->", [(T.OP_CLAUSULA, "-->")]),

    # Operadores relacionales
    ("=", [(T.OP_RELACIONAL, "=")]),
    ("\\=", [(T.OP_RELACIONAL, "\\=")]),
    ("==", [(T.OP_RELACIONAL, "==")]),
    ("\\==", [(T.OP_RELACIONAL, "\\==")]),
    ("=..", [(T.OP_RELACIONAL, "=..")]),
    ("<", [(T.OP_RELACIONAL, "<")]),
    ("=<", [(T.OP_RELACIONAL, "=<")]),
    (">", [(T.OP_RELACIONAL, ">")]),
    (">=", [(T.OP_RELACIONAL, ">=")]),

    # Operadores aritméticos
    ("+", [(T.OP_ARITMETICO, "+")]),
    ("-", [(T.OP_ARITMETICO, "-")]),
    ("*", [(T.OP_ARITMETICO, "*")]),
    ("/", [(T.OP_ARITMETICO, "/")]),
    ("//", [(T.OP_ARITMETICO, "//")]),
    ("**", [(T.OP_ARITMETICO, "**")]),

    # Operadores de control
    ("\\+", [(T.OP_CONTROL, "\\+")]),
    ("!", [(T.OP_CONTROL, "!")]),
    (";", [(T.OP_CONTROL, ";")]),

    # Delimitadores
    (",", [(T.COMA, ",")]),
    (".", [(T.PUNTO, ".")]),
    ("(", [(T.PARENTESIS_IZQ, "(")]),
    (")", [(T.PARENTESIS_DER, ")")]),
    ("[", [(T.CORCHETE_IZQ, "[")]),
    ("]", [(T.CORCHETE_DER, "]")]),
    ("{", [(T.LLAVE_IZQ, "{")]),
    ("}", [(T.LLAVE_DER, "}")]),
    ("|", [(T.BARRA_VERTICAL, "|")]),
]


@pytest.mark.parametrize("fuente, esperado", CASOS_VALIDOS)
def test_categoria_valida(fuente, esperado):
    tokens, errores, _ = tokenizar(fuente)
    assert errores == []
    assert tokens == esperado


def test_cuenta_minima_de_casos_validos():
    assert len(CASOS_VALIDOS) >= 20
