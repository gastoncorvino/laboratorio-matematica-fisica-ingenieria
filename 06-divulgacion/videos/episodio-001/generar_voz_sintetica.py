"""Generar narracion de referencia con voz sintetica de eSpeak.

Requisitos: espeak, ffmpeg, ffprobe en PATH (gratuitos).
El audio es solo un borrador accesible para sincronizar el video.
No requiere APIs, claves ni servicios de pago.
"""
from __future__ import annotations
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
VIDEO_BASE = HERE / 'render' / 'episodio_001_factorizacion_rsa_sin_voz.mp4'
DURATIONS = [7, 8, 8, 9, 11, 11, 12, 10]

def run(*cmd: str) -> None:
    subprocess.run(cmd, check=True)

def main() -> None:
    for tool in ('espeak', 'ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            raise SystemExit(f'Falta {tool} en PATH. Instalarlo y volver a intentar.')
    if not VIDEO_BASE.exists():
        raise SystemExit('Primero ejecutar: python generar_video.py (crea el video base).')
    lines = (HERE / 'guion.md').read_text(encoding='utf8').splitlines()
    spoken = []
    for line in lines:
        match = re.match(r'^\|\s*(\d+)\s*\|[^|]*\|\s*(.+?)\s*\|$', line)
        if match:
            spoken.append(match.group(2))
    if len(spoken) != len(DURATIONS):
        raise RuntimeError(f'Se esperaban {len(DURATIONS)} escenas, encontraron {len(spoken)}')
    out = HERE / 'render'
    audios = []
    for i,(text,seconds) in enumerate(zip(spoken,DURATIONS),1):
        voice = out / f'_voz_{i:02d}.wav'
        normalized = out / f'_voz_{i:02d}_normalizada.wav'
        run('espeak','-v','es-la','-s','170','-w',str(voice),text)
        # Pad exact timing to align spoken narration with each scene.
        run('ffmpeg','-y','-loglevel','error','-i',str(voice),
            '-af',f'apad,atrim=duration={seconds},afade=t=in:st=0:d=0.1,afade=t=out:st={seconds-0.15}:d=0.15',
            '-ar','44100','-ac','1',str(normalized))
        voice.unlink()
        audios.append(normalized)
    txt=out/'_audios.txt'
    txt.write_text(''.join(f"file '{p.name}'\n" for p in audios),encoding='utf8')
    entire=out/'_voz_completa.wav'
    run('ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(txt),
        '-ar','44100','-ac','1',str(entire))
    final=out/'episodio_001_factorizacion_rsa_con_voz_demo.mp4'
    run('ffmpeg','-y','-loglevel','error','-i',str(VIDEO_BASE),'-i',str(entire),
        '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k',
        '-t',str(sum(DURATIONS)),'-movflags','+faststart',str(final))
    for audio in audios: audio.unlink()
    entire.unlink();txt.unlink()
    print(f'Borrador narrado: {final}\nATENCION: voz robotica solo como referencia. Sustituir por voz propia en el montaje final.')

if __name__ == '__main__':main()
