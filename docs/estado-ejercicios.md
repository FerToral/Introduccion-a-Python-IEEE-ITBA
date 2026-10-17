# Alcance y ejercicios — IEEE-ITBA 2C2021

Cada respuesta queda junto a su consigna y teoría. Se mantienen las copias personales de 2021; la versión oficial actual se usa como referencia, no como sustituto de edición.

| Clase | Actividades con respuesta |
|---|---|
| 1 | Presentación, medias, horario modular, notas, ciclos, etiquetas, funciones, Collatz, promedios, e, primalidad, Fibonacci, adivinador, dominó, integración y pi |
| 2 | Temperaturas, tarjetas, listas, ordenamiento, archivos, Ahorcado y extras, derivada, palíndromos, paréntesis, frutas, señal, código secreto, estadística, conversión a entero y Ta-Te-Ti completo |
| 3 | Legajos, Morse, conjuntos, pangrama, CSV/JSON, Elecciones, alfabeto arcaico, estadística científica, candidatos/idiomas, frecuencias, helados, traducción, Truco y verificación JSON |

Se completaron las 23 celdas antes vacías/comentadas, el juego Ta-Te-Ti y el análisis con bibliotecas. Las propuestas de 2026 están identificadas; no se presentan como entregas históricas de Fernando. Los ejemplos didácticos no son sistemas de autenticación reales: no ingresar credenciales personales.

## Decisiones de las propuestas

- Adivinador: intervalo 0..9999 (la consigna no fija mínimo). «<» indica secreto menor que propuesta. Como máximo 14 respuestas válidas.
- Integral: rectángulos por izquierda y último tramo recortado. Admite orientación inversa; exige paso positivo.
- Derivadas: días desde 1, informando el día final del salto; None si no hubo subida/bajada.
- Palíndromo ampliado: se retiran también tildes para cumplir el ejemplo «búhos». La versión exacta no normaliza.
- Código secreto: cada aparición se cuenta una vez. Para 39541/19421 hay **2 correctos y 1 mal ubicado**, no 2: el primer ejemplo docente reutiliza el único 1 del secreto. El ejemplo 9955/9559 sí da 2 y 2.
- Helados: pares de formatos sin orden y con repetición del mismo formato; formatos distintos del mismo precio cuentan como opciones distintas.
- Pangrama: alfabeto inglés completo, incluida la v que omite la ayuda docente.
- Factorial del anexo: se corrige 0! = 1; se rechazan negativos.
- Estadística: varianza poblacional, menor moda en empates. Media cercana a varianza es compatible con Poisson, no una demostración. Señal: cruces discretos sin interpolar ni inventar precisión.

## Validación

Las pruebas leen las celdas reales. Cubren los 10000 secretos del adivinador, 1600 duelos entre 40 cartas, paréntesis hasta longitud 10, casos límite, 8192 mediciones y 30000 lotes; comparan estadística manual con biblioteca estándar y NumPy/SciPy.

Los notebooks pasan esquema Jupyter y sintaxis, sin salidas guardadas. Se ensayan bibliotecas y generación de un gráfico sin pantalla. La preparación de Colab se prueba en carpetas vacías con red simulada y comprobación de huellas; no sobrescribe archivos diferentes.

No se afirma aprobación docente ni ejecución de jueces HackerRank. No se certifica ejecución automática de todos los cuadernos de principio a fin: contienen entradas interactivas y exploraciones para estudiar por sección. Videos, imágenes y servicios externos dependen de sus proveedores. Los ejemplos históricos de e y Fibonacci conservan su alcance exploratorio.
