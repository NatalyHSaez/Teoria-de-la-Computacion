"""
Pruebas inválidas: caracteres no admitidos, átomos/cadenas sin cierre,
comentarios sin cierre y números mal formados (sección 6 del enunciado,
mínimo 8 casos).
"""

import pytest

from conftest import tokenizar, T


CASOS_INVALIDOS = [
    ("dato(@raro).", "carácter no admitido"),
    ("dato(^raro).", "carácter no admitido"),
    ("dato(~raro).", "carácter no admitido"),
    ("dato(`raro).", "carácter no admitido"),
    ("atomo_roto('sin cierre).", "átomo entre comillas simples sin cierre"),
    ('cadena_rota("sin cierre).', "cadena sin cierre"),
    ("numero_malo(1.2.3).", "número mal formado (demasiados puntos decimales)"),
    ("numero_malo2(1e+).", "número mal formado (exponente sin dígitos)"),
    ("/* comentario\nsin cierre", "comentario de bloque sin cierre"),
]


@pytest.mark.parametrize("fuente, mensaje_esperado", CASOS_INVALIDOS)
def test_error_lexico_detectado(fuente, mensaje_esperado):
    _, errores, _ = tokenizar(fuente)
    assert len(errores) >= 1
    assert any(mensaje_esperado in e.mensaje for e in errores)


def test_cuenta_minima_de_casos_invalidos():
    assert len(CASOS_INVALIDOS) >= 8


def test_recuperacion_continua_despues_de_un_error():
    fuente = "bueno1. dato(@raro). bueno2."
    tokens, errores, _ = tokenizar(fuente)
    assert len(errores) == 1
    assert (T.ATOMO, "bueno1") in tokens
    assert (T.ATOMO, "bueno2") in tokens


def test_ubicacion_del_error_incluye_linea_y_columna():
    fuente = "uno.\ndato(@raro)."
    _, errores, _ = tokenizar(fuente)
    assert len(errores) == 1
    assert errores[0].linea == 2
    assert errores[0].fragmento == "@"
