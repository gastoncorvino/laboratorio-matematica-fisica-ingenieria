"""Validación estructural y matemática, sin descargar ni importar modelos TTS."""
import importlib.util
import json
from pathlib import Path
import unittest
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('crear_video',R/'crear_video.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class TestGuiones(unittest.TestCase):
    def test_todos_validos(self):
        guiones=list((R/'guiones').glob('episodio_*.json'))
        self.assertEqual(len(guiones),4)
        for f in guiones:
            with self.subTest(f=f):
                d=json.loads(f.read_text(encoding='utf8'))
                module.validar(d)
                self.assertTrue(len(d['escenas'])>=7)
    def test_factorizaciones(self):
        self.assertEqual(77,7*11)
        self.assertEqual(95,5*19)
        self.assertEqual(3233,53*61)
        self.assertEqual(35,5*7)
        self.assertEqual(213,3*71)
    def test_fermat_intentos(self):
        import math
        def intentos(n):
            a=math.isqrt(n)
            if a*a<n:a+=1
            comienzo=a
            while True:
                b2=a*a-n
                b=math.isqrt(b2)
                if b*b==b2:return (a-comienzo+1,a-b,a+b)
                a+=1
        self.assertEqual(intentos(35),(1,5,7))
        self.assertEqual(intentos(213),(23,3,71))
    def test_marcas(self):
        self.assertEqual(module.marca(89.4),'00:01:29,400')

if __name__=='__main__':unittest.main()
