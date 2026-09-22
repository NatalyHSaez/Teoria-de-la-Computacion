import os

from lexer.lexer import AnalizadorLexico

RUTA_CORPUS = os.path.join(os.path.dirname(__file__), "..", "corpus")


def _leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


def test_archivos_validos_no_producen_errores():
    carpeta = os.path.join(RUTA_CORPUS, "validos")
    archivos = sorted(f for f in os.listdir(carpeta) if f.endswith(".pl"))
    assert len(archivos) >= 20, "El enunciado exige al menos 20 entradas validas"
    for nombre in archivos:
        fuente = _leer(os.path.join(carpeta, nombre))
        tokens, errores, _ = AnalizadorLexico(fuente).analizar()
        assert errores == [], f"{nombre}: {[e.mensaje for e in errores]}"
        assert len(tokens) > 1, f"{nombre} no produjo tokens"


def test_archivos_invalidos_producen_errores():
    carpeta = os.path.join(RUTA_CORPUS, "invalidos")
    archivos = sorted(f for f in os.listdir(carpeta) if f.endswith(".pl"))
    assert len(archivos) >= 8, "El enunciado exige al menos 8 entradas invalidas"
    for nombre in archivos:
        fuente = _leer(os.path.join(carpeta, nombre))
        _, errores, _ = AnalizadorLexico(fuente).analizar()
        assert errores, f"{nombre} debia producir errores"
