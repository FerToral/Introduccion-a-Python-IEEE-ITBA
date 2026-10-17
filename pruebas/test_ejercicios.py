"""Regresiones sobre las celdas de esta cursada, sin red ni instalaciones."""

import ast
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def fuente(clase, indice):
    path = ROOT / "clases" / f"clase-{clase:02d}" / f"clase-{clase:02d}.ipynb"
    cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
    identifier = f"clase-{clase:02d}-celda-{indice:03d}"
    return "".join(next(cell for cell in cells if cell["id"] == identifier)["source"])


def funciones(clase, indice):
    tree = ast.parse(fuente(clase, indice))
    definitions = ast.Module(body=[node for node in tree.body
                                   if isinstance(node, ast.FunctionDef)], type_ignores=[])
    namespace = {}
    exec(compile(definitions, f"clase-{clase}-celda-{indice}", "exec"), namespace)
    return namespace


def ejecutar_celda(clase, indice, entradas=()):
    output = StringIO()
    with patch("builtins.input", side_effect=entradas), redirect_stdout(output):
        namespace = {}
        exec(compile(fuente(clase, indice), f"clase-{clase}-celda-{indice}", "exec"), namespace)
    return output.getvalue().splitlines(), namespace


class ClaseUno(unittest.TestCase):
    def test_intervalo_inclusivo_y_reintento_solo_de_b(self):
        self.assertEqual(ejecutar_celda(1, 65, ["5", "5"])[0], ["5"])
        self.assertEqual(ejecutar_celda(1, 65, ["3", "1", "2", "4"])[0], ["3", "4"])

    def test_secuencia_con_una_sola_condicional(self):
        result, _ = ejecutar_celda(1, 66)
        self.assertEqual(list(map(int, result)), [1, 2, 3, 4, 5, 4, 3, 2, 1, 0])

    def test_codigos_de_barras_conservan_ceros(self):
        output, _ = ejecutar_celda(1, 78, ["3", "000000123", "1", "123000789", "3", "000031416", "2"])
        self.assertEqual(output, ["000000123", "123000789", "123000789", "123000789", "000031416", "000031416"])

    def test_contar_divisores_devuelve_valor_y_no_usa_global(self):
        function = funciones(1, 90)["divisores"]
        for number, expected in [(1, 1), (9, 3), (10, 4), (13, 2), (36, 9)]:
            with self.subTest(number=number):
                self.assertEqual(function(number), expected)
        for number in (0, -1):
            with self.assertRaises(ValueError):
                function(number)

    def test_collatz_ejemplos_de_consigna(self):
        function = funciones(1, 92)["cantPasos"]
        for number, expected in [(1, 0), (2, 1), (6, 8), (13, 9)]:
            with self.subTest(number=number):
                self.assertEqual(function(number), expected)
        with self.assertRaises(ValueError):
            function(0)

    def test_collatz_1_a_1000_con_oraculo_memorizado(self):
        function = funciones(1, 92)["cantPasos"]
        pasos = {1: 0}
        for inicio in range(1, 1001):
            secuencia = []
            numero = inicio
            while numero not in pasos:
                secuencia.append(numero)
                numero = numero // 2 if numero % 2 == 0 else 3 * numero + 1
            for anterior in reversed(secuencia):
                pasos[anterior] = pasos[numero] + 1
                numero = anterior
            self.assertEqual(function(inicio), pasos[inicio])

    def test_collatz_enteros_grandes_y_dominio(self):
        function = funciones(1, 92)["cantPasos"]
        for exponente in (53, 80, 200):
            self.assertEqual(function(2 ** exponente), exponente)
        for numero in (0, -1, -100):
            with self.assertRaises(ValueError):
                function(numero)

    def test_promedio_simple_y_ponderado_distinguen_tercera_nota(self):
        functions = funciones(1, 96)
        self.assertAlmostEqual(functions["promedio_simple"](3, 6, 9), 6)
        self.assertAlmostEqual(functions["promedio"](1, 2, 10), 4.2)
        self.assertAlmostEqual(functions["promedio"](10, 0, 0), 2)
        self.assertAlmostEqual(functions["promedio"](0, 0, 10), 3)
        self.assertAlmostEqual(functions["promedio"](4, 4, 4), 4)

    def test_primalidad_historica(self):
        function = funciones(1, 100)["primalidad"]
        expected = {2, 3, 5, 7, 11, 13, 17, 19}
        self.assertEqual({number for number in range(1, 21) if function(number)}, expected)
        self.assertFalse(function(0))
        self.assertFalse(function(-7))


