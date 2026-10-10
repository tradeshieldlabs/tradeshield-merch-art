# Round 8: brand-standard re-export (TRADESHIELD-BRAND-STANDARD.md).
# Lockup = icon LEFT + "TradeShield™" white + sub-label (MERCH/NETWORK) left-aligned under it, 0.2em tracking.
# Tagline = 3 lines, ALL #22D3EE, ™ on line 3. Colors only #22D3EE, #FFFFFF, #0a0f1c, #0891B2.
# ™ = 0.45em superscript, same color as adjacent text, but never shorter than TM_MIN_IN at print size.
import os,io,base64,json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
import cairosvg
from PIL import Image
CY='#22D3EE'; WH='#FFFFFF'; NV='#0a0f1c'; AC='#0891B2'
SRC='/workspace/merch-print/_src/inter/extras/ttf/'
FONTS={k:TTFont(SRC+f'Inter-{k}.ttf') for k in ['ExtraBold','Bold','SemiBold','Medium']}
OUT='/workspace/tradeshield-merch-art/files/humor-r2'; os.makedirs(OUT,exist_ok=True)
TM_MIN_IN=0.08
BRUTUS='/workspace/tradeshield-merch/artifacts/storefront/public/images/brutus/vector/'
def glyphs(s,font):
    f=FONTS[font]; return f,f.getGlyphSet(),f.getBestCmap(),f['head'].unitsPerEm
def tpath(s,font,size,x,y,fill,track=0.0):
    f,gs,cmap,upm=glyphs(s,font); sc=size/upm; parts=[]; cx=0
    for i,ch in enumerate(s):
        g=cmap.get(ord(ch))
        if g is None: continue
        pen=SVGPathPen(gs); gs[g].draw(TransformPen(pen,(sc,0,0,-sc,x+cx,y))); d=pen.getCommands()
        if d: parts.append(d)
        cx+=gs[g].width*sc+(track*size if i<len(s)-1 else 0)
    return f'<path fill="{fill}" d="{" ".join(parts)}"/>',cx
def width(s,font,size,track=0.0): return tpath(s,font,size,0,0,'#000',track)[1]
def capH(font,size):
    f,gs,cmap,upm=glyphs('H',font); b=BoundsPen(gs); gs[cmap[ord('H')]].draw(b); return b.bounds[3]/upm*size
def tmTop(font,size):
    f,gs,cmap,upm=glyphs('™',font); b=BoundsPen(gs); gs[cmap[ord('™')]].draw(b); return b.bounds[3]/upm*size
def tmH(font,size):
    f,gs,cmap,upm=glyphs('™',font); b=BoundsPen(gs); gs[cmap[ord('™')]].draw(b); return (b.bounds[3]-b.bounds[1])/upm*size
