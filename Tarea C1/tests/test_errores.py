def test_atomo_sin_cierre(analizar):
    tokens, errores = analizar("roto('Juan.\ncontinua.")
    assert len(errores) == 1
    assert "cierre" in errores[0].mensaje.lower()
    assert errores[0].linea == 1
    assert any(t.lexema == "continua" for t in tokens)


def test_cadena_sin_cierre(analizar):
    tokens, errores = analizar('dato("hola.')
    assert len(errores) == 1
    assert "cierre" in errores[0].mensaje.lower()


def test_comentario_sin_cierre(analizar):
    tokens, errores = analizar("/* sin cerrar\nx(1).")
    assert len(errores) == 1
    assert "comentario" in errores[0].mensaje.lower()
    assert errores[0].linea == 1


def test_caracter_no_admitido(analizar):
    tokens, errores = analizar("raro(@).")
    assert len(errores) == 1
    assert "no admitido" in errores[0].mensaje.lower()
    assert (errores[0].linea, errores[0].columna) == (1, 6)


def test_numero_mal_formado_letras(analizar):
    tokens, errores = analizar("malo(12abc).")
    assert len(errores) == 1
    assert "mal formado" in errores[0].mensaje.lower()


def test_numero_mal_formado_puntos(analizar):
    tokens, errores = analizar("malo2(1.2.3).")
    assert len(errores) == 1
    assert "mal formado" in errores[0].mensaje.lower()