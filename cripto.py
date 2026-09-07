#!/usr/bin/env python3
"""Criptoanalisis de los 20 acertijos de consigna.txt.

Fase 1: clasificar cada acertijo por Indice de Coincidencia (IC).
Fase 2: romper los monoalfabeticos (Cesar / afin).
Fase 3: romper los polialfabeticos (Vigenere).

Sin dependencias externas. Ejecutar: python3 cripto.py
"""

import re
import sys
import unicodedata
from collections import Counter
from itertools import product

ABC = "abcdefghijklmnopqrstuvwxyz"

# Frecuencias del espanol en %, con la ñ ya colapsada en n por la normalizacion.
FREQ_ES = {
    "a": 11.96, "b": 0.92, "c": 2.92, "d": 6.87, "e": 16.78, "f": 0.52,
    "g": 0.73, "h": 0.89, "i": 4.15, "j": 0.30, "k": 0.01, "l": 8.37,
    "m": 2.12, "n": 7.01, "o": 8.69, "p": 2.78, "q": 1.53, "r": 4.94,
    "s": 7.88, "t": 3.31, "u": 4.80, "v": 0.39, "w": 0.01, "x": 0.06,
    "y": 1.54, "z": 0.15,
}

# Palabras cortas frecuentes: confirman lo que el chi2 solo sugiere.
PALABRAS = {
    "de", "la", "que", "el", "en", "y", "a", "los", "las", "un", "una",
    "por", "con", "no", "es", "se", "del", "al", "lo", "su", "para",
    "mas", "como", "pero", "sin", "sobre", "todo", "cada", "hasta",
    "desde", "quien", "donde", "son", "esta", "hace", "antes",
}


def normalizar(texto):
    """Baja a minusculas, saca tildes/ñ y deja solo a-z.

    Los acentuados del cifrado no siguen el mismo desplazamiento que las
    letras normales: son ruido. Se normalizan a su letra base.
    """
    sin_tildes = unicodedata.normalize("NFD", texto.lower())
    sin_tildes = "".join(c for c in sin_tildes if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z]", "", sin_tildes)


def cargar_acertijos(ruta="consigna.txt"):
    """Extrae los acertijos numerados. consigna.txt es la unica fuente de verdad."""
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    pares = re.findall(r"^\s*(\d{1,2})\)\s*(.+)$", texto, re.MULTILINE)
    return {int(n): frase.strip() for n, frase in pares}


# --------------------------------------------------------------------------
# FASE 1 - Indice de Coincidencia
# --------------------------------------------------------------------------

def indice_coincidencia(texto):
    """Probabilidad de que dos letras al azar del texto sean iguales.

    Espanol claro ~0.077. Un cifrado monoalfabetico solo renombra letras,
    asi que conserva el IC. Uno polialfabetico aplana la distribucion
    hacia el azar puro (1/26 = 0.038).
    """
    letras = normalizar(texto)
    n = len(letras)
    if n < 2:
        return 0.0
    conteo = Counter(letras)
    return sum(c * (c - 1) for c in conteo.values()) / (n * (n - 1))


def clasificar(ic):
    if ic >= 0.060:
        return "monoalfabetico"
    if ic <= 0.050:
        return "polialfabetico"
    return "dudoso (texto corto)"


# --------------------------------------------------------------------------
# FASE 2 - Cesar y puntaje de "esto ya es espanol"
# --------------------------------------------------------------------------

def chi2(texto):
    """Distancia entre las frecuencias observadas y las del espanol.

    Mas bajo = mas parecido al espanol. Es el criterio que ordena candidatos
    cuando hay 26 (o miles de) claves posibles y nadie las va a leer a mano.
    """
    letras = normalizar(texto)
    n = len(letras)
    if n == 0:
        return float("inf")
    conteo = Counter(letras)
    total = 0.0
    for letra in ABC:
        esperado = FREQ_ES[letra] * n / 100
        total += (conteo[letra] - esperado) ** 2 / max(esperado, 0.01)
    return total / n


def palabras_validas(texto):
    """Cuenta palabras comunes del espanol. El chi2 falla en frases cortas."""
    limpio = unicodedata.normalize("NFD", texto.lower())
    limpio = "".join(c for c in limpio if unicodedata.category(c) != "Mn")
    tokens = re.findall(r"[a-z]+", limpio)
    return sum(1 for t in tokens if t in PALABRAS)


def puntaje(texto):
    """Menor es mejor. chi2 ordena, las palabras comunes confirman."""
    return chi2(texto) - 2.0 * palabras_validas(texto)


def desplazar(texto, k):
    """Cesar sobre a-z. Todo lo demas (tildes, puntuacion) pasa intacto."""
    salida = []
    for ch in texto:
        if "a" <= ch <= "z":
            salida.append(chr((ord(ch) - 97 - k) % 26 + 97))
        elif "A" <= ch <= "Z":
            salida.append(chr((ord(ch) - 65 - k) % 26 + 65))
        else:
            salida.append(ch)
    return "".join(salida)


def romper_cesar(texto):
    """Fuerza bruta de los 26 desplazamientos, ordenados por puntaje."""
    cands = [(puntaje(desplazar(texto, k)), k, desplazar(texto, k)) for k in range(26)]
    cands.sort()
    return cands[0]


