"""Generador de video vertical E01 (graficos originales; sin voz).

Uso: python generar_video.py
Deps: Pillow (pip install Pillow), ffmpeg instalado en PATH.
No necesita cuenta, servicios en la nube ni recursos externos.
"""
from __future__ import annotations
import math
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / 'render'
OUT.mkdir(exist_ok=True)
W, H = 1080, 1920
DURATIONS = [7, 8, 8, 9, 11, 11, 12, 10]
NAVY = (11, 17, 37)
WHITE = (244, 247, 251)
MUTED = (179, 195, 213)
TEAL = (87, 220, 189)
ORANGE = (252, 183, 111)
VIOLET = (182, 151, 245)
SCENES = [
    dict(label='LA MATEMÁTICA QUE PROTEGE', title='¿UNA MULTIPLICACIÓN\nPUEDE PROTEGER\nTUS DATOS?', formula=['7 × 11 = 77'], note='De una cuenta de primaria a la criptografía.', color=TEAL),
    dict(label='01 / MULTIPLICAR', title='MULTIPLICAR\nES FÁCIL', formula=['7 × 11 = 77'], note='Conocemos los factores y calculamos el producto.', color=ORANGE),
    dict(label='02 / FACTORIZAR', title='¿Y SI VAMOS\nAL REVÉS?', formula=['77 = ? × ?'], note='Encontrar los factores es el problema inverso.', color=VIOLET),
    dict(label='03 / EL ÁLGEBRA AYUDA', title='UNA DIFERENCIA\nDE CUADRADOS', formula=['a² − b²', '= (a − b)(a + b)'], note='Una resta se convierte en una multiplicación.', color=TEAL),
    dict(label='04 / MÉTODO DE FERMAT', title='PROBEMOS\nCON 77', formula=['9² = 81', '81 − 77 = 4 = 2²'], note='Buscamos un cuadrado cuyo exceso sea otro cuadrado.', color=ORANGE),
    dict(label='05 / ENCONTRAMOS LOS FACTORES', title='LA IDENTIDAD\nREVELA EL RESULTADO', formula=['77 = 9² − 2²', '= (9 − 2)(9 + 2)', '= 7 × 11'], note='¡Acabamos de factorizar 77!', color=TEAL),
    dict(label='06 / CONEXIÓN CON RSA', title='PRIMOS SECRETOS.\nPRODUCTO PÚBLICO.', formula=['61 × 53 = 3233'], note='El módulo n es parte de la clave pública RSA.', color=VIOLET),
    dict(label='07 / EL LÍMITE DEL EJEMPLO', title='¿ASÍ SE ROMPE\nRSA REAL?', formula=['NO TAN FÁCIL'], note='Es una demostración educativa. Código y pruebas en GitHub.', color=ORANGE),
]

FONT_CANDIDATES = {
 'heavy': ['/usr/share/fonts/truetype/inter/Inter-Bold.otf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','C:/Windows/Fonts/segoeuib.ttf','C:/Windows/Fonts/arialbd.ttf'],
 'regular': ['/usr/share/fonts/truetype/inter/Inter-Regular.otf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','C:/Windows/Fonts/segoeui.ttf','C:/Windows/Fonts/arial.ttf'],
}

def font(size, weight='regular'):
    for f in FONT_CANDIDATES[weight]:
        if Path(f).exists():
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()

def tw(draw, txt, f):
    b = draw.textbbox((0,0),txt,font=f)
    return b[2]-b[0]

def gradient(img, i):
    d=ImageDraw.Draw(img)
    for y in range(H):
        t=y/H
        # Subtle nocturnal blue-to-purple for continuity
        color=(int(10+10*t), int(17+11*t), int(35+30*t))
        d.line((0,y,W,y),fill=color)

def center_fit(draw, text, y, max_w=910, max_size=121, min_size=45, fill=WHITE):
    size=max_size
    f=font(size,'heavy')
    while size > min_size and tw(draw,text,f)>max_w:
        size-=2
        f=font(size,'heavy')
    draw.text((W/2,y),text,font=f,fill=fill,anchor='mt',stroke_width=0)
    return size

