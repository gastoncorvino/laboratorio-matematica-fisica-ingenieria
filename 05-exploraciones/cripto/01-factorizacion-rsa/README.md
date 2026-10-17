# E01 — Factorización de enteros, Fermat y RSA

**Estado: EN DESARROLLO — demostraciones automatizadas incluidas.**  
**Disciplina:** teoría de números / criptografía (exploración transversal)  
**Objetivo:** demostrar la diferencia entre factorizar números y polinomios, derivar Fermat, y explicar su relación conceptual con RSA.

## Pregunta

¿Por qué pasar de `7 × 11` a `77` es directo mientras que hallar factores de un entero enorme puede ser costoso? ¿Cómo se utiliza una identidad algebraica para factorizar un número entero?

## 1. Dos significados de factorización

**Enteros:** `77 = 7 × 11`. **Polinomios:** `x² - 5x + 6 = (x - 2)(x - 3)`. Son objetos matemáticos distintos. La diferencia de cuadrados los conecta:

`a² - b² = (a - b)(a + b)`.

## 2. Deducción del método de Fermat

Para un `n` impar compuesto, buscamos enteros `a ≥ ceil(sqrt(n))` y `b ≥ 0` tales que:

`a² - n = b²`.

Entonces `n = a² - b² = (a-b)(a+b)`. Iteramos `a` aumentando de uno en uno hasta hallar una diferencia cuadrada.

| n | a | a² − n | b | Factores |
|---:|---:|---:|---:|---:|
| 77 | 9 | 4 | 2 | 7 × 11 |
| 95 | 12 | 49 | 7 | 5 × 19 |
| 3233 | 57 | 16 | 4 | 53 × 61 |

**Por qué empezar en la raíz:** dado que `b² ≥ 0`, necesitamos `a² ≥ n`. Usamos aritmética entera (`math.isqrt`) para evitar errores de redondeo.

**Por qué funciona mejor con factores cercanos:** si `n = pq` y `p,q` son impares, entonces `a=(p+q)/2` y `b=|q-p|/2`, de manera que `a²-b²=pq`. Cuando `p` y `q` están próximos, `a` suele estar cerca de `sqrt(n)`.

## 3. Conexión con RSA

RSA usa un módulo `n=pq` y un exponente público `e`. Ambos componen una clave pública. La clave privada se construye a partir de información secreta relacionada con `p` y `q`. Conocer los factores de `n` permite calcular `φ(n)=(p−1)(q−1)` y recuperar un exponente privado válido `d=e⁻¹ mod φ(n)` en el ejemplo clásico.

**Ejemplo exclusivamente didáctico:** `p=61`, `q=53`, `n=3233`, `e=17`, `φ(n)=3120`, `d=2753`, mensaje numérico `m=65`, cifrado `c=2790` y recuperación `m=65`.

`c = m^e mod n` y `m = c^d mod n`.

**Advertencias:**

- Estos primos son deliberadamente pequeños. Este ejemplo **no es criptografía segura**.
- RSA real usa módulos enormemente mayores, generación aleatoria segura y esquemas de relleno como OAEP para cifrado.
- La factorización de Fermat suele ser demasiado lenta cuando los factores están lejos; otros algoritmos clásicos como GNFS emplean polinomios y técnicas más complejas.
- RSA no cifra toda la navegación web por sí mismo; es un mecanismo criptográfico de clave pública que se usa en protocolos y aplicaciones concretas.
- Con computación cuántica escalable y tolerante a fallos, el algoritmo de Shor amenaza la seguridad de RSA. Eso **no** implica que sea posible romperlo trivialmente hoy.

## 4. Ejecutar las demostraciones

Python 3.10+ sin dependencias externas para los ejemplos matemáticos.

```powershell
python 05-exploraciones/cripto/01-factorizacion-rsa/src/factorizacion.py 77
python 05-exploraciones/cripto/01-factorizacion-rsa/src/factorizacion.py 95
python 05-exploraciones/cripto/01-factorizacion-rsa/src/factorizacion.py 3233
python 05-exploraciones/cripto/01-factorizacion-rsa/src/rsa_demo.py
python -m unittest discover -s 05-exploraciones/cripto/01-factorizacion-rsa/tests -v
```

El script de factorización muestra tanto la división por prueba como Fermat y permite limitar el número de intentos. El de RSA comprueba el mensaje recuperado y declara explícitamente su inseguridad.

## 5. Hipótesis para un experimento posterior

H1: En semiprimos con factores impares cercanos, Fermat puede encontrar los factores en menos iteraciones que la división por prueba. H2: al alejar los factores, el número de intentos de Fermat crece. **Pendiente de ejecutar con baterías mayores y de publicar medidas comparables.** No extrapolar tiempos de Python a RSA-2048.

## 6. Autoevaluación

- ¿Qué diferencia existe entre factorizar un polinomio y un entero?
- ¿Por qué `a` empieza en `ceil(sqrt(n))`?
- ¿Cómo deduzco `a=(p+q)/2` y `b=(q-p)/2`?
- ¿Cuándo es ineficiente Fermat?
- ¿Qué contiene realmente la clave pública de RSA?
- ¿Por qué esta demostración no implica que RSA real sea fácil de romper?

## 7. Referencias

- Python: documentación oficial de `math.isqrt`: <https://docs.python.org/3/library/math.html#math.isqrt>.
- Python: documentación oficial de `pow`: <https://docs.python.org/3/library/functions.html#pow>.
- NIST SP 800-56B Rev. 2: recomendaciones para mecanismos de establecimiento de claves basados en factorización de enteros: <https://csrc.nist.gov/pubs/sp/800/56/b/r2/final>.
- NIST FIPS 186-5: estándar de firmas digitales con RSA entre sus algoritmos: <https://csrc.nist.gov/pubs/fips/186-5/final>.
- MIT OpenCourseWare: material de matemática para el contexto de los conceptos algebraicos: <https://ocw.mit.edu/>.

## 8. Divulgación

Guion/escenas/reproducibilidad: [`06-divulgacion/videos/episodio-001/`](../../../06-divulgacion/videos/episodio-001/).