def descifrar_afin(texto, a, b):
    """x -> a*x + b mod 26. Cesar es el caso a=1."""
    inv = pow(a, -1, 26)
    salida = []
    for ch in texto:
        if "a" <= ch <= "z":
            salida.append(chr(inv * (ord(ch) - 97 - b) % 26 + 97))
        elif "A" <= ch <= "Z":
            salida.append(chr(inv * (ord(ch) - 65 - b) % 26 + 65))
        else:
            salida.append(ch)
    return "".join(salida)


def romper_afin(texto):
    """26 desplazamientos x 12 multiplicadores coprimos con 26."""
    coprimos = [a for a in range(1, 26, 2) if a != 13]
    cands = []
    for a, b in product(coprimos, range(26)):
        claro = descifrar_afin(texto, a, b)
        cands.append((puntaje(claro), a, b, claro))
    cands.sort()
    return cands[0]


# --------------------------------------------------------------------------
# FASE 3 - Vigenere
# --------------------------------------------------------------------------

def ic_promedio_por_periodo(letras, m):
    """IC promedio al partir el texto en m columnas.

    Si m es el largo real de la clave, cada columna quedo cifrada con un
    unico Cesar: vuelve a comportarse como espanol y el IC sube a ~0.077.
    """
    ics = []
    for i in range(m):
        col = letras[i::m]
        n = len(col)
        if n < 2:
            continue
        conteo = Counter(col)
        ics.append(sum(c * (c - 1) for c in conteo.values()) / (n * (n - 1)))
    return sum(ics) / len(ics) if ics else 0.0


def estimar_largo_clave(texto, maximo=12):
    """Friedman: prueba cada largo y devuelve los mejores por IC de columna."""
    letras = normalizar(texto)
    puntajes = [(ic_promedio_por_periodo(letras, m), m) for m in range(1, maximo + 1)]
    puntajes.sort(reverse=True)
    return puntajes


def kasiski(texto, largo=3):
    """Distancias entre trigramas repetidos. Sus divisores delatan la clave."""
    letras = normalizar(texto)
    posiciones = {}
    for i in range(len(letras) - largo + 1):
        posiciones.setdefault(letras[i:i + largo], []).append(i)
    distancias = []
    for pos in posiciones.values():
        if len(pos) > 1:
            distancias += [b - a for a, b in zip(pos, pos[1:])]
    factores = Counter()
    for d in distancias:
        for f in range(2, 13):
            if d % f == 0:
                factores[f] += 1
    return factores.most_common(5)


def clave_vigenere(texto, m):
    """Resuelve un Cesar independiente por columna, cada uno por chi2."""
    letras = normalizar(texto)
    clave = ""
    for i in range(m):
        col = letras[i::m]
        mejor = min(range(26), key=lambda k: chi2(desplazar(col, k)))
        clave += ABC[mejor]
    return clave


def descifrar_vigenere(texto, clave):
    """Aplica la clave solo sobre a-z; el resto no consume posicion de clave."""
    salida = []
    j = 0
    for ch in texto:
        if ch.lower() in ABC:
            k = ord(clave[j % len(clave)]) - 97
            salida.append(desplazar(ch, k))
            j += 1
        else:
            salida.append(ch)
    return "".join(salida)


def romper_vigenere(texto, maximo=12):
    """Prueba los largos mas prometedores y devuelve el mejor descifrado."""
    cands = []
    for _, m in estimar_largo_clave(texto, maximo)[:6]:
        clave = clave_vigenere(texto, m)
        claro = descifrar_vigenere(texto, clave)
        cands.append((puntaje(claro), m, clave, claro))
    cands.sort()
    return cands[0]


# --------------------------------------------------------------------------

def main():
    acertijos = cargar_acertijos()
    if not acertijos:
        sys.exit("No se encontraron acertijos en consigna.txt")

    print("=" * 78)
    print("FASE 1 - Clasificacion por Indice de Coincidencia")
    print("=" * 78)
    print(f"{'#':>3} {'letras':>7} {'IC':>7}  familia")
    familias = {}
    for n, frase in sorted(acertijos.items()):
        ic = indice_coincidencia(frase)
        fam = clasificar(ic)
        familias[n] = fam
        print(f"{n:>3} {len(normalizar(frase)):>7} {ic:>7.4f}  {fam}")

    print()
    print("=" * 78)
    print("FASE 2 - Ataque monoalfabetico (Cesar, si falla afin)")
    print("=" * 78)
    pendientes = []
    for n, frase in sorted(acertijos.items()):
        sc, k, claro = romper_cesar(frase)
        if palabras_validas(claro) >= 2:
            print(f"{n:>3} Cesar k={k:<2} -> {claro}")
        else:
            sc_a, a, b, claro_a = romper_afin(frase)
            if palabras_validas(claro_a) >= 2:
                print(f"{n:>3} Afin a={a} b={b} -> {claro_a}")
            else:
                pendientes.append(n)

    print()
    print("=" * 78)
    print("FASE 3 - Ataque polialfabetico (Vigenere) sobre los pendientes")
    print("=" * 78)
    for n in pendientes:
        frase = acertijos[n]
        sc, m, clave, claro = romper_vigenere(frase)
        print(f"{n:>3} IC={indice_coincidencia(frase):.4f} "
              f"largos={[m for _, m in estimar_largo_clave(frase)[:3]]} "
              f"kasiski={kasiski(frase)}")
        print(f"    clave='{clave}' (m={m}) -> {claro}")


if __name__ == "__main__":
    main()
