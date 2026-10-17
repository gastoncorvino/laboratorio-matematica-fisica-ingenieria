# Narración con voz propia (flujo experimental)

**Estado:** PROTOTIPO LOCAL, pendiente de validar en el equipo del autor.

Objetivo: producir narraciones para próximos episodios de Matemática, Física e Ingeniería, y versiones en otros idiomas, empleando una muestra **autorizada de la propia voz**.

## Herramienta
[Chatterbox Multilingual V3 de Resemble AI](https://github.com/resemble-ai/chatterbox) (modelo abierto, multilingüe). El audio de referencia se utiliza para generar nuevas frases; **FFmpeg solo sirve para convertir, montar y sincronizar**.

## Flujo
1. Mantener las grabaciones originales y la muestra de voz exclusivamente en el equipo personal, **fuera del repositorio**. No subir archivos WAV, M4A, pesos personalizados ni la muestra de voz.
2. Escribir un guion por idioma (por ejemplo, `episodio_003_es.txt`, `episodio_003_en.txt`). **El sintetizador no traduce:** primero se traduce y revisa el guion.
3. Instalar Python 3.11 y `chatterbox-tts` en un entorno local aislado. El primer uso descarga los pesos del modelo; usar GPU si está disponible.
4. Generar cada narración en WAV con `ChatterboxMultilingualTTS.from_pretrained(device=device, t3_model="v3")` y `model.generate(texto, language_id="es", audio_prompt_path=referencia)`.
5. Escuchar cada resultado y corregir errores de pronunciación, énfasis y términos técnicos. Preparar subtítulos **a partir de la narración final**, no de tiempos estimados.
6. Con FFmpeg o Kdenlive, sincronizar animaciones y subtítulos al audio final.
7. Documentar modelo, idioma, versión, errores detectados y limitaciones. Aclarar cuando la narración esté generada mediante IA.

## Seguridad y límites
- Nunca publicar la muestra de voz en GitHub, tampoco en repositorios privados.
- Una referencia de voz no garantiza reproducción perfecta de identidad, prosodia o acento regional.
- Los resultados en idiomas diferentes pueden cambiar el acento.
- El rendimiento en CPU puede ser muy lento.
- Este README no acredita que un modelo de clonación esté instalado o que haya generado narraciones verificadas.

Kit local independiente: `kit_voz_propia_multilingue.zip` entregado en la conversación; **no se distribuye en GitHub** porque incluye una muestra personal.
