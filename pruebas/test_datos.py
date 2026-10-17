"""Comprueba los auxiliares y ejecuta sus ejemplos reales, sin usar la red."""

import csv
from contextlib import chdir
import hashlib
import json
from pathlib import Path
import statistics
import unittest

from test_ejercicios import ejecutar_celda, funciones

ROOT = Path(__file__).resolve().parents[1]


class ArchivosDePractica(unittest.TestCase):
    def test_integridad_y_presencia_junto_a_cada_clase(self):
        manifest = json.loads((ROOT / "docs/datos-de-practica.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["archivos"]), 4)
        for entry in manifest["archivos"]:
            for relative in entry["copias"]:
                with self.subTest(archivo=relative):
                    content = (ROOT / relative).read_bytes()
                    self.assertEqual(len(content), entry["bytes"])
                    self.assertEqual(hashlib.sha256(content).hexdigest(), entry["sha256"])

    def test_lectura_de_noticia_con_acentos_y_cierre(self):
        with chdir(ROOT / "clases/clase-02"):
            output, namespace = ejecutar_celda(2, 119)
        self.assertTrue(namespace["file"].closed)
        self.assertEqual(namespace["file"].encoding.lower(), "utf-8")
        self.assertEqual(len(namespace["contenido"]), 11)
        self.assertIn("Titán", "".join(namespace["contenido"]))
        self.assertTrue(any("cráter" in line for line in output))

    def test_mediciones_incluyen_las_8192_muestras(self):
        with chdir(ROOT / "clases/clase-02"):
            _, namespace = ejecutar_celda(2, 152)
        self.assertTrue(namespace["file"].closed)
        lines = [line for line in namespace["contenido"] if line.strip() and not line.startswith("#")]
        reader = csv.reader(lines)
        self.assertEqual(next(reader), ["Time (s)", "Channel 1 (V)", "Channel 2 (V)"])
        rows = [[float(value) for value in row] for row in reader]
        self.assertEqual(len(rows), 8192)
        self.assertTrue(all(len(row) == 3 for row in rows))
        # El original redondea muchos tiempos: no son estrictamente crecientes.
        self.assertTrue(all(a[0] <= b[0] for a, b in zip(rows, rows[1:])))
        self.assertEqual(sum(a[0] == b[0] for a, b in zip(rows, rows[1:])), 5398)

    def test_control_de_calidad_tiene_30_mil_lotes(self):
        path = ROOT / "clases/clase-02/ControlCalidadBotellas.csv"
        with path.open(encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            self.assertEqual(reader.fieldnames, ["", "Fallas"])
            rows = list(reader)
        self.assertEqual(len(rows), 30000)
        self.assertEqual([int(row[""]) for row in rows], list(range(30000)))
        self.assertTrue(all(int(row["Fallas"]) >= 0 for row in rows))

    def test_ejemplo_csv_ejecuta_y_cierra_archivo(self):
        folder = ROOT / "clases/clase-03"
        with (folder / "datos.csv").open(encoding="utf-8", newline="") as file:
            rows = list(csv.reader(file))
        with chdir(folder):
            output, namespace = ejecutar_celda(3, 76)
        self.assertEqual(rows[0], ["Legajo", "Nombre", "Apellido", "Quimica", "Matematica", "Fisica"])
        self.assertEqual(len(rows), 7)
        self.assertEqual(output, [str(row) for row in rows])
        self.assertTrue(namespace["csvfile"].closed)

    def test_ejemplo_json_de_la_clase(self):
        output, namespace = ejecutar_celda(3, 110)
        self.assertEqual(output, ["[1, 2, 3]", "3", "294"])
        self.assertEqual(namespace["d"], {"a": [1, 2, 3], "b": [4, 6, 8], "c": [99, 98, 97]})

    def test_conteo_de_palabras_casos_limite(self):
        contar = funciones(2, 127)["contar_palabra"]
        self.assertEqual(contar([], "que"), 0)
        self.assertEqual(contar(["QUE, que. aquello;que\tque?"], "que"), 4)
        self.assertEqual(contar(["cráter CRÁTER, cráteres"], "CRÁTER"), 2)
        self.assertEqual(contar(["aquel esquema cualquiera"], "que"), 0)

    def test_conteo_de_noticia_real(self):
        with chdir(ROOT / "clases/clase-02"):
            output, namespace = ejecutar_celda(2, 127)
        # Oráculo independiente para este texto: separar en palabras Unicode.
        import re
        tokens = re.findall(r"\w+", "".join(namespace["noticia"]).casefold())
        self.assertEqual(output, [f"cráter: {tokens.count('cráter')}", f"que: {tokens.count('que')}"])
        self.assertGreater(tokens.count("cráter"), 0)
        self.assertGreater(tokens.count("que"), 0)
        self.assertTrue(namespace["file"].closed)

    def test_resumen_de_columnas_y_limites(self):
        resumir = funciones(2, 152)["resumir_columnas"]
        self.assertEqual(resumir([[1, -2, 3], [3, 2, -1]]), [[1, 3, 2], [-2, 2, 0], [-1, 3, 1]])
        self.assertEqual(resumir([[2, 4, 6]]), [[2, 2, 2], [4, 4, 4], [6, 6, 6]])
        for filas in ([], [[1, 2]], [[1, 2, 3], [4, 5, 6, 7]]):
            with self.subTest(filas=filas), self.assertRaises(ValueError):
                resumir(filas)
        with chdir(ROOT / "clases/clase-02"):
            _, namespace = ejecutar_celda(2, 152)
        for columna, obtenido in enumerate(namespace["resumen"]):
            valores = [fila[columna] for fila in namespace["mediciones"]]
            self.assertEqual(obtenido[:2], [min(valores), max(valores)])
            self.assertAlmostEqual(obtenido[2], statistics.fmean(valores))

    def test_cruces_ascendentes_y_periodos(self):
        cruces = funciones(2, 152)["cruces_y_periodos"]
        filas = [[0, -1, 0], [1, 0, 0], [2, 1, 0], [3, -1, 0], [4, 2, 0]]
        self.assertEqual(cruces(filas), ([2, 4], [2]))
        self.assertEqual(cruces([]), ([], []))
        self.assertEqual(cruces([[0, 1, 0]]), ([], []))
        self.assertEqual(cruces([[0, 1, 0], [1, -1, 0]]), ([], []))

    def test_estadistica_sin_bibliotecas_casos_limite(self):
        estadisticas = funciones(2, 157)["estadisticas_fallas"]
        for datos in ([7], [1, 2, 3], [1, 1, 2, 4], [3, 3, 1, 1], [0, 0, 0]):
            copia = datos.copy()
            with self.subTest(datos=datos):
                media, varianza, moda, mediana = estadisticas(datos)
                self.assertAlmostEqual(media, statistics.mean(datos))
                self.assertAlmostEqual(varianza, statistics.pvariance(datos))
                self.assertEqual(moda, min(statistics.multimode(datos)))
                self.assertEqual(mediana, statistics.median(datos))
                self.assertEqual(datos, copia)
        with self.assertRaises(ValueError):
            estadisticas([])

    def test_estadistica_de_30_mil_lotes_reales(self):
        with chdir(ROOT / "clases/clase-02"):
            _, namespace = ejecutar_celda(2, 157)
        datos = namespace["fallas"]
        self.assertEqual(len(datos), 30000)
        self.assertAlmostEqual(namespace["media"], statistics.mean(datos))
        self.assertAlmostEqual(namespace["varianza"], statistics.pvariance(datos))
        self.assertEqual(namespace["moda"], min(statistics.multimode(datos)))
        self.assertEqual(namespace["mediana"], statistics.median(datos))
        self.assertTrue(namespace["file"].closed)


if __name__ == "__main__":
    unittest.main()
