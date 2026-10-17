"""Pruebas de las propuestas de resolución; ejecutan las celdas reales."""
from contextlib import chdir, redirect_stdout
from io import StringIO
import itertools
import math
import unittest

from test_ejercicios import ROOT, ejecutar_celda, funciones


class IntegradoresClaseUno(unittest.TestCase):
    def test_presentacion_completa(self):
        self.assertEqual(ejecutar_celda(1, 21)[0], ["Fernando Toralez tiene 20 años"])

    def test_operadores_y_modulo_historicos(self):
        self.assertIn("2.0", ejecutar_celda(1, 33, ["1", "2", "3"])[0][0])
        self.assertAlmostEqual(ejecutar_celda(1, 34, ["2", "4", "8"])[1]["mediaG"], 4)
        for horas in (0, 5, 20, 25, 45, 240):
            self.assertEqual(ejecutar_celda(1, 40, [str(horas)])[1]["hra"] % 24, horas % 24)

    def test_calificacion_en_cada_frontera(self):
        for nota, letra in [(0,"F"),(59,"F"),(60,"D"),(69,"D"),(70,"C"),
                            (79,"C"),(80,"B"),(89,"B"),(90,"A"),(100,"A")]:
            self.assertEqual(ejecutar_celda(1, 57, [str(nota)])[1]["nota"], letra)
        self.assertIn("aprobado", ejecutar_celda(1, 56, ["4"])[0][0])
        self.assertIn("desaprobado", ejecutar_celda(1, 56, ["3"])[0][0])

    def test_credenciales_didacticas_de_la_consigna(self):
        chequeo = funciones(1, 89)["chequeo"]
        self.assertTrue(chequeo("Juan", "12345_"))
        self.assertTrue(chequeo("Pablo", "xDcFvGbHn"))
        self.assertFalse(chequeo("Juan", "xDcFvGbHn"))

    def test_adivinador_todo_el_dominio_en_14_intentos(self):
        adivinar = funciones(1, 104)["adivinar"]
        for secreto in range(10000):
            def responder(pregunta):
                propuesta = int(pregunta.split()[0])
                return "=" if secreto == propuesta else "<" if secreto < propuesta else ">"
            self.assertLessEqual(adivinar(responder), 14)
        with self.assertRaises(ValueError):
            adivinar(lambda _: "<")
        respuestas = iter(["?", "="])
        self.assertEqual(adivinar(lambda _: next(respuestas)), 1)

    def test_domino_conteo_inverso_y_sin_repeticiones(self):
        ns = funciones(1, 106)
        for n in range(31):
            salida = StringIO()
            with redirect_stdout(salida):
                ns["mostrarFichas"](n)
            fichas = salida.getvalue().splitlines()
            self.assertEqual(len(fichas), ns["cantidadFichas"](n))
            self.assertEqual(len(fichas), len(set(fichas)))
            self.assertEqual(ns["valorMaximo"](len(fichas)), n)
        for cantidad in (0, -1, 2, 11, 14):
            self.assertEqual(ns["valorMaximo"](cantidad), -1)

    def test_integral_rectangulos_izquierdos_y_ultimo_parcial(self):
        integral = funciones(1, 108)["integral"]
        self.assertAlmostEqual(integral(lambda x: 2*x+1, 0, 1, 0.0001), 1.9999)
        self.assertAlmostEqual(integral(lambda x: 1, 0, 1, 0.3), 1)
        self.assertAlmostEqual(integral(lambda x: 1, 1, 0, 0.3), -1)
        self.assertEqual(integral(lambda x: 1, 0, 0, 1), 0)
        for paso in (0, -1, float("inf"), float("nan")):
            with self.assertRaises(ValueError):
                integral(lambda x: x, 0, 1, paso)

    def test_pi_y_factorial_cero(self):
        pi = funciones(1, 110)["aproximar_pi"]
        self.assertLess(abs(pi(1) - math.pi), 1e-7)
        self.assertAlmostEqual(pi(2), math.pi, places=14)
        factorial = funciones(1, 115)["f"]
        for n in range(15):
            self.assertEqual(factorial(n), math.factorial(n))
        with self.assertRaises(ValueError):
            factorial(-1)


