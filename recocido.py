#!/usr/bin/env python3
"""Fase 7 - Sustitucion arbitraria por recocido simulado con cuadrigramas.

El solver por patrones falla con 50 letras porque su juez es debil: premia
cualquier cadena de palabras que existan. Un modelo de cuadrigramas juzga el
texto entero, letra por letra, y castiga las combinaciones que el espanol no
produce. Es el ataque estandar contra sustitucion arbitraria.

El modelo se arma con la lista de frecuencias: cada palabra aporta sus
cuadrigramas pesados por lo usada que es, lo que aproxima texto corrido.
"""

import math
import random
import re
import sys
from collections import defaultdict

from cripto import ABC, cargar_acertijos, normalizar
from solver import cargar_lexico, sin_tildes

REINICIOS = 40
ITERACIONES = 6000


def modelo_cuadrigramas(ruta="frecuencias.txt"):
    """log P(cuadrigrama) estimado desde la lista de frecuencias."""
    conteo = defaultdict(float)
    total = 0.0
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            partes = linea.split()
            if len(partes) != 2:
                continue
            w = sin_tildes(partes[0])
            if not (w.isascii() and w.isalpha()):
                continue
            # Los espacios delimitan: el modelo aprende inicios y finales.
            w = f" {w} "
            n = int(partes[1])
            for i in range(len(w) - 3):
                conteo[w[i:i + 4]] += n
                total += n
    piso = math.log(0.01 / total)
    return {g: math.log(c / total) for g, c in conteo.items()}, piso


def puntuar(texto, modelo, piso):
    t = " " + " ".join(re.findall(r"[a-z]+", sin_tildes(texto))) + " "
    return sum(modelo.get(t[i:i + 4], piso) for i in range(len(t) - 3))


def puntuar_combinado(texto, modelo, piso, peso):
    """Cuadrigramas para guiar la escalada, palabras reales para decidir.

    Los cuadrigramas solos se equivocan: medidos contra el acertijo 18, el
    texto verdadero puntua PEOR que uno falso (-17.90 contra -17.47). Las
    palabras solas tampoco alcanzan. Juntos si separan (2.3 contra -35.5).
    """
    n = max(len(normalizar(texto)), 1)
    palabras = sum(peso.get(w, 0.0)
                   for w in re.findall(r"[a-z]+", sin_tildes(texto)))
    return palabras + 5.0 * puntuar(texto, modelo, piso) / n


def atacar(frase, modelo, piso, peso):
    """Recocido: parte de un mapeo por frecuencia y va intercambiando pares."""
    letras = normalizar(frase)
    orden_cif = [c for c, _ in sorted(
        ((c, letras.count(c)) for c in set(letras)), key=lambda x: -x[1])]
    orden_es = "eaosrnidlctumpbgvyqhfzjxkw"
    base = dict(zip(orden_cif, orden_es))
    for c in ABC:
        base.setdefault(c, "?")
    libres = [c for c in ABC if c not in base.values()]
    for c in base:
        if base[c] == "?":
            base[c] = libres.pop()

    def descifrar(mapa):
        return "".join(mapa.get(c, c) if c in ABC else c
                       for c in sin_tildes(frase))

    mejor_global = (-1e9, None)
    for _ in range(REINICIOS):
        mapa = dict(base)
        claves = list(mapa)
        random.shuffle(claves)
        for i in range(0, len(claves) - 1, 2):
            mapa[claves[i]], mapa[claves[i + 1]] = mapa[claves[i + 1]], mapa[claves[i]]
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
        if actual > mejor_global[0]:
            mejor_global = (actual, dict(mapa))
    return mejor_global[0], descifrar(mejor_global[1])


def main():
    acertijos = cargar_acertijos()
    modelo, piso = modelo_cuadrigramas()
    _, peso = cargar_lexico()
    objetivo = [int(a) for a in sys.argv[1:]] or sorted(acertijos)
    for n in objetivo:
        s, texto = atacar(acertijos[n], modelo, piso, peso)
        print(f"{n:>2} [{s:7.1f}] {texto}", flush=True)


if __name__ == "__main__":
    main()
