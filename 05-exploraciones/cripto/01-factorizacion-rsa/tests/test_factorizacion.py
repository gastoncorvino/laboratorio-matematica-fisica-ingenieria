"""Pruebas ejecutables con unittest; sin paquetes adicionales."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "src"


def cargar(nombre):
    import sys
    spec = importlib.util.spec_from_file_location(nombre, ROOT / f"{nombre}.py")
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo

factor = cargar("factorizacion")
rsa = cargar("rsa_demo")


class FactorizacionTests(unittest.TestCase):
    def test_raiz_superior(self):
        self.assertEqual(factor.techo_raiz(77), 9)
        self.assertEqual(factor.techo_raiz(81), 9)
        self.assertEqual(factor.techo_raiz(3233), 57)

    def test_fermat_ejemplos(self):
        for n, factores, a, b in [(77, (7, 11), 9, 2),
                                  (95, (5, 19), 12, 7),
                                  (3233, (53, 61), 57, 4),
                                  (10403, (101, 103), 102, 1)]:
            with self.subTest(n=n):
                r = factor.fermat(n)
                self.assertEqual((r.p, r.q), factores)
                self.assertEqual((r.a, r.b), (a, b))
                self.assertEqual(r.p * r.q, n)

    def test_division_prueba(self):
        for n in (77, 95, 3233, 10403):
            resultado = factor.division_prueba(n)
            self.assertEqual(resultado.p * resultado.q, n)
        self.assertIsNone(factor.division_prueba(97))

    def test_casos_limite(self):
        self.assertIsNone(factor.fermat(97, 100))
        self.assertIsNone(factor.fermat(95, 1))
        self.assertEqual(factor.fermat(49).p, 7)
        with self.assertRaises(ValueError):
            factor.fermat(1)
        with self.assertRaises(ValueError):
            factor.techo_raiz(-1)

    def test_rsa_demo(self):
        r = rsa.demostrar_rsa()
        self.assertEqual((r["n"], r["d"], r["cifrado"], r["recuperado"]),
                         (3233, 2753, 2790, 65))


if __name__ == "__main__":
    unittest.main()
