"""Integridad del formato, preparación de Colab y dependencias científicas."""
from contextlib import chdir, redirect_stdout
from hashlib import sha256
from io import BytesIO, StringIO
import json
from pathlib import Path
import statistics
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from test_ejercicios import ROOT, ejecutar_celda, fuente

class FormatoYEntorno(unittest.TestCase):
    def test_formato_jupyter_y_ids_unicos(self):
        import nbformat
        for ruta in (ROOT / "clases").glob("*/*.ipynb"):
            nb = nbformat.read(ruta, as_version=4)
            nbformat.validate(nb)
            ids = [c.id for c in nb.cells]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertTrue(all(not c.get("outputs") for c in nb.cells))

    def test_estadistica_cientifica_contra_biblioteca_estandar(self):
        with chdir(ROOT / "clases/clase-03"):
            _, ns = ejecutar_celda(3, 93)
        media, varianza, moda, mediana = ns["estadistica_con_librerias"](ns["fallas"])
        self.assertAlmostEqual(media, statistics.mean(ns["fallas"]))
        self.assertAlmostEqual(varianza, statistics.pvariance(ns["fallas"]))
        self.assertEqual(moda, min(statistics.multimode(ns["fallas"])))
        self.assertEqual(mediana, statistics.median(ns["fallas"]))

    def test_preparacion_colab_sin_sobrescribir_y_con_huellas(self):
        for clase in (2, 3):
            ruta = ROOT / "clases" / f"clase-{clase:02}" / f"clase-{clase:02}.ipynb"
            nb = json.loads(ruta.read_text(encoding="utf-8"))
            codigo = "".join(next(c for c in nb["cells"] if c["id"].endswith("-datos"))["source"])
            carpeta = ruta.parent
            datos = {p.name: p.read_bytes() for p in carpeta.iterdir()
                     if p.name in ("noticia.txt","datos.csv","mediciones.csv","ControlCalidadBotellas.csv")}
            with TemporaryDirectory(dir=ROOT, prefix="prueba-datos-") as temporal, chdir(temporal):
                ns = {}
                def descargar(url, timeout):
                    return BytesIO(datos[url.rsplit("/", 1)[1]])
                with patch("urllib.request.urlopen", side_effect=descargar) as red, redirect_stdout(StringIO()):
                    exec(codigo, ns)
                    self.assertEqual(red.call_count, len(datos))
                    exec(codigo, ns)
                    self.assertEqual(red.call_count, len(datos))
                    Path("noticia.txt").write_text("No sobrescribir", encoding="utf-8")
                    with self.assertRaises(ValueError):
                        ns["preparar_dato"]("noticia.txt")
                    self.assertEqual(Path("noticia.txt").read_text(encoding="utf-8"), "No sobrescribir")

    def test_librerias_y_grafico_sin_interfaz(self):
        import IPython
        import requests
        import jupyterlab
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib import pyplot
        figura, eje = pyplot.subplots()
        eje.plot([0,1,2], [0,1,4])
        imagen = BytesIO()
        figura.savefig(imagen, format="png")
        pyplot.close(figura)
        self.assertGreater(len(imagen.getvalue()), 1000)

if __name__ == "__main__":
    unittest.main()