class IntegradoresClaseDos(unittest.TestCase):
    def test_ahorcado_extra_gana_pierde_y_no_duplica_errores(self):
        ns = funciones(2, 139)
        self.assertEqual(ns["estado_ahorcado"]("AHORCADO", "AOP")[:2],
                         ("A _ O _ _ A _ O", 1))
        self.assertEqual(ns["estado_ahorcado"]("A", "ZZZ")[1], 1)
        letras = iter("AHORCDO")
        with redirect_stdout(StringIO()):
            self.assertTrue(ns["jugar_ahorcado"]("AHORCADO", lambda _: next(letras)))
            letras = iter("BCDEFG")
            self.assertFalse(ns["jugar_ahorcado"]("A", lambda _: next(letras)))

    def test_derivada_y_dias_sin_inventar_saltos(self):
        ns = funciones(2, 142)
        self.assertEqual(ns["derivada"]([10,12,8,15,15]), [2,-4,7,0])
        self.assertEqual(ns["dias_extremos"]([10,12,8,15,15]), (4,3))
        self.assertEqual(ns["dias_extremos"]([]), (None,None))
        self.assertEqual(ns["dias_extremos"]([3,2,1]), (None,2))

    def test_palindromos_exactos_y_normalizados(self):
        ns = funciones(2, 144)
        self.assertFalse(ns["palindromo"]("python"))
        self.assertFalse(ns["palindromo"]("Neuquén"))
        self.assertTrue(ns["palindromo"]("reconocer"))
        for texto in ("¿Acaso hubo búhos aca?", "Neuquén", ""):
            self.assertTrue(ns["palindromo_normalizado"](texto))

    def test_parentesis_todos_los_casos_hasta_diez_simbolos(self):
        esCorrecto = funciones(2, 146)["esCorrecto"]
        for n in range(11):
            for simbolos in itertools.product("()", repeat=n):
                texto = "".join(simbolos)
                reduccion = texto
                while "()" in reduccion:
                    reduccion = reduccion.replace("()", "")
                self.assertEqual(esCorrecto(texto), reduccion == "")
        self.assertTrue(esCorrecto("Yo (Juan) quiero (necesito) café."))

    def test_frutas_limites(self):
        fn = funciones(2, 148)["miguelito"]
        for codigo, esperado in [("BBBBBNNNNNNNN","3 Bananas y 7 Naranjas"),
                                  ("BN","0 Bananas y 1 Naranja"),("","0 Bananas y 0 Naranjas"),
                                  ("NN","0 Bananas y 1 Naranja")]:
            self.assertEqual(fn(codigo), esperado)
        with self.assertRaises(ValueError):
            fn("X")

    def test_codigo_secreto_no_cuenta_digitos_dos_veces(self):
        fn = funciones(2, 154)["comparar_codigo"]
        self.assertEqual(fn("9955", "9559"), (2, 2))
        # La primera muestra docente reutiliza el único 1 del secreto.
        # Con multiplicidades, hay 2 correctos y 1 mal ubicado, no 2.
        self.assertEqual(fn("39541", "19421"), (2, 1))
        self.assertEqual(fn("11111", "11111"), (5, 0))
        self.assertEqual(fn("12345", "99999"), (0, 0))
        for n in range(1, 5):
            for a in itertools.product("12", repeat=n):
                for b in itertools.product("12", repeat=n):
                    a, b = "".join(a), "".join(b)
                    correctos, malos = fn(a, b)
                    self.assertLessEqual(correctos + malos, n)
                    self.assertEqual(fn(b, a), (correctos, malos))

    def test_text2number_gramatica_y_enteros_grandes(self):
        fn = funciones(2, 159)["text2number"]
        for texto in ("0", "-0", "+123", " -123 ", "00012", "  42  ", "9"*100):
            self.assertEqual(fn(texto), int(texto))
        for texto in ("", " ", "-", "+", "1 2", "--1", "1.2", "١", "\t12", "1\n"):
            with self.subTest(texto=repr(texto)), self.assertRaises(ValueError):
                fn(texto)

    def test_tateti_gana_empata_y_rechaza_movimientos(self):
        ns = funciones(2, 161)
        for linea in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
            board = [" "]*9
            for posicion in linea:
                board[posicion] = "X"
            self.assertEqual(ns["ganador_tablero"](board), "X")
        for entradas, resultado in [
            (["a","0","1","1","4","2","5","3"], "X"),
            (["1","2","3","5","4","6","8","7","9"], "empate")]:
            leer = iter(entradas)
            with redirect_stdout(StringIO()):
                self.assertEqual(ns["jugar_tateti"](lambda _: next(leer)), resultado)


