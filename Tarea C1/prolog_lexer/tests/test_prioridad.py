"""
Casos de máxima coincidencia (maximal munch) y prioridad entre átomos,
variables y operadores de uno o varios caracteres, solicitados en la
sección 6 del enunciado.
"""

import pytest

from conftest import tokenizar, T


CASOS_PRIORIDAD = [
    # '=..' debe ganar sobre '=' y '=='
    ("X =.. Y", [(T.VARIABLE, "X"), (T.OP_RELACIONAL, "=.."), (T.VARIABLE, "Y")]),
    # '==' debe ganar sobre '='
    ("X == Y", [(T.VARIABLE, "X"), (T.OP_RELACIONAL, "=="), (T.VARIABLE, "Y")]),
    # '\\==' debe ganar sobre '\\='
    ("X \\== Y", [(T.VARIABLE, "X"), (T.OP_RELACIONAL, "\\=="), (T.VARIABLE, "Y")]),
    # '=<' debe ganar sobre '='
    ("X =< Y", [(T.VARIABLE, "X"), (T.OP_RELACIONAL, "=<"), (T.VARIABLE, "Y")]),
    # '>=' debe ganar sobre '>'
    ("X >= Y", [(T.VARIABLE, "X"), (T.OP_RELACIONAL, ">="), (T.VARIABLE, "Y")]),
    # '-->' debe ganar sobre '-'
    ("X --> Y", [(T.VARIABLE, "X"), (T.OP_CLAUSULA, "-->"), (T.VARIABLE, "Y")]),
    # ':-' se reconoce como un solo operador, no como ':' + '-'
    ("cabeza :- cuerpo", [
        (T.ATOMO, "cabeza"), (T.OP_CLAUSULA, ":-"), (T.ATOMO, "cuerpo"),
    ]),
    # El signo NO forma parte del lexema del número: son dos tokens.
    ("-3", [(T.OP_ARITMETICO, "-"), (T.ENTERO, "3")]),
    ("+3.5", [(T.OP_ARITMETICO, "+"), (T.REAL, "3.5")]),
    # Átomo vs. variable según la letra inicial (minúscula/mayúscula).
    ("padre_de_X", [(T.ATOMO, "padre_de_X")]),
    ("Padre_de_x", [(T.VARIABLE, "Padre_de_x")]),
    # Variable anónima distinta de una variable nombrada que empieza con '_'.
    ("_ _Temp", [(T.VARIABLE, "_"), (T.VARIABLE, "_Temp")]),
    # Número real vs. punto final de cláusula.
    ("3.14.", [(T.REAL, "3.14"), (T.PUNTO, ".")]),
    ("3.", [(T.ENTERO, "3"), (T.PUNTO, ".")]),
    # El comentario de línea no interfiere con los tokens vecinos.
    ("uno % comentario\ndos", [(T.ATOMO, "uno"), (T.ATOMO, "dos")]),
    # '//' (división entera) no se confunde con dos '/' consecutivos.
    ("A // B", [(T.VARIABLE, "A"), (T.OP_ARITMETICO, "//"), (T.VARIABLE, "B")]),
    # '**' (potencia) no se confunde con dos '*' consecutivos.
    ("A ** B", [(T.VARIABLE, "A"), (T.OP_ARITMETICO, "**"), (T.VARIABLE, "B")]),
]


@pytest.mark.parametrize("fuente, esperado", CASOS_PRIORIDAD)
def test_prioridad_maxima_coincidencia(fuente, esperado):
    tokens, errores, _ = tokenizar(fuente)
    assert errores == []
    assert tokens == esperado
