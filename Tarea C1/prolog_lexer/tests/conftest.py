import os
import sys

# Permite ejecutar `pytest` desde la raíz del proyecto sin instalar el paquete.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lexer.lexer import AnalizadorLexico
from lexer.token_types import TipoToken as T  # noqa: F401  (re-exportado para los tests)


def tokenizar(fuente):
    """
    Ejecuta el analizador sobre `fuente` y devuelve una tupla:
        (lista_simplificada_de_tokens, errores, tabla)
    donde lista_simplificada_de_tokens es una lista de pares (tipo, lexema)
    SIN el token EOF final, para facilitar las comparaciones en los tests.
    """
    tokens, errores, tabla = AnalizadorLexico(fuente).analizar()
    simplificados = [(tok.tipo, tok.lexema) for tok in tokens if tok.tipo != T.EOF]
    return simplificados, errores, tabla
