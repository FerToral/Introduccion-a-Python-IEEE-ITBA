# Procedencia de los cuadernos

Los cuadernos corresponden al curso **Introducción a la Programación con Python de IEEE-ITBA, 2C2021**. El material base es de IEEESBITBA; las copias de estudio incluyen respuestas de Fernando Toralez. Se mantiene la licencia CC BY-NC-SA 4.0 que declara el curso.

| Clase | Evidencia de la edición | Fuente base |
|---|---|---|
| 1 | Copia personal de agosto de 2021; enlace a los desafíos 2C2021 | [Clase 1 original](https://github.com/IEEESBITBA/Curso-python/tree/master/Curso_Introductorio_Clases) |
| 2 | Copia de agosto de 2021; procedencia Colab apunta al repositorio institucional | [Clases originales](https://github.com/IEEESBITBA/Curso-python/tree/master/Curso_Introductorio_Clases) |
| 3 | Dos copias de agosto de 2021, con diferencias en dos celdas de código | [Clases originales](https://github.com/IEEESBITBA/Curso-python/tree/master/Curso_Introductorio_Clases) |

Se conserva la teoría Markdown, las consignas, los anexos y los recursos enlazados. Las salidas guardadas y los contadores de ejecución se quitaron para abrir cada clase desde un estado limpio. Los originales y las variantes completas continúan en el respaldo privado.

## Adaptaciones de las respuestas

| Clase | Actividad | Cambio |
|---|---|---|
| 1 | Secuencia A–B | Permitir A=B, solicitar nuevamente B si es menor que A y mostrar ambos extremos |
| 1 | Secuencia con while | Inicializar los contadores y cumplir la secuencia 1,2,3,4,5,4,3,2,1,0 |
| 1 | Etiquetas | Leer el código como texto para mantener ceros iniciales |
| 1 | Divisores | Usar el parámetro de la función y devolver la cantidad de divisores |
| 1 | Dr. Lothar | Respuesta histórica `cantPasos` recuperada de Cuaderno de pruebas (celda 27); se reubica junto a la consigna, usa división entera y valida el dominio positivo |
| 1 | Promedios | Conservar promedio simple y ponderado; aplicar 30% a la tercera nota y mostrar los tres ejemplos pedidos |
| 2 | Temperaturas | Usar decimal `273.15`, obtener un número en Kelvin y verificar el cero absoluto con ese límite |
| 2 | Nombre en tarjeta | Abreviar sólo el nombre; limitar el apellido a 24 caracteres cuando sea necesario |
| 2 | Lista de pares | Conservar tres métodos que generan los mismos enteros de 0 a 48 |
| 2 | Intercambio de letras | Validar cada índice contra ambos extremos y mostrar un error en entradas inválidas |
| 2 | Archivos | Usar UTF-8, admitir BOM en mediciones y cerrar los archivos con `with` |
| 2 | Noticia | Propuesta nueva de conteo de palabras completas, sin distinguir mayúsculas y conservando acentos |
| 2 | Señal | Completar la lectura histórica con mínimos, máximos y promedios por columna; aproximar cruces ascendentes y periodos sin inventar precisión |
| 2 | Lotes | Propuesta nueva de estadística sin bibliotecas: media, varianza poblacional, moda y mediana; probar datos vacíos, pares, impares y empates |
| 3 | Ejemplo CSV | Leer con UTF-8 y cerrar el archivo al terminar |
| 3 | Conjuntos y elecciones | Reubicar el intento de votos en su desafío, contar por candidato e imprimir el ganador; la consigna supone que no hay empate |

La copia de Clase 3 con mayor desarrollo del intento de votos es la base elegida. La otra copia también contenía una exploración distinta de subconjuntos: se conserva como ejemplo adicional junto a esa sección. Las dos versiones históricas completas se mantienen en el respaldo; no se decidió únicamente por fecha ni por nombre.

Las comprobaciones se apoyan en las consignas internas y en pruebas propias. No se incorporaron solucionarios externos ni se reemplazó el trabajo por respuestas de otra cursada. La corrección de celdas concretas no certifica todos los ejercicios restantes.

La respuesta de Collatz estaba en la celda 27 de otro cuaderno personal, no debajo de su consigna en Clase 1. Se recuperó `cantPasos`; la división `/=` se sustituyó por división entera y se añadió rechazo de valores no positivos. Se conserva el nombre histórico y no se impone el máximo de 1000 que tenía su interfaz antigua, porque la consigna de la clase no lo establece. Las variantes de Ahorcado y Elecciones de ese cuaderno se relacionan por ejercicio: la clase conserva la versión posterior más adecuada, sin copiar sus mensajes de depuración ni errores de entrada. Esto no demuestra que todo el cuaderno exploratorio pertenezca a una única cursada.

Los cuatro auxiliares proceden de los enlaces institucionales incluidos en las clases. Fuentes y SHA-256 en [Datos de práctica](datos-de-practica.json). Los CSV son datos docentes, no evaluaciones privadas. La noticia de terceros se conserva en el respaldo privado y se recupera bajo demanda: no se redistribuye su texto en Git.

## Propuestas y contraste oficial — 17 de octubre de 2026

Se completan las 23 celdas vacías/comentadas, Ta-Te-Ti y el análisis NumPy/SciPy mediante propuestas nuevas asistidas, no soluciones históricas ni copias de compañeros. Las celdas lo indican. Se corrigen además la presentación, el caso cero del factorial docente y la preparación de auxiliares para Colab/Windows, sin sobrescribir datos ni depender de wget.

Se contrastaron las tres clases oficiales del commit `5d558a2228cbe7132129b8430950fd341a5f3d1e`: tienen 132/180/129 celdas frente a las copias personales de 124/171/122 antes de añadir preparación. Coinciden literalmente, normalizando espacios, 38/46/35 celdas Markdown de 67/89/63; la diferencia incluye material editado y no prueba un número de ejercicios faltantes. Se conserva la edición personal, sus tres desafíos y sus consignas, en vez de mezclar automáticamente versiones.

Las decisiones ante ambigüedades —primer ejemplo del código secreto, mínimo del adivinador, tildes del palíndromo y combinaciones de helados— están en el estado de ejercicios y en pruebas. No hay certificación de corrección oficial.
