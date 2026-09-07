#!/usr/bin/env python3
"""Fase 6 - Sustitucion con alfabeto de palabra clave, por fuerza bruta.

Buscar entre las 26! permutaciones posibles es inutil con 50 letras de texto:
aparecen soluciones falsas mejor puntuadas que la verdadera (comprobado).

Pero un ejercicio de catedra casi nunca usa una permutacion al azar: usa un
alfabeto derivado de una palabra clave. 'CLAVE' -> C,L,A,V,E + el resto del
abecedario. Eso reduce el espacio a ~50k claves, y 50k se prueban todas.
"""

import re
import sys

from cripto import ABC, cargar_acertijos
from solver import cargar_lexico, sin_tildes


def alfabeto_clave(palabra):
    """'clave' -> 'clavebdfghijkmnopqrstuwxyz' (sin repetir letras)."""
    visto = []
    for c in palabra + ABC:
        if c not in visto:
            visto.append(c)
    return "".join(visto)


def traducir(texto, origen, destino):
    tabla = str.maketrans(origen + origen.upper(), destino + destino.upper())
    return texto.translate(tabla)


def puntaje_palabras(texto, peso):
    return sum(peso.get(t, 0.0) for t in re.findall(r"[a-z]+", sin_tildes(texto)))


def atacar(frase, peso, claves):
    """Prueba cada clave en los dos sentidos y con los 26 desplazamientos."""
    mejor = (-1.0, "", "", "")
    for palabra in claves:
        alfa = alfabeto_clave(palabra)
        for desp in range(26):
            rot = alfa[desp:] + alfa[:desp]
            # Sentido A: el alfabeto clave es el del cifrado.
            cand = traducir(frase, rot, ABC)
            s = puntaje_palabras(cand, peso)
            if s > mejor[0]:
                mejor = (s, palabra, f"A+{desp}", cand)
            # Sentido B: el alfabeto clave es el del texto claro.
            cand = traducir(frase, ABC, rot)
            s = puntaje_palabras(cand, peso)
            if s > mejor[0]:
                mejor = (s, palabra, f"B+{desp}", cand)
    return mejor


def main():
    acertijos = cargar_acertijos()
    _, peso = cargar_lexico()
    claves = [w for w in sorted(peso, key=peso.get, reverse=True)[:50000]
              if 3 <= len(w) <= 12]
    objetivo = [int(a) for a in sys.argv[1:]] or sorted(acertijos)
    for n in objetivo:
        s, palabra, modo, texto = atacar(acertijos[n], peso, claves)
        print(f"{n:>2} clave={palabra:<12} {modo:<5} [{s:6.1f}] {texto}",
              flush=True)


if __name__ == "__main__":
    main()
