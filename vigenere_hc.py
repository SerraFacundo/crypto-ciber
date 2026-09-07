#!/usr/bin/env python3
"""Fase 5 - Vigenere por escalada de colina con puntaje de palabras reales.

El ataque clasico (chi2 por columna) necesita ~100 letras por columna. Estos
acertijos tienen 50 letras en total, asi que las columnas son ruido. En vez de
eso se optimiza la clave entera contra el texto completo: se prueba cada letra
en cada posicion y se queda la que mas palabras espanolas reales produce.
"""

import random
import re
import sys

from cripto import ABC, cargar_acertijos, descifrar_vigenere
from solver import cargar_lexico, sin_tildes

REINICIOS = 30


def puntaje_palabras(texto, peso):
    """Suma de log-frecuencias de los tokens que son palabras del espanol."""
    return sum(peso.get(t, 0.0) for t in re.findall(r"[a-z]+", sin_tildes(texto)))


def atacar(frase, peso, m):
    """Escalada: fija una posicion de clave por vez hasta que no mejora."""
    mejor = (-1.0, "")
    for _ in range(REINICIOS):
        clave = [random.choice(ABC) for _ in range(m)]
        actual = puntaje_palabras(descifrar_vigenere(frase, "".join(clave)), peso)
        mejoro = True
        while mejoro:
            mejoro = False
            for i in range(m):
                original = clave[i]
                for letra in ABC:
                    clave[i] = letra
                    s = puntaje_palabras(
                        descifrar_vigenere(frase, "".join(clave)), peso)
                    if s > actual:
                        actual, original, mejoro = s, letra, True
                clave[i] = original
        if actual > mejor[0]:
            mejor = (actual, "".join(clave))
    return mejor


def main():
    acertijos = cargar_acertijos()
    _, peso = cargar_lexico()
    objetivo = [int(a) for a in sys.argv[1:]] or sorted(acertijos)
    for n in objetivo:
        frase = acertijos[n]
        resultados = [(*atacar(frase, peso, m), m) for m in range(2, 11)]
        s, clave, m = max(resultados)
        print(f"{n:>2} m={m} clave={clave:<10} [{s:6.1f}] "
              f"{descifrar_vigenere(frase, clave)}", flush=True)


if __name__ == "__main__":
    main()
