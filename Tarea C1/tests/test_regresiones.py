"""Casos límite ausentes del corpus inicial, con resultados verificables."""
import subprocess
import sys
from pathlib import Path

import pytest

from src.lexer import Lexer
from src.symbol_table import TablaLexemas
from src.tokens import TokenType


@pytest.mark.parametrize("numero", ["3.14", "0.0", "12", "1e3", "1.2E-3"])
def test_numero_antes_del_punto_final(analizar, numero):
    tokens, errores = analizar(numero + ".")
    assert not errores
    assert [(t.tipo, t.lexema) for t in tokens] == [
        (TokenType.NUMERO, numero), (TokenType.PUNTO, ".")]


@pytest.mark.parametrize("fragmento", ["12abc", "1.2abc", "1.2.3.4", "12e", "1e+", "1.2E-", "12_abc"])
def test_numero_invalido_completo_y_recuperacion(analizar, fragmento):
    tokens, errores = analizar(fragmento + ", sigue.")
    assert len(errores) == 1
    assert errores[0].fragmento == fragmento
    assert (errores[0].linea, errores[0].columna) == (1, 1)
    assert [t.lexema for t in tokens] == [",", "sigue", "."]


@pytest.mark.parametrize("caracter", [":", "?", "\\"])
def test_prefijo_aislado_no_es_operador(analizar, caracter):
    tokens, errores = analizar(caracter + " sigue")
    assert len(errores) == 1
    assert errores[0].fragmento == caracter
    assert [t.lexema for t in tokens] == ["sigue"]


@pytest.mark.parametrize("literal", ["'don''t'", '"a""b"', "''", '""'])
def test_comilla_doblada_y_literal_vacio(analizar, literal):
    tokens, errores = analizar(literal)
    assert not errores
    assert len(tokens) == 1
    assert tokens[0].lexema == literal


@pytest.mark.parametrize("salto", ["\n", "\r\n", "\r"])
def test_posicion_tras_comentarios_y_saltos(analizar, salto):
    tokens, errores = analizar("% comentario" + salto + "/* a" + salto + "b */\tX")
    assert not errores
    assert [(t.lexema, t.linea, t.columna) for t in tokens] == [("X", 3, 6)]


def test_tabla_y_analisis_repetido_no_duplican():
    tabla = TablaLexemas()
    lexer = Lexer("padre(X,X). padre(X).", tabla)
    tokens, errores = lexer.analizar()
    assert not errores
    assert len(tabla) == 2
    assert dict(tabla.items())["X"]["veces"] == 3
    assert {t.indice_tabla for t in tokens if t.lexema == "X"} == {1}
    lexer.analizar()
    assert sum(t.tipo == TokenType.EOF for t in tokens) == 1
    assert dict(tabla.items())["X"]["veces"] == 3


@pytest.mark.parametrize("contenido,codigo", [("ok.", 0), ("@ sigue.", 1)])
def test_cli_codigos_y_diagnosticos(tmp_path, contenido, codigo):
    archivo = tmp_path / "entrada.pl"
    archivo.write_text(contenido, encoding="utf-8-sig")
    resultado = subprocess.run([sys.executable, "-m", "src.main", str(archivo), "--tabla"],
                              cwd=Path(__file__).resolve().parents[1], capture_output=True)
    assert resultado.returncode == codigo
    assert b"ATOMO" in resultado.stdout
    assert (b"fragmento:" in resultado.stderr) == bool(codigo)


def test_cli_archivo_inexistente(tmp_path):
    resultado = subprocess.run([sys.executable, "-m", "src.main", str(tmp_path / "falta.pl")],
                              cwd=Path(__file__).resolve().parents[1], capture_output=True)
    assert resultado.returncode == 2
    assert b"Traceback" not in resultado.stderr
