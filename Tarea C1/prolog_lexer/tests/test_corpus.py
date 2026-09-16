"""
Pruebas de integración sobre los dos archivos de entrada completos
solicitados en la sección 6 del enunciado: uno sin errores y otro con
múltiples errores léxicos recuperables.
"""

import os

from conftest import tokenizar, T
from lexer.lexer import AnalizadorLexico

RUTA_CORPUS = os.path.join(os.path.dirname(__file__), "..", "corpus")


def _leer(nombre):
    with open(os.path.join(RUTA_CORPUS, nombre), encoding="utf-8") as f:
        return f.read()


def test_programa_valido_no_produce_errores():
    fuente = _leer("programa_valido.pl")
    tokens, errores, tabla = AnalizadorLexico(fuente).analizar()

    assert errores == []
    assert len(tokens) > 50
    assert len(tabla) > 0

    tipos_presentes = {tok.tipo for tok in tokens}
    categorias_esperadas = {
        T.ATOMO, T.ATOMO_COMILLAS, T.VARIABLE, T.ENTERO, T.REAL, T.CADENA,
        T.OP_CLAUSULA, T.OP_RELACIONAL, T.OP_ARITMETICO, T.OP_CONTROL,
        T.COMA, T.PUNTO, T.PARENTESIS_IZQ, T.PARENTESIS_DER,
        T.CORCHETE_IZQ, T.CORCHETE_DER, T.LLAVE_IZQ, T.LLAVE_DER,
        T.BARRA_VERTICAL,
    }
    faltantes = categorias_esperadas - tipos_presentes
    assert not faltantes, f"Categorías no cubiertas por el corpus válido: {faltantes}"


def test_programa_con_errores_multiples_es_recuperable():
    fuente = _leer("programa_con_errores.pl")
    tokens, errores, _ = AnalizadorLexico(fuente).analizar()

    assert len(errores) >= 8

    atomos = [tok.lexema for tok in tokens if tok.tipo == T.ATOMO]
    # Los hechos válidos intercalados entre errores deben seguir apareciendo,
    # lo que demuestra que el análisis se recupera y continúa.
    assert "hecho_valido" in atomos