class ClaseDos(unittest.TestCase):
    def test_ahorcado_ejemplos_de_entrega(self):
        for entradas, esperado in [(["PYTHON", "A", "B", "C", "P", "Y", "T", "H", "O", "N"], "9"),
                                   (["IEEE", "X", "Y", "E", "I"], "4")]:
            with self.subTest(palabra=entradas[0]):
                self.assertEqual(ejecutar_celda(2, 137, entradas)[0], [esperado])

    def test_ahorcado_letra_unica_repetida_y_acierto_inmediato(self):
        self.assertEqual(ejecutar_celda(2, 137, ["AAAA", "A"])[0], ["1"])
        self.assertEqual(ejecutar_celda(2, 137, ["A", "Z", "A"])[0], ["2"])
        self.assertEqual(ejecutar_celda(2, 137, ["ABC", "A", "B", "C"])[0], ["3"])

    def test_conversiones_de_temperatura(self):
        functions = funciones(2, 25)
        self.assertEqual(functions["farenheit"](0), 32)
        self.assertEqual(functions["farenheit"](100), 212)
        self.assertEqual(functions["farenheit"](-40), -40)
        self.assertAlmostEqual(functions["kelvin"](0), 273.15)
        self.assertAlmostEqual(functions["kelvin"](-273.15), 0)

    def test_umbral_de_cero_absoluto(self):
        output, _ = ejecutar_celda(2, 25, ["-274", "-273.15"])
        self.assertEqual(sum("Advertencia" in line for line in output), 1)
        output, _ = ejecutar_celda(2, 25, ["-273.1"])
        self.assertFalse(any("Advertencia" in line for line in output))

    def test_nombre_tarjeta_limite_y_apellido_con_nombre_incluido(self):
        function = funciones(2, 58)["nombre_tarjeta"]
        self.assertEqual(function("Ana", "Toralez"), "Ana Toralez")
        self.assertEqual(function("A", "x" * 24), "A " + "x" * 24)
        self.assertEqual(function("Fernando", "x" * 30), "F " + "x" * 24)
        self.assertEqual(function("Ana", "AnaMaria" * 4), "A " + ("AnaMaria" * 4)[:24])

    def test_tres_listas_de_pares_sin_perder_elementos(self):
        _, namespace = ejecutar_celda(2, 79)
        expected = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24,
                    26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48]
        for name in ("a", "b", "c"):
            self.assertEqual(namespace[name], expected)

    def test_intercambio_y_limites_de_cada_indice(self):
        function = funciones(2, 80)["intercambiar_letras"]
        self.assertEqual(function("hola", 0, 3), "aolh")
        self.assertEqual(function("hola", 1, 1), "hola")
        for text, a, b in [("hola", 0, 4), ("hola", 4, 0), ("hola", 0, -1),
                           ("hola", -1, 0), ("", 0, 0)]:
            with self.subTest(text=text, a=a, b=b), self.assertRaises(IndexError):
                function(text, a, b)

    def test_interfaz_de_indices_invalidos_muestra_error(self):
        output, _ = ejecutar_celda(2, 80, ["hola", "0", "4"])
        self.assertTrue(any(line.startswith("Error:") for line in output))


class ClaseTres(unittest.TestCase):
    def test_elecciones_ejemplo_y_ausencia_de_limite_arbitrario(self):
        functions = funciones(3, 85)
        votes = ["Mickey", "Donald", "Mickey", "Minnie", "Mickey", "Goofy",
                 "Daisy", "Goofy", "Goofy", "Minnie", "Goofy", "Donald"]
        self.assertEqual(functions["ganador_elecciones"](votes), "Goofy")
        self.assertEqual(functions["ganador_elecciones"](["A"] * 150 + ["B"]), "A")
        self.assertEqual(functions["recuento_votos"](["A", "B", "A", "C"]), {"A": 2, "B": 1, "C": 1})
        with self.assertRaises(ValueError):
            functions["ganador_elecciones"]([])

    def test_interfaz_elecciones_imprime_nombre(self):
        output, _ = ejecutar_celda(3, 85, ["3", "Ana", "Luis", "Ana"])
        self.assertEqual(output, ["Ana"])


if __name__ == "__main__":
    unittest.main()
