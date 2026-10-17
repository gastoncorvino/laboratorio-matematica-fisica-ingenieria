"""RSA de libro con primos minúsculos. Nunca usar en seguridad real."""
from math import gcd


def demostrar_rsa() -> dict[str, int]:
    p, q, e, mensaje = 61, 53, 17, 65
    n = p * q
    phi = (p - 1) * (q - 1)
    assert gcd(e, phi) == 1
    d = pow(e, -1, phi)
    cifrado = pow(mensaje, e, n)
    recuperado = pow(cifrado, d, n)
    assert recuperado == mensaje
    return dict(p=p, q=q, n=n, e=e, phi=phi, d=d,
                mensaje=mensaje, cifrado=cifrado, recuperado=recuperado)


if __name__ == "__main__":
    print("DEMO EDUCATIVA: RSA sin relleno, NO SEGURO")
    for k, v in demostrar_rsa().items():
        print(f"{k}: {v}")
