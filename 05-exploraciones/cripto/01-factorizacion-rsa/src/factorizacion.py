"""Factorización de enteros con división por prueba y Fermat (educativo)."""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from math import isqrt


@dataclass(frozen=True)
class Resultado:
    p: int
    q: int
    intentos: int
    a: int | None = None
    b: int | None = None


def techo_raiz(n: int) -> int:
    """Devuelve ceil(sqrt(n)) de forma exacta, sin coma flotante."""
    if n < 0:
        raise ValueError("n debe ser no negativo")
    r = isqrt(n)
    return r if r * r == n else r + 1


def division_prueba(n: int) -> Resultado | None:
    """Factoriza n>=2 cuando es compuesto; None cuando n es primo."""
    if n < 2:
        raise ValueError("n debe ser >= 2")
    if n % 2 == 0:
        return Resultado(2, n // 2, 1) if n != 2 else None
    i, pasos = 3, 0
    while i <= isqrt(n):
        pasos += 1
        if n % i == 0:
            return Resultado(i, n // i, pasos)
        i += 2
    return None


def fermat(n: int, max_intentos: int = 100_000) -> Resultado | None:
    """Factorización Fermat: para impares >= 3; None si no hay factor no trivial.

    Una respuesta None NO significa que n sea primo: puede haberse agotado
    el presupuesto de intentos. `n` par se resuelve separadamente.
    """
    if n < 3:
        raise ValueError("n debe ser >= 3")
    if max_intentos < 1:
        raise ValueError("max_intentos debe ser >= 1")
    if n % 2 == 0:
        return Resultado(2, n // 2, 1)
    a = techo_raiz(n)
    for intento in range(1, max_intentos + 1):
        b2 = a * a - n
        b = isqrt(b2)
        if b * b == b2:
            p, q = a - b, a + b
            if p > 1 and p * q == n:
                return Resultado(p, q, intento, a, b)
            return None  # 1 × n: factorización trivial
        a += 1
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Factorizar un entero (educativo)")
    parser.add_argument("numero", type=int, help="entero >= 3")
    parser.add_argument("--max-intentos", type=int, default=100_000)
    args = parser.parse_args()
    n = args.numero
    print("Número:", n)
    print("Raíz superior:", techo_raiz(n))
    t = division_prueba(n)
    f = fermat(n, args.max_intentos)
    print("División por prueba:", f"{t.p} × {t.q}" if t else "primo/no factorizable")
    if f:
        print(f"Fermat: {n} = {f.a}² − {f.b}² = {f.p} × {f.q}")
        print("Intentos:", f.intentos)
    else:
        print("Fermat: sin factor no trivial dentro del límite, o número primo")


if __name__ == "__main__":
    main()
