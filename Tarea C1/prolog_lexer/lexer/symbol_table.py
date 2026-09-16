"""
Tabla de lexemas (tabla de símbolos) del analizador.
"""


class TablaDeSimbolos:
    """
    Registra, sin duplicados innecesarios, los átomos, variables y
    literales (enteros, reales y cadenas) encontrados durante el análisis
    léxico.

    No resuelve ámbitos, unificación ni ningún otro análisis semántico:
    su única función es evitar registrar dos veces el mismo lexema dentro
    de la misma categoría y entregar un índice estable que el token puede
    referenciar como atributo.
    """

    CATEGORIAS = ("atomo", "variable", "entero", "real", "cadena")

    def __init__(self):
        self._indices = {c: {} for c in self.CATEGORIAS}
        self._entradas = []  # lista de (categoria, valor) en orden de inserción

    def registrar(self, categoria, valor):
        if categoria not in self._indices:
            raise ValueError(f"Categoría desconocida: {categoria!r}")
        indices_categoria = self._indices[categoria]
        if valor in indices_categoria:
            return indices_categoria[valor]
        indice = len(self._entradas)
        self._entradas.append((categoria, valor))
        indices_categoria[valor] = indice
        return indice

    def obtener(self, indice):
        return self._entradas[indice]

    def __len__(self):
        return len(self._entradas)

    def __iter__(self):
        return iter(self._entradas)

    def como_lista(self):
        """Devuelve la tabla como una lista de diccionarios, útil para imprimir."""
        return [
            {"indice": i, "categoria": categoria, "valor": valor}
            for i, (categoria, valor) in enumerate(self._entradas)
        ]

    def por_categoria(self, categoria):
        return [valor for (cat, valor) in self._entradas if cat == categoria]