class C:
    def __init__(s,w,h,ppi): s.w,s.h,s.ppi=w,h,ppi; s.el=[]; s.log={'tm_in':[],'small_in':[]}
    def tm_size(s,font,size):
        t=0.45*size; need=TM_MIN_IN*s.ppi
        if tmH(font,t)<need: t=need/tmH(font,1)
        s.log['tm_in'].append(round(tmH(font,t)/s.ppi,3)); return t
    def text(s,txt,font,size,x,base,col,track=0.0,tm=False,anchor='l'):
        w=width(txt,font,size,track); ts=s.tm_size(font,size) if tm else 0
        tw=w+(size*0.04+width('™',font,ts) if tm else 0)
        x0={'l':x,'c':x-tw/2,'r':x-tw}[anchor]
        p,_=tpath(txt,font,size,x0,base,col,track); s.el.append(p)
        if tm:
            # superscript: top of ™ aligned with cap top
            tb=base-capH(font,size)+tmTop(font,ts)
            s.el.append(tpath('™',font,ts,x0+w+size*0.03,tb,col)[0])
        s.log['small_in'].append(round(capH(font,size)/s.ppi,3)); return tw
    def shield(s,x,top,h,col=CY):
        sc=h/51.0; tx=x-10.5*sc+2*sc; ty=top-6.5*sc
        s.el.append(f'<g transform="translate({tx:.2f},{ty:.2f}) scale({sc:.4f})" fill="none" stroke="{col}" stroke-linecap="round" stroke-linejoin="round"><path stroke-width="4" d="M32 6.5 L52.1 14.4 Q53.5 15.2 53.5 17.4 L53.5 34.5 Q53.5 50 32 57.5 Q10.5 50 10.5 34.5 L10.5 17.4 Q10.5 15.2 11.9 14.4 Z"/><circle cx="17" cy="33" r="2.4" fill="{col}" stroke="none"/><path stroke-width="3.4" d="M19.5 33 H25 L28.5 24 L34 42 L38 31 H45"/></g>')
        return 43/51*h
    def lockup(s,cx,top,H,sub='MERCH',word='TradeShield',wcol=WH,anchor='c'):
        """icon left, wordmark right, sub-label under wordmark, left-aligned. H = icon height."""
        ws=H*0.40/capH('SemiBold',1); ss=ws*0.5
        gap=H*0.22; iw=43/51*H
        ww=width(word,'SemiBold',ws)+ws*0.04+width('™','SemiBold',s.tm_size('SemiBold',ws)); s.log['tm_in'].pop()
        sw=width(sub,'SemiBold',ss,0.2)
        tw=iw+gap+max(ww,sw)
        x0={'c':cx-tw/2,'l':cx,'r':cx-tw}[anchor]
        s.shield(x0,top,H)
        blockH=capH('SemiBold',ws)+ss*0.55+capH('SemiBold',ss); by=top+(H-blockH)/2
        s.text(word,'SemiBold',ws,x0+iw+gap,by+capH('SemiBold',ws),wcol,tm=True)
        s.text(sub,'SemiBold',ss,x0+iw+gap,by+blockH,AC if wcol==WH else NV,track=0.2)
        return tw,H
    def tagline(s,cx,top,size,lh=1.28):
        for i,t in enumerate(['Trade Safer.','Trade Smarter.','Learn Together.']):
            s.text(t,'SemiBold',size,cx,top+capH('SemiBold',size)+i*size*lh,CY,tm=(i==2),anchor='c')
        return capH('SemiBold',size)+2*size*lh
    def rule(s,cx,y,w,t,col=CY): s.el.append(f'<rect x="{cx-w/2:.1f}" y="{y:.1f}" width="{w:.1f}" height="{t:.1f}" rx="{t/2:.1f}" fill="{col}"/>')
    def image(s,path,x,y,w):
        im=Image.open(path).convert('RGBA'); h=w*im.height/im.width; b=io.BytesIO(); im.save(b,'PNG')
        s.el.append(f'<image x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" href="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}"/>'); return h
    def save(s,name):
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.w/s.ppi:.4f}in" height="{s.h/s.ppi:.4f}in" viewBox="0 0 {s.w} {s.h}">'+''.join(s.el)+'</svg>'
        open(f'{OUT}/{name}.svg','w').write(svg); cairosvg.svg2png(bytestring=svg.encode(),write_to=f'{OUT}/{name}.png',output_width=s.w,output_height=s.h)
        LOG[name]=dict(tm_in=sorted(set(s.log['tm_in'])),smallest_in=min(s.log['small_in']) if s.log['small_in'] else None)
LOG={}
def slogan_lines(c,cx,top,lines,size,lh=1.12,font='ExtraBold',fitw=None):
    fitw=fitw or c.w*0.86
    mw=max(width(t,font,size) for t,_ in lines)
    if mw>fitw: size=size*fitw/mw
    y=top
    for t,col in lines:
        y+=capH(font,size); c.text(t,font,size,cx,y,col,anchor='c'); y+=size*(lh-0.72)
    return y
def back_std(name,sub='MERCH'):
    c=C(3600,4800,300); c.lockup(1800,500,520,sub); c.tagline(1800,1350,250)
    c.text('tradeshieldlabs.com','Medium',120,1800,2420,CY,anchor='c'); c.save(name)
