# Introducción a Python — IEEE ITBA

Cuadernos de estudio de Fernando Toralez del curso introductorio IEEE-ITBA, **segundo cuatrimestre de 2021**. Teoría, ejemplos, consignas y respuestas permanecen juntos en cada clase.

| Clase | Temas | Estudiar |
|---|---|---|
| 1 | Variables, operadores, condiciones, ciclos y funciones | [Notebook](clases/clase-01/clase-01.ipynb) · [Abrir en Colab](https://colab.research.google.com/github/FerToral/Introduccion-a-Python-IEEE-ITBA/blob/main/clases/clase-01/clase-01.ipynb) |
| 2 | Strings, listas, archivos y ejercicios integradores | [Notebook](clases/clase-02/clase-02.ipynb) · [Abrir en Colab](https://colab.research.google.com/github/FerToral/Introduccion-a-Python-IEEE-ITBA/blob/main/clases/clase-02/clase-02.ipynb) |
| 3 | Diccionarios, conjuntos, bibliotecas, CSV y JSON | [Notebook](clases/clase-03/clase-03.ipynb) · [Abrir en Colab](https://colab.research.google.com/github/FerToral/Introduccion-a-Python-IEEE-ITBA/blob/main/clases/clase-03/clase-03.ipynb) |

Los desafíos de entrega de la edición son **La conjetura del Dr. Lothar**, **Ahorcado** y **Las Elecciones** ([HackerRank 2C2021](https://www.hackerrank.com/2021-2c-curso-introductorio-de-python)). Los integradores incluyen dominó, Riemann, pi, Ta-Te-Ti, código secreto, estadística, traducciones y Truco.

## Ejecutar

En Colab, abrir una clase y ejecutar sus secciones en orden. Las clases 2 y 3 preparan automáticamente los auxiliares que falten desde una versión fijada del repositorio institucional, verificando SHA-256. No sobrescriben un archivo local diferente. Las celdas interactivas solicitan entradas; no usar contraseñas ni datos de alumnos reales en los ejemplos.

Para JupyterLab se ensayó Python 3.12.14:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python herramientas/preparar_datos.py
python -m jupyter lab
```

Abrir cada notebook desde su carpeta de clase. Las bibliotecas están fijadas a las versiones ensayadas; Colab puede incluir otras. No se depende de wget/Linux. Videos e imágenes requieren conexión.

Los CSV docentes están junto a sus clases; la noticia de terceros se recupera bajo demanda desde su fuente, sin redistribuir su texto en este repositorio. [Fuentes y huellas de datos](docs/datos-de-practica.json).

## Ejercicios y pruebas

Hay respuestas históricas, correcciones y propuestas nuevas de resolución añadidas en 2026, señaladas en sus celdas. No se atribuyen retrospectivamente como entregas de 2021. Consultar [alcance, decisiones y actividades](docs/estado-ejercicios.md) y [autoría y procedencia](docs/procedencia.md).

```sh
python herramientas/validar_cuadernos.py
python -m unittest discover -s pruebas -v
```

Las pruebas comprueban funciones/celdas reales, interfaces y datos; los notebooks pasan estructura Jupyter y sintaxis. No equivalen a aprobación docente ni a ejecutar automáticamente todas las interacciones y servicios externos.

## Material del curso y licencia

La teoría, consignas y ejemplos pertenecen a [IEEESBITBA/Curso-python](https://github.com/IEEESBITBA/Curso-python/tree/master/Curso_Introductorio_Clases). La referencia oficial se fijó en [5d558a2](https://github.com/IEEESBITBA/Curso-python/tree/5d558a2228cbe7132129b8430950fd341a5f3d1e/Curso_Introductorio_Clases); no es idéntica a las copias de la edición 2021.

Material y adaptación bajo **CC BY-NC-SA 4.0**, con atribución a IEEESBITBA. Licencias originales en [español](licencias/LICENCIA-original.txt) e [inglés](licencias/LICENSE-original.txt). Recursos externos conservan sus propios autores y condiciones.
