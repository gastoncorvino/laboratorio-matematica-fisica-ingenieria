# Generación local de videos con voz propia — laboratorio científico

**Estado: prototipo reproducible.** Diseñado para Windows PowerShell 5.1, Python 3.11, FFmpeg y el entorno **Chatterbox** que ya se encuentra instalado en `%LOCALAPPDATA%\LaboratorioVoz`.

Este proyecto **no distribuye ni publica tu muestra de voz**. No descarga otro motor ni altera los guiones existentes. El archivo `muestra_voz_personal.wav` se mantiene dentro de `%LOCALAPPDATA%\LaboratorioVoz\referencias\`, fuera de GitHub.

## Cómo usarlo

Desde PowerShell, situarse en esta carpeta del proyecto y ejecutar:

```powershell
# Validar el guion sin cargar el modelo
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\crear_video.ps1 -Episodio 001 -Idioma es -SoloValidar

# Generar solo la primera frase (prueba de voz corta con tu timbre sintético)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\crear_video.ps1 -Episodio 001 -Idioma es -Primeras 1

# Video 001 entero en español (nuevo audio sintetizado a partir de tu voz)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\crear_video.ps1 -Episodio 001 -Idioma es

# Mismo episodio narrado en inglés con la referencia de voz propia
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\crear_video.ps1 -Episodio 001 -Idioma en

# Episodio 003, por qué Fermat necesita más intentos con factores separados
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\crear_video.ps1 -Episodio 003 -Idioma es

# Opcional: variar la guía de pronunciación, experimental
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\crear_video.ps1 -Episodio 001 -Idioma es -Primeras 1 -Cfg 0.1
```

El resultado aparece en `%LOCALAPPDATA%\LaboratorioVoz\videos\episodio_001_es_final` (o según episodio e idioma). Se generan un MP4, el WAV, `subtitulos.srt`, `tiempos.json`, un JSON del guion utilizado e imágenes de escenas.

## Por qué se sincronizan mejor los subtítulos

No se usa un cronómetro estimado. **Cada fragmento corto del guion se sintetiza por separado**, se mide el número exacto de muestras de audio que genera el modelo y se asigna ese mismo intervalo a un subtítulo y un fotograma, con pausas entre frases. El modelo se carga **una sola vez** para toda la producción, importante porque el equipo actual ejecuta en CPU.

La duración final del video se adapta al audio, no se acelera el audio para encajar en escenas fijas. El subtítulo corresponde al *texto solicitado* a Chatterbox. Si el motor omite, pronuncia mal o cambia palabras, el subtítulo debe corregirse manualmente tras escuchar el video. **Esto no es alineación palabra por palabra** ni un sustituto de la revisión editorial.

## Calidad regional y privacidad

La voz obtenida es **una voz artificial basada en tu grabación original**, no una grabación humana. Chatterbox Multilingual genérico puede mezclar acentos; cambiar `-Cfg` puede alterar pronunciación y ritmo, pero **no garantiza acento argentino**. Usamos por defecto `-Modelo v2`, la API compatible con `chatterbox-tts==0.1.7`; `-Modelo v3` solo se activa si la versión instalada acepta ese parámetro.

Nunca subas muestras de voz, audios originales ni los videos privados a GitHub. Todos los medios quedan en `%LOCALAPPDATA%` por defecto. Verificá la privacidad de los proyectos y aclará la narración sintética si después decidís publicarlos.

## Guiones disponibles

- `guiones/episodio_001_es.json`: multiplicación, factorización, diferencia de cuadrados y RSA.
- `guiones/episodio_001_en.json`: versión revisada en inglés, **no traducción automática del modelo de voz**.
- `guiones/episodio_003_es.json`: por qué Fermat tarda más si los factores están alejados; 35 = 5 × 7 (1 intento) frente a 213 = 3 × 71 (23 intentos).
- `guiones/episodio_003_en.json`: adaptación al inglés.

El episodio 002 conserva su **grabación humana original**; no es necesario volver a sintetizarlo.

## Pruebas

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\crear_video.ps1 -Episodio 003 -Idioma es -SoloValidar
```

Para verificar la generación gráfica sin cargar Chatterbox, usar `-Maqueta -Primeras 2`: **exporta silencio y sobreimpresión de MAQUETA SIN VOZ; no publicarlo.**

Requisitos: `ffmpeg` accesible en PATH y el entorno `.venv` de Chatterbox instalado previamente con dependencias Pillow, numpy, soundfile y torch.

Referencias: [Chatterbox oficial](https://github.com/resemble-ai/chatterbox). El método de Fermat se presenta como herramienta educativa, no como método práctico para romper RSA actual.
