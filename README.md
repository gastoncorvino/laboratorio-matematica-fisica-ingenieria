# Laboratorio de Matemática, Física e Ingeniería

> Portfolio técnico y cuaderno de aprendizaje autodidacta, abierto y reproducible.

**Estado:** proyecto iniciado · **Fecha de inicio:** 17-10-2026  
**Modalidad:** formación gratuita y autodidacta · **Referencias principales:** MIT OpenCourseWare.

## ¿Para qué existe este laboratorio?

Documentar **qué entiendo**, **cómo lo deduzco**, **cómo lo pongo a prueba** y **qué limitaciones tiene** lo que construyo. El código es una herramienta para validar y aplicar conocimientos; no todos los temas requieren software. También se aceptan demostraciones en papel, informes experimentales, diseños, mediciones y simulaciones.

Cada trabajo declara su estado (`PLANIFICADO`, `EN DESARROLLO`, `VERIFICADO`, `REVISAR`), así como las fuentes, supuestos y pruebas. **No se considera demostrado un conocimiento solo por publicar un video o ejecutar un programa.**

## Mapa del repositorio

| Carpeta | Propósito |
| --- | --- |
| `00-plan-de-estudios/` | Hoja de ruta de ocho semestres y bibliografía |
| `01-matematica/` | Cálculo, álgebra, EDO y estadística |
| `02-fisica/` | Mecánica, ondas, electromagnetismo y cuántica |
| `03-ingenieria/` | Métodos numéricos, electrónica, materiales y control |
| `04-laboratorios-integradores/` | Problemas que requieren varias disciplinas |
| `05-exploraciones/` | Temas transversales complementarios; RSA inicia aquí |
| `06-divulgacion/` | Guiones, fuentes visuales y publicaciones |
| `07-evaluaciones/` | Autoevaluaciones, criterios y evidencia de progreso |
| `plantillas/` | Fichas reproducibles para nuevas unidades |

## Primer proyecto: factorización de enteros y RSA

**Exploración E01 — Factorización, diferencia de cuadrados y RSA (didáctico)**  
[Ver documentación, código, resultados esperados y limitaciones](05-exploraciones/cripto/01-factorizacion-rsa/README.md).

```powershell
python 05-exploraciones/cripto/01-factorizacion-rsa/src/factorizacion.py 3233
python 05-exploraciones/cripto/01-factorizacion-rsa/src/rsa_demo.py
python -m unittest discover -s 05-exploraciones/cripto/01-factorizacion-rsa/tests -v
```

*No implementa criptografía para uso real, ni afirma haber roto RSA moderno.*

## Primer semestre del plan base

- **M1** Cálculo diferencial e integral — MIT 18.01SC.
- **F1** Mecánica clásica I — MIT 8.01SC.
- **I1** Métodos numéricos — temas iniciales de MIT 2.086.
- **Laboratorio integrador 1:** simulación de movimiento, comparación analítico/numérico, energía y error.

Estos módulos están **planificados**. La exploración RSA **no** reemplaza un módulo del currículo.

## Qué constituye una entrega verificable

1. Enunciado del problema y motivación.
2. Fundamentos, derivaciones y fuentes consultadas.
3. Implementación, cálculo o procedimiento replicable.
4. Pruebas con resultados esperados, casos límite y contrastes.
5. Interpretación, errores, supuestos y limitaciones.
6. Divulgación accesible: video breve y, cuando corresponda, explicación extendida.
7. Autoevaluación y próximos experimentos.

Ver la [metodología de evidencia](docs/metodologia-evidencia.md) y la [plantilla de proyecto](plantillas/FICHA_PROYECTO.md).

## Bibliografía

MIT OpenCourseWare: <https://ocw.mit.edu/>. Cada unidad agregará bibliografía primaria específica y enlaces verificables. Los números de curso en el plan indican materiales de referencia, **no** acreditaciones ni afiliación con el MIT.

## Licencia

Código de ejemplo: MIT (véase `LICENSE`). Textos, explicaciones y gráficos originales: CC BY 4.0, salvo indicación en contrario. Los contenidos de terceros conservan sus propios derechos.

## Publicar este repositorio por primera vez desde Windows

Tras descomprimir el proyecto e instalar Git y [GitHub CLI](https://cli.github.com/), desde Windows PowerShell ejecutar `./publicar_github.ps1` (o `& .\publicar_github.ps1`). El script identifica la cuenta iniciada en `gh`, crea un repositorio **público nuevo** y sube el código. **Nunca sobreescribe otro repositorio existente**. Autenticarse por navegador cuando GitHub lo solicite. No guardar credenciales en scripts.

**Actualizaciones posteriores** desde esta misma carpeta: `git add . ; git commit -m "Descripcion del avance" ; git push`. Versionar solamente contenido original y archivos permitidos; los MP4 quedan fuera del repositorio. Ver también `docs/guia-publicacion.md`.
