# Resultados de la verificación inicial

**Fecha:** 2026-10-17  
**Entorno de ejecución:** Python 3.13.5 en Linux (contenedor de preparación).
**Comando reproducible:**

```bash
python -m unittest discover -s 05-exploraciones/cripto/01-factorizacion-rsa/tests -v
```

```text
test_casos_limite (test_factorizacion.FactorizacionTests.test_casos_limite) ... ok
test_division_prueba (test_factorizacion.FactorizacionTests.test_division_prueba) ... ok
test_fermat_ejemplos (test_factorizacion.FactorizacionTests.test_fermat_ejemplos) ... ok
test_raiz_superior (test_factorizacion.FactorizacionTests.test_raiz_superior) ... ok
test_rsa_demo (test_factorizacion.FactorizacionTests.test_rsa_demo) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```

**Criterio de aceptación de esta etapa:** 5 pruebas completadas sin errores y coincidencia con los ejemplos matemáticos publicados. **No** se ha realizado una evaluación de seguridad de RSA, ni benchmarking extrapolable.
