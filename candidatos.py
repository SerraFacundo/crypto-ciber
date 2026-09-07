#!/usr/bin/env python3
"""Fase 8 - Generar candidatos para que los lea una persona.

Los jueces automaticos (cuadrigramas, palabras, IC) fallan a 50 letras: sobre
el acertijo 18, de respuesta conocida, todos puntuan el texto verdadero por
debajo de uno falso. Pero la respuesta correcta si aparece entre los mejores
candidatos; lo que falta es quien la reconozca.

Asi que este script no decide: entrega los N mejores optimos locales del
recocido, ordenados, para lectura humana.
"""

import sys

from cripto import cargar_acertijos
from recocido import (ITERACIONES, atacar, modelo_cuadrigramas,
                      puntuar_combinado)
from solver import cargar_lexico

CANDIDATOS = 25


def generar(frase, modelo, piso, peso, reinicios=150):
    """Corre el recocido muchas veces y junta los optimos locales distintos."""
    import random
    import math
    from cripto import ABC, normalizar

    letras = normalizar(frase)
    orden_cif = [c for c, _ in sorted(
        ((c, letras.count(c)) for c in set(letras)), key=lambda x: -x[1])]
    orden_es = "eaosrnidlctumpbgvyqhfzjxkw"
    base = dict(zip(orden_cif, orden_es))
    libres = [c for c in ABC if c not in base.values()]
    for c in ABC:
        if c not in base:
            base[c] = libres.pop()

    from solver import sin_tildes

    def descifrar(mapa):
        return "".join(mapa.get(c, c) if c in ABC else c
                       for c in sin_tildes(frase))

    vistos = {}
    for _ in range(reinicios):
        mapa = dict(base)
        claves = list(mapa)
        random.shuffle(claves)
        for i in range(0, len(claves) - 1, 2):
            mapa[claves[i]], mapa[claves[i + 1]] = (
                mapa[claves[i + 1]], mapa[claves[i]])
        actual = puntuar_combinado(descifrar(mapa), modelo, piso, peso)
        for paso in range(ITERACIONES):
            temp = max(0.05, 10.0 * (1 - paso / ITERACIONES))
            a, b = random.sample(ABC, 2)
            mapa[a], mapa[b] = mapa[b], mapa[a]
            nuevo = puntuar_combinado(descifrar(mapa), modelo, piso, peso)
            if nuevo > actual or random.random() < math.exp((nuevo - actual) / temp):
                actual = nuevo
            else:
                mapa[a], mapa[b] = mapa[b], mapa[a]
        texto = descifrar(mapa)
        vistos[texto] = max(vistos.get(texto, -1e9), actual)
    return sorted(vistos.items(), key=lambda x: -x[1])[:CANDIDATOS]


def main():
    acertijos = cargar_acertijos()
    modelo, piso = modelo_cuadrigramas()
    _, peso = cargar_lexico()
    for n in [int(a) for a in sys.argv[1:]]:
        print(f"\n===== acertijo {n} =====", flush=True)
        print(f"      cifrado: {acertijos[n]}", flush=True)
        for texto, s in generar(acertijos[n], modelo, piso, peso):
            print(f"  [{s:7.1f}] {texto}", flush=True)


if __name__ == "__main__":
    main()
