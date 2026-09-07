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

Descartado hasta ahora, con evidencia:

- **César** (26 desplazamientos) y **afín** (312 claves): fuerza bruta completa, sin resultado.
- **Vigenère con clave de 1 a 4 letras**: fuerza bruta exhaustiva, sin resultado.
- **Vigenère con clave compartida entre acertijos**: el IC por columnas queda plano en 0.044 para todo largo de clave de 1 a 12.
- **Clave compartida entre acertijos**: el IC del texto combinado cae a 0.0442; cada acertijo tiene su propia clave.
- **Transposición**: las frecuencias de letras en crudo no son las del español (chi² de 90 a 160 en los pendientes, contra 10 a 26 en los resueltos).

Hipótesis viva: **sustitución con alfabeto derivado de una palabra clave**,
distinta por acertijo. Es lo habitual en un ejercicio de cátedra y reduce el
espacio de búsqueda de 26! a unas 50 000 claves, que sí se prueban todas.

Nota metodológica: el solver genérico de sustitución fue **descartado como
juez**. Validado contra texto conocido, con frases de ~50 letras devuelve
soluciones falsas con mejor puntaje que la verdadera. Un resultado suyo no
prueba nada sin verificación independiente.
