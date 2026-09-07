#!/usr/bin/env python3
"""Fase 4 - Solver de sustitucion monoalfabetica por patrones de palabra.

La estadistica pura no alcanza con ~50 letras. Lo que si alcanza es la forma
de las palabras: 'llaves' tiene patron 0-0-1-2-3-4 y pocas palabras del
espanol lo cumplen. Se prueban candidatas manteniendo un mapeo biyectivo
cifrado->claro y se retrocede ante cualquier contradiccion.

Contar cuantas palabras "existen" no alcanza como criterio: con 636k formas,
'buli' y 'aboyo' tambien existen. Cada candidata pesa por su frecuencia real
en espanol, asi 'de' vale mucho mas que 'buli'.

Tolera palabras sin candidata: el enunciado trae erratas ('Cadá', 'PLZ').
"""

import math
import sys
import unicodedata
from collections import defaultdict

from cripto import ABC, cargar_acertijos, normalizar

MAX_SALTOS = 3          # palabras que se permiten dejar sin resolver (erratas)
LIMITE_NODOS = 2_000_000  # corte de busqueda por acertijo
MAX_CANDIDATAS = 300    # ramas por palabra, las mas frecuentes primero
PESO_RARA = 1.0         # palabra valida pero fuera de las 50k mas usadas


def sin_tildes(texto):
    d = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in d if unicodedata.category(c) != "Mn")


def patron(palabra):
    """Forma canonica: 'llaves' -> (0,0,1,2,3,4). Invariante bajo sustitucion."""
    visto = {}
    return tuple(visto.setdefault(c, len(visto)) for c in palabra)


def cargar_lexico(dic="palabras.txt", frec="frecuencias.txt"):
    """Devuelve (candidatas_por_patron, peso). El peso es log(frecuencia)."""
    peso = {}
    with open(frec, encoding="utf-8") as f:
        for linea in f:
            partes = linea.split()
            if len(partes) == 2:
                w = sin_tildes(partes[0])
                if w.isascii() and w.isalpha():
                    peso[w] = max(peso.get(w, 0), math.log(int(partes[1])))

    por_patron = defaultdict(list)
    with open(dic, encoding="utf-8") as f:
        vocab = {sin_tildes(l.strip()) for l in f}
    vocab |= set(peso)
    for w in vocab:
        if w.isascii() and w.isalpha():
            por_patron[patron(w)].append(w)

    for lista in por_patron.values():
        lista.sort(key=lambda w: -peso.get(w, PESO_RARA))
    return por_patron, peso


def palabras_cifradas(frase):
    """Palabras del criptograma, normalizadas y sin repetir."""
    crudas = [normalizar(p) for p in frase.split()]
    return sorted({p for p in crudas if len(p) >= 1}, key=len, reverse=True)


def resolver(frase, por_patron, peso):
    """Backtracking que maximiza la suma de log-frecuencias, no el conteo."""
    palabras = palabras_cifradas(frase)
    candidatas = {
        p: por_patron.get(patron(p), [])[:MAX_CANDIDATAS] for p in palabras
    }
    # Menos candidatas primero: poda el arbol lo antes posible.
    palabras.sort(key=lambda p: (len(candidatas[p]), -len(p)))
    tope = max(peso.values())

    mejor = [(-1.0, {}, {})]
    nodos = [0]

    def buscar(i, mapa, inverso, score, elegidas, saltos):
        nodos[0] += 1
        if nodos[0] > LIMITE_NODOS:
            return
        if score > mejor[0][0]:
            mejor[0] = (score, dict(mapa), dict(elegidas))
        if i == len(palabras):
            return
        # Cota optimista: ni con la palabra mas frecuente en cada hueco alcanza.
        if score + (len(palabras) - i) * tope <= mejor[0][0]:
            return

        cif = palabras[i]
        for claro in candidatas[cif]:
            nuevo_m, nuevo_i, ok = {}, {}, True
            for a, b in zip(cif, claro):
                if mapa.get(a, b) != b or inverso.get(b, a) != a:
                    ok = False
                    break
                if a not in mapa:
                    nuevo_m[a], nuevo_i[b] = b, a
            if not ok:
                continue
            mapa.update(nuevo_m)
            inverso.update(nuevo_i)
            elegidas[cif] = claro
            buscar(i + 1, mapa, inverso, score + peso.get(claro, PESO_RARA),
                   elegidas, saltos)
            del elegidas[cif]
            for a in nuevo_m:
                del mapa[a]
            for b in nuevo_i:
                del inverso[b]

        if saltos < MAX_SALTOS:
            buscar(i + 1, mapa, inverso, score, elegidas, saltos + 1)

    buscar(0, {}, {}, 0.0, {}, 0)
    return mejor[0]


def aplicar(frase, mapa):
    """Descifra con el mapeo; lo no resuelto queda en MAYUSCULA para verlo."""
    salida = []
    for ch in frase:
        base = sin_tildes(ch)
        if base in ABC:
            salida.append(mapa.get(base, base.upper()))
        else:
            salida.append(ch)
    return "".join(salida)


def main():
    acertijos = cargar_acertijos()
    por_patron, peso = cargar_lexico()
    objetivo = [int(a) for a in sys.argv[1:]] or sorted(acertijos)
    for n in objetivo:
        score, mapa, _ = resolver(acertijos[n], por_patron, peso)
        print(f"{n:>2} [{score:6.1f}] {aplicar(acertijos[n], mapa)}", flush=True)


if __name__ == "__main__":
    main()
