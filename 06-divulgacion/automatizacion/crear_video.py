#!/usr/bin/env python3
# coding: utf-8
"""Videos educativos narrados por el propio autor mediante clonación local autorizada.

Genera texto -> audio por fragmento -> timeline exacto -> imagen/subtitulo -> MP4.
No sube grabaciones ni usa servicios externos de sintesis.
--maqueta reemplaza el modelo por silencio PARA TESTEAR EL MONTAJE, no es voz.
"""
from __future__ import annotations
import argparse
import inspect
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS = 24
W, H = 1080, 1920
COLORS = {"fondo":(11,18,35),"blanco":(245,248,251),"gris":(181,198,217),"aqua":(85,222,188),"naranja":(251,179,115)}
FONT_BOLD=["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
FONT_REGULAR=["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def fuente(tam: int, bold=False):
    for p in (FONT_BOLD if bold else FONT_REGULAR):
        if Path(p).is_file(): return ImageFont.truetype(p,tam)
    return ImageFont.load_default()


def medir(draw, texto, f):
    box=draw.textbbox((0,0),texto,font=f)
    return box[2]-box[0]


def linea_wrap(draw, texto: str, max_ancho: int, tam: int, bold:bool=False):
    f=fuente(tam,bold)
    palabras=texto.strip().split()
    lineas=[]; actual=""
    for p in palabras:
        nuevo=(actual+' '+p).strip()
        if medir(draw,nuevo,f)>max_ancho and actual:
            lineas.append(actual);actual=p
        else:actual=nuevo
    if actual:lineas.append(actual)
    return lineas


def subtitulo_corto(txt: str, limite=106):
    """No altera el audio; el subtitulo es la frase EXACTA del fragmento."""
    if len(txt)>limite:
        raise ValueError('Subtitulo demasiado largo para una pantalla: '+txt)
    return txt


def marca(t:float)->str:
    ms=round(t*1000)
    h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'


def img_escena(escena, frase, episodio, indice, total, idioma, destino, maqueta=False):
    im=Image.new('RGB',(W,H),COLORS['fondo']); d=ImageDraw.Draw(im)
    aqua=COLORS['aqua'];blanco=COLORS['blanco'];gris=COLORS['gris']
    # Background grid / scientific palette
    for y in range(0,H,85):d.line([(0,y),(W,y)],fill=(20,31,50),width=1)
    for x in range(0,W,85):d.line([(x,0),(x,H)],fill=(20,31,50),width=1)
    d.rounded_rectangle((72,74,W-72,181),radius=24,fill=(24,48,66))
    d.text((101,100),'LABORATORIO  /  MATEMÁTICA · FÍSICA · INGENIERÍA',font=fuente(24,True),fill=aqua)
    d.text((82,253),escena.get('etiqueta','DEMOSTRACIÓN'),font=fuente(32,True),fill=aqua)
    tit=escena['titulo']
    top=339
    for line in linea_wrap(d,tit,905,73,True)[:4]:
        d.text((81,top),line,font=fuente(73,True),fill=blanco);top+=104
    # Formula block fixed in upper two-thirds
    d.rounded_rectangle((67,760,1013,1278),radius=45,fill=(25,44,67),outline=(42,103,102),width=3)
    formulas=escena.get('formulas',[])
    if not formulas:formulas=['¿QUÉ APRENDIMOS?']
    formula_top=800+(440-(len(formulas)*118))/2
    for j,form in enumerate(formulas):
        tm=88
        while tm>=35 and medir(d,form,fuente(tm,True))>850:tm-=3
        color=aqua if j==len(formulas)-1 else blanco
        d.text((W/2,int(formula_top+j*118)),form,font=fuente(tm,True),fill=color,anchor='mt')
    # Caption box with deliberate separation from card
    d.rounded_rectangle((65,1407,1015,1692),radius=34,fill=(8,11,19),outline=(69,126,130),width=2)
    texto=subtitulo_corto(frase)
    tam=43
    lineas=linea_wrap(d,texto,825,tam,True)
    while len(lineas)>3 and tam>31:
        tam-=2
        lineas=linea_wrap(d,texto,825,tam,True)
    if len(lineas)>3:raise ValueError('Subtitulo excede 3 lineas incluso con fuente ajustada: '+frase)
    height=round(tam*1.55)
    initial=1545-(len(lineas)*height)/2
    for j,line in enumerate(lineas):
        d.text((W/2,int(initial+j*height)),line,font=fuente(tam,True),fill=blanco,anchor='mt')
    d.rectangle((85,1742,997,1753),fill=(45,57,75))
    d.rectangle((85,1742,85+round((indice+1)/total*912),1753),fill=aqua)
    d.text((82,1792),f'EPISODIO {episodio}  ·  {idioma.upper()}',font=fuente(29,True),fill=gris)
    d.text((995,1792),f'{indice+1:02d} / {total:02d}',font=fuente(29,True),fill=aqua,anchor='ra')
    if maqueta:
        d.text((W/2,1872),'MAQUETA SIN VOZ — NO PUBLICAR',font=fuente(25,True),fill=(253,158,108),anchor='mm')
    im.save(destino,format='PNG')


def validar(datos):
    if not isinstance(datos,dict) or not isinstance(datos.get('escenas'),list) or not datos['escenas']:
        raise ValueError('El guion JSON debe incluir escenas.')
    for i,esc in enumerate(datos['escenas'],1):
        if not esc.get('titulo') or not isinstance(esc.get('frases'),list) or not esc['frases']:
            raise ValueError(f'Escena {i}: titulo y frases son obligatorios.')
        for frase in esc['frases']:
            if not isinstance(frase,str) or not frase.strip():raise ValueError('Frase vacía')
            subtitulo_corto(frase)
    if datos.get('idioma') not in ['es','en']:
        raise ValueError('Idioma no soportado en estos guiones: '+str(datos.get('idioma')))


def render(datos, args):
    import numpy as np
    import soundfile as sf
    out=args.salida.resolve();out.mkdir(parents=True,exist_ok=True)
    datos_path=out/'guion_usado.json'
    datos_path.write_text(json.dumps(datos,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    escenas=[(esc,frase) for esc in datos['escenas'] for frase in esc['frases']]
    sr=24000;device='none';modelo=None
    if not args.maqueta:
        if not args.referencia.is_file():raise FileNotFoundError('No existe la muestra vocal local: '+str(args.referencia))
        import torch
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        device='cuda' if torch.cuda.is_available() else 'cpu'
        print('Inicializando modelo compatible (una sola vez)... dispositivo:',device,flush=True)
        sig=inspect.signature(ChatterboxMultilingualTTS.from_pretrained)
        opts={'device':device}
        if 't3_model' in sig.parameters:opts['t3_model']='v3' if args.modelo=='v3' else 'v2'
        elif args.modelo=='v3':print('AVISO: V3 no esta disponible; usando V2 instalado.',flush=True)
        modelo=ChatterboxMultilingualTTS.from_pretrained(**opts)
        sr=modelo.sr
    if sr%FPS!=0:raise ValueError('El sample rate debe ser divisible por FPS para montaje exacto.')
    muestras_por_frame=sr//FPS
    wav_parts=[];srt=[];lista=[];timeline=[];cursor_frames=0
    for i,(esc,frase) in enumerate(escenas):
        print(f'Frase {i+1}/{len(escenas)}: {frase}',flush=True)
        if args.maqueta:
            voz=np.zeros(max(1,int((2.5+len(frase)/18)*sr)),dtype=np.float32)
        else:
            import torch
            with torch.inference_mode():
                audio=modelo.generate(frase,language_id=datos['idioma'],audio_prompt_path=str(args.referencia),exaggeration=args.exageracion,cfg_weight=args.cfg)
            voz=audio.detach().float().cpu().numpy().reshape(-1)
            if not len(voz):raise RuntimeError('El modelo devolvio audio vacio.')
            voz=np.nan_to_num(voz,nan=0,posinf=0,neginf=0)
            del audio
        speaking_samples=len(voz)
        pad=round(args.pausa*sr)
        frames=math.ceil((speaking_samples+pad)/muestras_por_frame)
        segmento=np.pad(voz.astype(np.float32),(0,frames*muestras_por_frame-speaking_samples))
        wav_parts.append(segmento)
        start=cursor_frames/FPS;end=(cursor_frames+frames)/FPS
        caption_end=start+speaking_samples/sr
        srt.append(f'{i+1}\n{marca(start)} --> {marca(caption_end)}\n{frase}\n')
        img_file=out/f'fotograma_{i+1:03}.png'
        idx=next(x for x,e in enumerate(datos['escenas']) if e is esc)
        img_escena(esc,frase,datos['episodio'],idx,len(datos['escenas']),datos['idioma'],img_file,args.maqueta)
        # concat demuxer durations assigned on frame boundaries
        lista += [f"file '{img_file.name}'", f'duration {frames/FPS:.9f}']
        timeline.append({'n':i+1,'escena':idx+1,'inicio_seg':start,'fin_seg':end,'voz_fin_seg':caption_end,'texto':frase})
        cursor_frames+=frames
    lista += [f"file '{(out/f'fotograma_{len(escenas):03}.png').name}'"]
    raw=np.concatenate(wav_parts)
    # Normalizar solo amplitud sin cambiar velocidad ni timbre; limita el volumen de salida.
    pico=float(np.max(np.abs(raw))) if len(raw)>0 else 0.0
    if pico>0:
        ganancia=min(5.0,0.87/pico)
        raw=np.clip(raw*ganancia,-0.98,0.98)
    audio_out=out/'narracion.wav';sf.write(audio_out,raw,sr,subtype='PCM_16')
    (out/'acerca_de_la_voz.json').write_text(json.dumps({
        'tipo':'silencio de prueba' if args.maqueta else 'narracion IA basada en voz propia',
        'idioma':datos['idioma'], 'modelo': args.modelo,'cfg':args.cfg,
        'exageracion':args.exageracion, 'dispositivo':device,
        'nota':'El audio original de referencia no se copia a este directorio.'
    },ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'subtitulos.srt').write_text('\n'.join(srt),encoding='utf-8')
    (out/'tiempos.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    concat_file=out/'fotogramas.ffconcat'
    concat_file.write_text('ffconcat version 1.0\n'+'\n'.join(lista)+'\n',encoding='utf-8')
    video_out=out/f"episodio_{datos['episodio']}_{datos['idioma']}_{'maqueta' if args.maqueta else 'voz_propia_ia'}.mp4"
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat_file),'-i',str(audio_out),'-t',f'{cursor_frames/FPS:.3f}', '-r',str(FPS),'-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(video_out)]
    print(f'Video: {cursor_frames/FPS:.2f} segundos; preparando MP4 ...',flush=True)
    subprocess.run(cmd,check=True,cwd=str(out))
    if not video_out.exists() or video_out.stat().st_size<1000:raise RuntimeError('MP4 no creado.')
    print('OK MP4:',video_out)
    print('SRT:',out/'subtitulos.srt')
    print('Voz:',audio_out)
    if args.maqueta:print('ATENCION: demo silenciosa, no tiene tu voz. Utilizar sin --maqueta para produccion.')


def main():
    p=argparse.ArgumentParser(description='Generar video vertical y subtitulos desde guiones y voz personal')
    p.add_argument('--guion',type=Path,required=True)
    p.add_argument('--salida',type=Path,required=True)
    p.add_argument('--referencia',type=Path,default=Path('referencia.wav'))
    p.add_argument('--modelo',choices=['v2','v3'],default='v2')
    p.add_argument('--cfg',type=float,default=0.25)
    p.add_argument('--exageracion',type=float,default=0.48)
    p.add_argument('--pausa',type=float,default=0.30)
    p.add_argument('--maqueta',action='store_true')
    p.add_argument('--validar',action='store_true')
    p.add_argument('--primeras',type=int,default=0,help='Solo los primeros N fragmentos (prueba corta)')
    a=p.parse_args()
    if not a.guion.is_file():p.error('Guion no encontrado: '+str(a.guion))
    d=json.loads(a.guion.read_text(encoding='utf-8-sig'))
    validar(d)
    if a.primeras:
        copia=[]
        n=a.primeras
        for esc in d['escenas']:
            if n <= 0: break
            nuevo=dict(esc)
            nuevo['frases']=esc['frases'][:n]
            copia.append(nuevo)
            n-=len(nuevo['frases'])
        d['escenas']=copia
    print(f"Guion valido: episodio {d['episodio']}; idioma {d['idioma']}; {len(d['escenas'])} escenas; {sum(len(s['frases']) for s in d['escenas'])} fragmentos")
    if a.validar:return
    if not shutil.which('ffmpeg'):p.error('FFmpeg no encontrado en PATH')
    render(d,a)

if __name__=='__main__':main()
