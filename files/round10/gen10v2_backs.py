# v2 backs: small mark at the very top of the back print area (WWE/ALD/Kith style); graphic kept below.
import re,cairosvg
s=open('/workspace/merch-design-r10/src/gen10.py').read(); exec(s[:s.index('# ---------- shared small marks')])
def inner(f): t=open(f).read(); return re.search(r'<svg[^>]*>(.*)</svg>',t,re.S).group(1)
TOP=60  # 0.2in pad from top edge of back print area
def build(name,graphic,mark,shift):
    c=C(3600,4800,300)
    if mark=='word': sz=wsize(2.75); word(c,1800,TOP+capH('SemiBold',sz),sz,W)
    else: icon(c,1800,TOP,round(1.25*51/43*300),CY)
    if graphic: raw(c,f'<g transform="translate(0,{shift})">{inner(graphic+".svg")}</g>')
    c.save(name); cairosvg.svg2png(url=name+'.svg',write_to=name+'.png',output_width=3600,output_height=4800); print(name,c.log)
build('founders-A__back_top','founders-A__back','word',0)
build('ndt-A__back_top','ndt-A__back','icon',450)
build('ls__back_top',None,'word',0)
