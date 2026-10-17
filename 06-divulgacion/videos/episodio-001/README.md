# Episodio 001 — ¿Qué tiene que ver factorizar con RSA?

**Duración:** ~76 s · **Formato:** vertical 9:16 · **Audiencia:** sin criptografía y poca matemática.  
**Pieza editorial:** primera divulgación del laboratorio, no prueba de seguridad.

## Archivos

- `guion.md`: narración sugerida y texto de pantalla.
- `storyboard.md`: escenas con tiempos y mensaje central.
- `subtitulos_referencia.srt`: subtítulos temporizados aproximados para sincronizar tras grabar la voz.
- `generar_video.py`: crea PNG y MP4 con gráficos originales, Pillow y FFmpeg.
- `descripcion_plataformas.md`: títulos, descripciones y enlaces pendientes de publicar.

### Regeneración en Windows

```powershell
python -m pip install Pillow
python 06-divulgacion/videos/episodio-001/generar_video.py
```

Requiere `ffmpeg` disponible en PATH. Se creará un MP4 en el directorio `render/` (excluido de Git por ser un binario grande). El video base **no contiene voz ni música**, de manera intencional. Añadir voz propia en Kdenlive y sincronizar las frases del guion para obtener la versión publicable.

Referencias técnicas: ver documentación del proyecto E01. No usar este ejemplo para anunciar que RSA moderno está roto.

### Narración gratuita y edición

1. **Recomendado:** grabar la voz propia con el celular o Audacity, una toma por escena según `guion.md`.
2. **Alternativa Windows:** ejecutar `grabar_voz_windows.ps1` en *Windows PowerShell 5.1*. Necesita alguna voz de español instalada y crea ocho WAV para editar en Kdenlive. La voz de Windows puede sonar artificial.
3. **Demo Linux:** con `espeak`, FFmpeg y el video base generado, ejecutar `python generar_voz_sintetica.py` y se crea un MP4 narrado de referencia.
4. Importar video, audios y `subtitulos_referencia.srt` en Kdenlive. Ajustar subtítulos al audio real. Exportar **H.264, 1080 × 1920, 24 fps, AAC**.
5. Revisar pronunciación de **Fermat**, pausas, sonido, márgenes seguros y lectura completa del subtítulo en móvil. No publicar antes de revisar el montaje.

**El MP4 se excluye del control de versiones**: los archivos fuente sí se versionan; los videos publicados se enlazan desde el README.

### Versión vertical subtitulada

`subtitulos_breves.srt` es la opción breve para mostrar sobre el video (frases condensadas que no tapan el cálculo). La narración larga está en `guion.md`; el texto completo está en `subtitulos_referencia.srt` y es especialmente útil en YouTube como pista de subtítulos. La plantilla visual deja una franja baja para superponer las frases con márgenes generosos. El borrador narrado puede ser poco natural: revisarlo con audio antes de subirlo.
