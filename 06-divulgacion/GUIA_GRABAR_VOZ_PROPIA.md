# Guiones para grabación con voz propia — Episodios 001 y 002

## Preparación de audio (sin equipos pagos)

1. Elegí un lugar silencioso. Usá el micrófono de auriculares o el celular a 15–20 cm de la boca, ligeramente hacia un lado para evitar golpes de aire.
2. Abrí **Grabadora de sonido** de Windows, **Audacity** o la grabadora del teléfono. Graba en WAV o M4A; no hace falta voz sintética.
3. Grabá **un audio completo por episodio** siguiendo los bloques temporales de abajo. Usá un cronómetro y dejá pausas reales entre operaciones. **No aceleres la voz:** si una explicación necesita más tiempo, ajustaremos después la duración del video.
4. Guardá los audios con estos nombres: `voz_001.wav` y `voz_002.wav` (también sirve `.m4a` o `.mp3`). Conservá los originales de las grabaciones.
5. Colocalos en `Descargas` junto con los dos videos sin audio y `montar_mi_voz_episodios_001_002.ps1`, o subí ambos archivos al chat para que revisemos la sincronización y el montaje.

**Voz y estilo:** tono de conversación, no de locutor comercial. Explicá cada operación como si se la mostraras a un compañero. Marcá una pequeña pausa antes de `77 = 7 × 11` y antes del resultado `95 = 5 × 19`. En español argentino podés decir *“siete por once”*, *“al cuadrado”*, *“factorizar”*, *“R-S-A”* (letras) y *“Fermat”*.

**Importante:** los videos actuales tienen subtítulos visuales. Antes de publicarlos, comprobaremos que coincidan con la voz real; el PowerShell mezcla audio y video, pero no corrige automáticamente desajustes de frase ni edita el guion.

---

# Guion de voz — Episodio 001

**Título:** ¿Una multiplicación puede proteger información?

| Escena | Tiempo | Narración sugerida |
|---|---|---|
| 1 | 0–7 s | ¿Cómo puede una multiplicación ayudar a proteger información? Vamos a descubrirlo. |
| 2 | 7–15 s | Multiplicar es fácil: siete por once da setenta y siete. Pero ahora hagámoslo al revés. |
| 3 | 15–23 s | Si conocemos solo el setenta y siete, tenemos que averiguar qué números lo forman. Eso es factorizar un entero. |
| 4 | 23–32 s | Fermat utiliza una identidad del álgebra: una diferencia de cuadrados se puede convertir en una multiplicación. |
| 5 | 32–43 s | Buscamos un cuadrado mayor que setenta y siete. Nueve al cuadrado da ochenta y uno; la diferencia es cuatro, otro cuadrado perfecto. |
| 6 | 43–54 s | Entonces: setenta y siete es nueve al cuadrado menos dos al cuadrado. De ahí salen siete por once. |
| 7 | 54–66 s | RSA usa el producto de dos primos para construir su clave pública. Factorizar productos enormes es mucho más difícil para los métodos clásicos conocidos. |
| 8 | 66–76 s | Este ejemplo es educativo, no una forma práctica de romper RSA real. La demostración y sus pruebas están en el repositorio. |

**Edición de voz:** grabar por escena para ajustar silencios sin acelerar palabras; si los segundos no alcanzan, prolongar la escena antes que recortar conceptos.


---

# Episodio 002 — Factorizar números con Fermat, paso a paso

**Duración estimada:** 89 segundos. **Objetivo:** una persona con matemática escolar entiende por qué probar cuadrados permite descubrir factores. **Versión de video incluida:** deliberadamente sin voz artificial.

| Escena | Intervalo | Guion para voz natural |
| --- | --- | --- |
| 1 | 00:00–00:06 | ¿Podemos descubrir los números que se multiplicaron para obtener noventa y cinco? |
| 2 | 00:06–00:14 | Fermat usa una fórmula conocida: una diferencia de cuadrados se convierte en una multiplicación. |
| 3 | 00:14–00:22 | La raíz cuadrada de noventa y cinco está entre nueve y diez. Empezamos probando con diez. |
| 4 | 00:22–00:30 | Diez al cuadrado menos noventa y cinco da cinco. Cinco no es un cuadrado perfecto. |
| 5 | 00:30–00:38 | Subimos a once. Once al cuadrado menos noventa y cinco da veintiséis. Tampoco funciona. |
| 6 | 00:38–00:46 | Probamos doce: ciento cuarenta y cuatro menos noventa y cinco da cuarenta y nueve. ¡Siete al cuadrado! |
| 7 | 00:46–00:55 | Ahora aplicamos la identidad: doce menos siete es cinco, y doce más siete es diecinueve. Encontramos los factores. |
| 8 | 00:55–01:03 | En Python repetimos este procedimiento, aumentando el número hasta encontrar un cuadrado perfecto. |
| 9 | 01:03–01:11 | Con el ejemplo RSA de tres mil doscientos treinta y tres, encontramos fácilmente cincuenta y tres por sesenta y uno. |
| 10 | 01:11–01:21 | Esto no rompe RSA moderno. Fermat es especialmente rápido cuando los factores están cerca. En otros casos, puede requerir muchísimos intentos. |
| 11 | 01:21–01:29 | El código, las pruebas y las limitaciones están documentados en mi laboratorio. Estudiar, experimentar y comprobar. |

## Recomendaciones para grabar

- Grabar cada escena por separado o en una toma continua, siguiendo los tiempos.
- Pausar después de cada operación. No acelerar la lectura para encajar; ajustar duración del video si hiciera falta.
- Usar celular cerca de la boca, en lugar silencioso, o un micrófono USB; no hace falta equipo pago.
- Ajustar el volumen con auriculares y revisar en teléfono.
- Exportar audio WAV o M4A. Usar `agregar_voz.ps1` para integrarlo sin volver a generar los gráficos.

## Rigor matemático

Para todo impar compuesto `n`, el método busca enteros `a` y `b` tales que `n = a² − b² = (a−b)(a+b)`. Si `n` es primo, la representación hallada puede ser trivial `1 × n`: el programa no la presenta como factorización útil. La cantidad de intentos depende de la separación entre los factores. El módulo RSA real `n` forma parte de la clave pública junto con `e`.