def make_slide(scene, i):
    im=Image.new('RGB',(W,H),NAVY);gradient(im,i);d=ImageDraw.Draw(im,'RGBA')
    color=scene['color']
    # Abstract geometry and subtle grid, created in code
    for x in range(80,W,80):
        d.line((x,0,x,H),fill=(255,255,255,7),width=1)
    for y in range(80,H,80):
        d.line((0,y,W,y),fill=(255,255,255,7),width=1)
    for r in [155,220,290]:
        d.ellipse((W-200-r,-110-r,W-200+r,-110+r),outline=(*color,30),width=3)
    for r in [120,190,255]:
        d.ellipse((-90-r,H-200-r,-90+r,H-200+r),outline=(*color,19),width=2)
    # Brand block
    d.rounded_rectangle((84,105,145,166),radius=15,fill=(*color,255))
    d.text((114,135),'∑',font=font(37,'heavy'),fill=(11,17,37),anchor='mm')
    d.text((170,129),'LABORATORIO',font=font(30,'heavy'),fill=WHITE)
    d.text((170,168),'MATEMÁTICA  ·  FÍSICA  ·  INGENIERÍA',font=font(18),fill=MUTED)
    # Header
    d.rounded_rectangle((84,287,84+min(800,tw(d,scene['label'],font(25,'heavy'))+49),340),radius=15,fill=(*color,30),outline=(*color,100),width=2)
    d.text((108,298),scene['label'],font=font(25,'heavy'),fill=(*color,255))
    top=400
    for row in scene['title'].split('\n'):
        fs=80
        ft=font(fs,'heavy')
        while tw(d,row,ft)>925 and fs>52:
            fs-=2;ft=font(fs,'heavy')
        d.text((83,top),row,font=ft,fill=WHITE)
        top+=108
    # A large central mathematical card
    card_top=715;card_bottom=1230
    d.rounded_rectangle((67,card_top+14,1013,card_bottom+14),radius=44,fill=(0,0,0,80))
    d.rounded_rectangle((67,card_top,1013,card_bottom),radius=44,fill=(23,36,62,255),outline=(*color,90),width=3)
    d.rounded_rectangle((106,card_top+37,383,card_top+83),radius=18,fill=(*color,43))
    d.text((133,card_top+44),'DEMOSTRACIÓN',font=font(24,'heavy'),fill=(*color,255))
    lines=scene['formula']
    heights={1:103,2:135,3:122}
    space=heights[len(lines)]
    formula_start = (card_top+card_bottom)/2 - len(lines)*space/2 + 19
    for j,txt in enumerate(lines):
        fill=(*color,255) if j==len(lines)-1 else WHITE
        center_fit(d,txt,formula_start+j*space, max_w=850,max_size=(117 if len(lines)==1 else 92), fill=fill)
    # Insight
    d.line((84,1324,996,1324),fill=(*color,120),width=3)
    d.text((84,1371),'¿QUÉ APRENDIMOS?',font=font(26,'heavy'),fill=(*color,255))
    # wrap note to 780px
    parts=[]; line=''
    for word in scene['note'].split():
        candidate=(line+' '+word).strip()
        if tw(d,candidate,font(46,'regular'))>882 and line:
            parts.append(line);line=word
        else:line=candidate
    if line:parts.append(line)
    y=1432
    for part in parts:
        d.text((84,y),part,font=font(46),fill=WHITE);y+=69
    # Progress and footer
    d.rounded_rectangle((84,1715,996,1728),radius=7,fill=(255,255,255,38))
    d.rounded_rectangle((84,1715,84+int((i+1)/len(SCENES)*912),1728),radius=7,fill=(*color,255))
    d.text((84,1780),'E01  ·  FACTORIZACIÓN Y RSA',font=font(27,'heavy'),fill=MUTED)
    d.text((996,1780),f'{i+1:02d} / {len(SCENES):02d}',font=font(27,'heavy'),fill=(*color,255),anchor='ra')
    im.convert('RGB').save(OUT/f'escena_{i+1:02d}.png',quality=95)


def render_video():
    if shutil.which('ffmpeg') is None:
        raise RuntimeError('Se necesita FFmpeg instalado y disponible en PATH')
    segments=[]
    for i,duration in enumerate(DURATIONS,1):
        source=OUT/f'escena_{i:02d}.png'
        target=OUT/f'_segmento_{i:02d}.mp4'
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
             '-loop','1','-framerate','24','-i',str(source),'-t',str(duration),
             '-vf',f'fade=t=in:st=0:d=0.25,fade=t=out:st={duration-.25}:d=0.25,format=yuv420p',
             '-c:v','libx264','-preset','veryfast','-crf','23',
             '-pix_fmt','yuv420p','-r','24','-movflags','+faststart',str(target)]
        subprocess.run(cmd,check=True)
        segments.append(target)
    txt=OUT/'_unir.txt'
    txt.write_text(''.join("file '"+f.name+"'\n" for f in segments),encoding='utf-8')
    outfile=OUT/'episodio_001_factorizacion_rsa_sin_voz.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0',
                    '-i',str(txt),'-c','copy','-movflags','+faststart',str(outfile)],check=True)
    for seg in segments:seg.unlink()
    txt.unlink()
    return outfile


def main():
    for i,scene in enumerate(SCENES):
        make_slide(scene,i)
    print('Escenas generadas:',len(SCENES))
    p=render_video()
    print('Video:',p)
    print('Duración:',sum(DURATIONS),'segundos, sin voz')

if __name__=='__main__':main()
