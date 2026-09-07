# Resultados

Estado: 8 de 20 resueltos. Actualizado durante el trabajo.

## Resueltos — César, desplazamiento 3

Método idéntico en los 8: sustitución monoalfabética por desplazamiento fijo
de 3 posiciones (César). Se rompe por fuerza bruta de los 26 desplazamientos.

El enunciado tiene erratas de tipeo. Se transcribe primero el descifrado
**literal** y, cuando hace falta, la lectura corregida entre corchetes.

| # | Frase descifrada | Tema |
|---|---|---|
| 4 | Dos llaves, una para cifrar y otra para abrir; la matemática las hace seguras. | Criptografía asimétrica / PKI |
| 14 | Barrera digital que filtra el tra`ã`ico [tráfico]; decide quién pasa y quién se queda afuera. | Firewall |
| 15 | `Iy leh` como `alida` [¿La nube como salida?], pero con riesgos; configuraciones y controles compartidos. | Seguridad en la nube / responsabilidad compartida |
| 16 | Escribir código pensando en el ataque; pruebas y `revs iones` [revisiones] antes de `lan zar`. | Desarrollo seguro / DevSecOps |
| 17 | Nuevas generaciones de Wi‑Fi; más velocidad, más seguridad, más regulación. | Seguridad Wi‑Fi (WPA3, Wi‑Fi 6/7) |
| 18 | Las 10 `vulnerablidades` [vulnerabilidades] más peligrosas en la web; OWASP las enumera. | OWASP Top 10 |
| 19 | `Cadá` [Cada] objeto conectado es una puerta; desde el hogar hasta la `industia` [industria]. | Seguridad en IoT |
| 20 | `Tecnologã` [Tecnología] operativa, sistemas que controlan el mundo `fisico` [físico]; SCADA y `PLZ` [PLC]. | Seguridad OT / ICS |

El acertijo 15 es el más dañado: `Lb ohk` no descifra a español legible con
ningún desplazamiento. La lectura propuesta se apoya en el resto de la frase,
que sí es inequívoca. Conviene confirmarlo con la cátedra antes de usarlo.

## Pendientes

1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13.

Todo ataque se corrió junto a un **control**: los acertijos 4 y 18, de
plaintext ya conocido, mezclados entre los pendientes. Si el ataque no
resuelve el control, su silencio sobre los pendientes no prueba nada.

Descartados, con el control resuelto en la misma corrida:

| Hipótesis | Cómo se probó | Control | Pendientes |
|---|---|---|---|
| César | 26 desplazamientos | 165.8 ✓ | — |
| Afín | 312 claves | ✓ | — |
| Vigenère, clave 1–4 | fuerza bruta exhaustiva | ✓ | basura |
| Vigenère, clave 5–10 | escalada con puntaje de palabras | 165.8 ✓ | 44–80 |
| Vigenère con reinicio por palabra | fuerza bruta 1–4 | 158.4 ✓ | 36–62 |
| Beaufort y Beaufort variante | fuerza bruta 1–3 | 158.4 ✓ | 36–62 |
| Autokey | fuerza bruta, primer 1–3 | ✓ | basura |
| Alfabeto con palabra clave | 50 000 claves × 26 rotaciones × 2 sentidos | 165.8 ✓ | 38–72 |
| Transposición | chi² del texto en crudo | — | 90–160, no es español |
| Clave compartida entre acertijos | IC combinado y por columnas | — | 0.044, plano |

**Sustitución arbitraria: no descartada, y es la hipótesis viva.** El límite
acá no es la hipótesis sino el largo del texto. Los acertijos tienen de 37 a
66 letras y todos los ataques estadísticos necesitan más:

- El solver por patrones, validado contra texto conocido, devuelve soluciones falsas mejor puntuadas que la verdadera.
- El modelo de cuadrigramas también se equivoca: sobre el acertijo 18 puntúa el texto verdadero peor que uno falso (−17.90 contra −17.47).
- El recocido con juez combinado resuelve el control 4 (67.9) pero **no** el control 18 (−7.7), que es César y se sabe la respuesta.

Un test de forma lo confirma: la distancia del perfil de frecuencias al
español da 26.5 y 28.3 para los controles 4 y 18, y 15.1 a 21.1 para varios
pendientes. Los pendientes se parecen al español **más** que los César ya
resueltos. A este largo la estadística no separa nada.

Ronda final de ataques, todos con el control 18 resuelto al lado:

| Hipótesis | Control 18 | Pendientes |
|---|---|---|
| Vigenère con clave de palabra real (50 000 palabras) | 59.0 ✓ | 34–61 |
| Desplazamiento distinto por palabra (k, k+p, k+2p…) | 91.8 ✓ | 24–63 |
| Desplazamiento según el largo de cada palabra | 52.2 | 13–43 |
| César progresivo por letra | ✓ | basura |
| Texto en inglés bajo César | — | sin coincidencias |

Y el generador de candidatos, leído a mano: sobre el control 18 la respuesta
correcta sale en el puesto 10 con −10.3, perfectamente legible
(`las 10 vulnerabl… en la web; … las enumera`). Sobre los pendientes el mejor
candidato de los 25 llega a −22.7 (acertijo 9), −32.6 (2) y −62.0 (1). No hay
nada legible. Con el mismo generador y el mismo juez, el control se resuelve y
los pendientes no.

## Conclusión

Los 12 pendientes no son sustitución monoalfabética, ni ninguna de las
variantes clásicas probadas. Un chequeo a mano en el acertijo 10 lo confirma:
`pwnqj` es prefijo de `pwnqjwgn`, y ninguna asignación consistente con
`fwnsqwwn` da tres palabras españolas a la vez.

La hipótesis de archivo corrupto quedó descartada: el texto es el original de
la cátedra. Las erratas (`traãico`, `Cadá`, `PLZ`, `Tecnologã`, `revs iones`)
vienen así de origen y no impidieron descifrar esos ocho.

Ronda de cierre, tapando huecos de mis propias herramientas:

| Hipótesis | Control 18 | Pendientes |
|---|---|---|
| Vigenère avanzando la clave en **todos** los caracteres, no solo letras | 91.8 ✓ | 36–66 |
| Alfabeto con palabra clave, claves de hasta 22 letras y términos del dominio | 96.5 ✓ | 38–46 |
| César sobre alfabeto de 27 letras (con ñ) | 67.9 ✓ | 22–47 |
| César sobre alfabeto de 32 (vocales acentuadas incluidas) | 71.0 ✓ | 27–54 |

Criptoanálisis manual del acertijo 11, el más corto (37 letras, 9 palabras):
`mjyuy` tiene patrón 0‑1‑2‑3‑2, que en español da `tiene, puede, viene, siete,
muere, duele, cosas, casos, playa, ojalá, quede, nueve, mirar, abrir`. Se
probó cada una propagando el mapeo a `jr`, `kq`, `jxwq` y `kytr`, que comparten
letras con ella. Ninguna cierra sin romper la biyección o exigir una palabra
inexistente. Coincide con lo que dice el ataque automático.

## Conclusión

Con 14 familias de cifra descartadas, cada una verificada contra un control de
respuesta conocida en la misma corrida, el criptoanálisis clásico no rompe
estos 12. La respuesta honesta es que falta información sobre el método, no
más cómputo.

Los 8 resueltos alcanzan de sobra para el objetivo real de la consigna:
elegir 1 tema principal y 2 secundarios.
