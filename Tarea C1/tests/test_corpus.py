def test_todos_los_validos_sin_errores(corpus_dir, analizar):
    archivos = sorted((corpus_dir / "validos").glob("*.pl"))
    assert len(archivos) >= 20, "El enunciado exige al menos 20 entradas válidas"
    for archivo in archivos:
        texto = archivo.read_text(encoding="utf-8")
        tokens, errores = analizar(texto)
        assert errores == [], f"{archivo.name}: {[e.mensaje for e in errores]}"
        assert tokens, f"{archivo.name} no produjo tokens"


def test_todos_los_invalidos_con_errores(corpus_dir, analizar):
    archivos = sorted((corpus_dir / "invalidos").glob("*.pl"))
    assert len(archivos) >= 8, "El enunciado exige al menos 8 entradas inválidas"
    for archivo in archivos:
        texto = archivo.read_text(encoding="utf-8")
        tokens, errores = analizar(texto)
        assert errores, f"{archivo.name} debia producir errores"


def test_programa_limpio(corpus_dir, analizar):
    texto = (corpus_dir / "programa_limpio.pl").read_text(encoding="utf-8")
    tokens, errores = analizar(texto)
    assert errores == []
    assert tokens


def test_programa_con_errores_recuperables(corpus_dir, analizar):
    texto = (corpus_dir / "programa_con_errores.pl").read_text(encoding="utf-8")
    tokens, errores = analizar(texto)
    assert len(errores) >= 3
    assert tokens
