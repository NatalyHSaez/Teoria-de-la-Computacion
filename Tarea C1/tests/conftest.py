import pytest
from pathlib import Path

from src.lexer import Lexer
from src.symbol_table import TablaLexemas
from src.tokens import TokenType

CORPUS_DIR = Path(__file__).resolve().parent.parent / "corpus"


@pytest.fixture
def analizar():
    def _analizar(texto, signed_numbers=True):
        tabla = TablaLexemas()
        lexer = Lexer(texto, tabla, signed_numbers=signed_numbers)
        tokens, errores = lexer.analizar()
        tokens = [t for t in tokens if t.tipo != TokenType.EOF]
        return tokens, errores

    return _analizar


@pytest.fixture
def corpus_dir():
    return CORPUS_DIR