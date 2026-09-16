import argparse
import sys
from pathlib import Path
from .lexer import Lexer
from .symbol_table import TablaLexemas  
from .tokens import TokenType

def main():
    parser = argparse.ArgumentParser(description="Analizador Lexico de Prolog(subconjunto)")
    parser.add_argument("archivo", help="Ruta del archivo .pl")
    parser.add_argument("--tabla", action="store_true", help="imprimir la tabla de lexemas")
    args = parser.parse_args()

    texto = Path(args.archivo).read_text(encoding="utf-8-sig")
    tabla = TablaLexemas()
    lexer = Lexer(texto, tabla)
    tokens, errores = lexer.analizar()

    for tok in tokens:
        if tok.tipo != TokenType.EOF:
            print(tok)
    for err in errores:
        print(f"Error linea {err.linea}, columna {err.columna}: {err.mensaje}" 
              f"| fragmento: {err.fragmento!r} | recuperacion: {err.recuperacion}", file=sys.stderr)
    if args.tabla:
        print("\n=== Tabla de Lexemas ===")
        for lex, info in sorted(tabla.items(), key=lambda x: x[1]["indice"]):
            print(f"{info['indice']:3d}: {lex!r:20s} x{info['veces']}")

if __name__ == "__main__":
    main()