class IntegradoresClaseTres(unittest.TestCase):
    def test_legajo_duplicado_preserva_dato(self):
        fn = funciones(3, 25)["agregar_legajo"]
        registro = {}
        self.assertTrue(fn(registro, "001", "Ejemplo A"))
        self.assertFalse(fn(registro, "001", "Ejemplo B"))
        self.assertEqual(registro, {"001":"Ejemplo A"})

    def test_morse_y_alfabeto_completo(self):
        fn = funciones(3, 27)["decodificar_morse"]
        self.assertEqual(fn(".--. .-. --- --. .-. .- -- .- -.-. .. --- -."), "PROGRAMACION")
        self.assertEqual(fn("... --- ..."), "SOS")
        self.assertEqual(fn(""), "")
        with self.assertRaises(ValueError):
            fn("......")

    def test_sets_y_pangrama_incluye_v(self):
        _, ns = ejecutar_celda(3, 48)
        self.assertEqual(ns["vainilla"] & ns["chocolate"] & ns["dulceDeLeche"], {"Marina"})
        fn = funciones(3, 49)["es_pangrama"]
        self.assertTrue(fn("The quick brown fox jumps over the lazy dog!"))
        self.assertFalse(fn("abcdefghijklmnopqrstuwxyz"))

    def test_arcaico_conserva_signos(self):
        fn = funciones(3, 88)["traducir"]
        self.assertEqual(fn("𐌀𐌋𐌅𐌀𐌁𐌄𐌕𐌏"), "ALFABETO")
        self.assertEqual(fn("¡𐌐𐌄𐌓𐌃𐌉!"), "¡PERDI!")
        self.assertEqual(fn("¿𐌔𐌉 𐌏 𐌍𐌏? 𐌌𐌌𐌌... 𐌔𐌉."), "¿SI O NO? MMM... SI.")
        self.assertEqual(fn("123 / ñ"), "123 / ñ")

    def test_diccionarios_de_idiomas_con_datos_ficticios(self):
        _, ns = ejecutar_celda(3, 95, ["Inglés"])
        self.assertEqual(len(ns["candidatos"]), 5)
        self.assertEqual(ns["candidatos_idioma"](ns["candidatos"], "Inglés"), ["Ana","Clara","Diego"])
        comunes = funciones(3, 97)["idiomas_en_comun"]
        bilingues = funciones(3, 97)["candidatos_bilingues"]
        datos = {n: {i for i, sabe in idiomas.items() if sabe}
                 for n, idiomas in ns["candidatos"].items()}
        self.assertEqual(comunes(datos), {"Español"})
        self.assertEqual(bilingues(datos), ["Ana","Clara","Diego"])
        self.assertEqual(comunes({}), set())

    def test_frecuencias_acentos_y_sin_letras(self):
        fn = funciones(3, 101)["frecuencias_letras"]
        self.assertEqual(fn("Áa! é, Ññ 123"), {"A":0.4,"E":0.2,"Ñ":0.4})
        self.assertEqual(fn("123!?"), {})
        with chdir(ROOT / "clases/clase-03"):
            _, ns = ejecutar_celda(3, 101)
        self.assertAlmostEqual(sum(ns["frecuencias"].values()), 1)

    def test_helados_pares_y_multiformatos_con_oraculo(self):
        ns = funciones(3, 103)
        self.assertEqual(ns["buscar_precios"]([1,2,3,4,5], 8), [3,5])
        self.assertEqual(ns["buscar_precios"]([7,4,2,6,7,7], 4), [2,2])
        for precios in ([], [1], [1,1], [1,2,3], [2,2,3,3]):
            for dinero in range(8):
                opciones = [(i,j) for i in range(len(precios))
                            for j in range(i,len(precios)) if precios[i]+precios[j] == dinero]
                self.assertEqual(ns["cantidad_combinaciones"](precios, dinero), len(opciones))
                resultado = ns["buscar_precios"](precios, dinero)
                self.assertEqual(resultado != [-1,-1], bool(opciones))

    def test_chaos_no_reemplaza_subpalabras_ni_puntuacion(self):
        fn = funciones(3, 105)["traducir_oracion"]
        self.assertEqual(fn("hola, como estás?", {"hola":"你好","como":"how","estás":"estáis"}), "你好, how estáis?")
        self.assertEqual(fn("se ve bien!", {"se":"it","ve":"regards","bien":"bom"}), "it regards bom!")
        self.assertEqual(fn("verso, ve;\nve!", {"ve":"go"}), "verso, go;\ngo!")

    def test_truco_40_cartas_todos_los_duelos(self):
        ns = funciones(3, 107)
        niveles = [
            ["1 de espada"],["1 de basto"],["7 de espada"],["7 de oro"],
            [f"3 de {p}" for p in ("basto","oro","espada","copa")],
            [f"2 de {p}" for p in ("basto","oro","espada","copa")],
            ["1 de oro","1 de copa"],
            *[[f"{n} de {p}" for p in ("basto","oro","espada","copa")] for n in (12,11,10)],
            ["7 de basto","7 de copa"],
            *[[f"{n} de {p}" for p in ("basto","oro","espada","copa")] for n in (6,5,4)]
        ]
        cartas = [(c, nivel) for nivel, grupo in enumerate(niveles) for c in grupo]
        self.assertEqual(len(cartas), 40)
        for a, na in cartas:
            for b, nb in cartas:
                esperado = a if na < nb else b if nb < na else "empate"
                self.assertEqual(ns["dueloDeCartas"](a,b), esperado)
        self.assertEqual(ns["duelo_multiple"](["7 de basto","7 de espada","12 de espada","4 de espada"]), "7 de espada")
        with self.assertRaises(ValueError):
            ns["valor_carta"]("8 de oro")

    def test_json_resultados_y_columnas(self):
        fn = funciones(3, 113)["verificar_usuario"]
        datos = {"usuarios":["a@example.test","b@example.test"],"contra":["demo-a","demo-b"]}
        self.assertEqual(fn(datos, "a@example.test", "demo-a"), "OK")
        self.assertEqual(fn(datos, "a@example.test", "demo-b"), "NO")
        self.assertEqual(fn(datos, "c@example.test", "demo-a"), "DNE")
        with self.assertRaises(ValueError):
            fn({"usuarios":["a"],"contra":[]}, "a", "")


if __name__ == "__main__":
    unittest.main()
