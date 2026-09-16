from src.tokens import TokenType


def test_mayor_coincidencia_operador_barra(analizar):
    tokens, _ = analizar("p(\\==, \\=).")
    ops = [t.lexema for t in tokens if t.tipo == TokenType.OPERADOR]
    assert ops == ["\\==", "\\="]


def test_mayor_coincidencia_igual(analizar):
    tokens, _ = analizar("p(=.., ==, =).")
    ops = [t.lexema for t in tokens if t.tipo == TokenType.OPERADOR]
    assert ops == ["=..", "==", "="]


def test_mayor_coincidencia_dos_puntos(analizar):
    tokens, _ = analizar("p(:-).")
    ops = [t.lexema for t in tokens if t.tipo == TokenType.OPERADOR]
    assert ops == [":-"]


def test_mayor_coincidencia_aritmetica(analizar):
    tokens, _ = analizar("p(//, **).")
    ops = [t.lexema for t in tokens if t.tipo == TokenType.OPERADOR]
    assert ops == ["//", "**"]


def test_variable_anonima_vs_normal(analizar):
    tokens, _ = analizar("v(_, _X, _Temporal).")
    assert tokens[2].tipo == TokenType.VARIABLE_ANON
    assert (tokens[4].tipo, tokens[4].lexema) == (TokenType.VARIABLE, "_X")
    assert (tokens[6].tipo, tokens[6].lexema) == (TokenType.VARIABLE, "_Temporal")


def test_signo_segun_contexto(analizar):
    tokens, _ = analizar("neg(-3) :- resta(X is -3).")
    assert (tokens[2].tipo, tokens[2].lexema) == (TokenType.NUMERO, "-3")
    idx = [t.lexema for t in tokens].index("is")
    assert (tokens[idx + 1].tipo, tokens[idx + 1].lexema) == (TokenType.OPERADOR, "-")
    assert (tokens[idx + 2].tipo, tokens[idx + 2].lexema) == (TokenType.NUMERO, "3")