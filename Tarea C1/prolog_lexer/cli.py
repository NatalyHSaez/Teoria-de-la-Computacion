#!/usr/bin/env python3
"""
CLI del analizador léxico de Prolog.

Uso:
    python cli.py archivo.pl
    python cli.py archivo.pl --tabla
    python cli.py archivo.pl --solo-errores
"""

import argparse
import sys

from lexer.lexer import AnalizadorLexico
from lexer.token_types import TipoToken


def analizar_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        fuente = f.read()
    analizador = AnalizadorLexico(fuente)
    return analizador.analizar()


def main():
    parser = argparse.ArgumentParser(
        description="Analizador léxico de un subconjunto de Prolog."
    )
    parser.add_argument("archivo", help="Archivo fuente Prolog (.pl) a analizar")
    parser.add_argument("--tabla", action="store_true", help="Imprimir la tabla de lexemas")
    parser.add_argument("--solo-errores", action="store_true", help="Imprimir solo los errores léxicos")
    args = parser.parse_args()

    tokens, errores, tabla = analizar_archivo(args.archivo)

    if not args.solo_errores:
        print("=== TOKENS ===")
        for tok in tokens:
            if tok.tipo is TipoToken.EOF:
                continue
            print(tok)

        if args.tabla:
            print("\n=== TABLA DE LEXEMAS ===")
            for entrada in tabla.como_lista():
                print(f"[{entrada['indice']}] {entrada['categoria']}: {entrada['valor']!r}")

    print(f"\n=== ERRORES LÉXICOS ({len(errores)}) ===")
    for err in errores:
        print(err)

    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
