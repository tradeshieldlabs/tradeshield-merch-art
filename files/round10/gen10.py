# Round 10 generator. Base primitives (glyph outlines, shield, ™) reused from round 9 gen9.py.
import random,json,sys
exec(open('/workspace/merch-design-r10/src/base.py').read())
W=WH; GR='#22C55E'; AM='#F59E0B'; RD='#EF4444'
B='/workspace/merch-design-r10/src/brutus-'
PT6=6/72  # 6pt in inches
def tm_size(s,font,size):  # brand v2: ™ = 0.6em, never below 6pt font size in print
    t=max(0.6*size,PT6*s.ppi); s.log['tm_in'].append(round(t/s.ppi*72,2)); return t
C.tm_size=tm_size
def icon(c,cx,top,h,col=CY): iw=43/51*h; c.shield(cx-iw/2,top,h,col); c.log.setdefault('icon_w_in',[]).append(round(iw/c.ppi,3)); return iw
def raw(c,x): c.el.append(x)
def para(c,lines,font,size,cx,top,anchor='c',lh=1.25,track=0.0,x=None):
    y=top
    for t,col in lines:
        y+=capH(font,size); c.text(t,font,size,cx if x is None else x,y,col,track=track,anchor=anchor); y+=size*(lh-0.72)
    return y
def candles(c,x,y,w,h,n=28,seed=3,trend=1.0,up=CY,dn=AC,wick=None,hollow_dn=False,sw=None):
    r=random.Random(seed); v=[0.0]; o=[]
    for i in range(n):
        op=v[-1]; cl=op+r.gauss(0.18*trend,1.0); hi=max(op,cl)+abs(r.gauss(0,0.45)); lo=min(op,cl)-abs(r.gauss(0,0.45)); o.append((op,cl,hi,lo)); v.append(cl)
    mn=min(q[3] for q in o); mx=max(q[2] for q in o); k=h/(mx-mn); step=w/n; bw=step*0.56; sw=sw or max(step*0.09,3)
    Y=lambda p:y+h-(p-mn)*k
    for i,(op,cl,hi,lo) in enumerate(o):
        cx=x+step*(i+0.5); col=up if cl>=op else dn
        raw(c,f'<line x1="{cx:.1f}" y1="{Y(hi):.1f}" x2="{cx:.1f}" y2="{Y(lo):.1f}" stroke="{wick or col}" stroke-width="{sw:.1f}" stroke-linecap="round"/>')
        t,b=min(Y(op),Y(cl)),max(Y(op),Y(cl)); b=max(b,t+sw)
        if hollow_dn and cl<op: raw(c,f'<rect x="{cx-bw/2+sw/2:.1f}" y="{t:.1f}" width="{bw-sw:.1f}" height="{b-t:.1f}" fill="none" stroke="{col}" stroke-width="{sw:.1f}"/>')
        else: raw(c,f'<rect x="{cx-bw/2:.1f}" y="{t:.1f}" width="{bw:.1f}" height="{b-t:.1f}" fill="{col}"/>')
def arc_text(c,txt,font,size,cx,cy,r,col,track=0.04,stroke=None,sw=0):
    f,gs,cmap,upm=glyphs(txt,font); ws=[width(ch,font,size) for ch in txt]; tot=sum(ws)+track*size*(len(txt)-1)
    import math; ang=-tot/r/2; 
    for ch,wd in zip(txt,ws):
        a=ang+wd/2/r; p,_=tpath(ch,font,size,-wd/2,0,col)
        if stroke: p=p.replace('<path ',f'<path stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" paint-order="stroke" ')
        raw(c,f'<g transform="translate({cx+r*math.sin(a):.1f},{cy-r*math.cos(a):.1f}) rotate({math.degrees(a):.2f})">{p}</g>'); ang+=(wd+track*size)/r
def stext(c,txt,font,size,x,base,col,stroke,sw,anchor='c',track=0.0):
    n=len(c.el); w=c.text(txt,font,size,x,base,col,anchor=anchor,track=track)
    c.el[n]=c.el[n].replace('<path ',f'<path stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" paint-order="stroke" '); return w
def pill(c,cx,cy,txt,col,size,fg=NV):
    w=width(txt,'Bold',size)+size*1.2; h=size*1.6
    raw(c,f'<rect x="{cx-w/2:.1f}" y="{cy-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h/2:.1f}" fill="{col}"/>'); c.text(txt,'Bold',size,cx,cy+capH('Bold',size)/2,fg,anchor='c')
def word(c,x,base,size,col=W,anchor='c'): return c.text('TradeShield','SemiBold',size,x,base,col,tm=True,anchor=anchor)
def wsize(w_in,ppi=300): return w_in*ppi/(width('TradeShield','SemiBold',1)*1.13)
INFO={}
def save(c,name,place,note=''): c.save(name); INFO[name]=dict(place=place,size_in=(round(c.w/c.ppi,2),round(c.h/c.ppi,2)),note=note)

# ---------- shared small marks ----------
for col,sfx in [(CY,''),(NV,'_navy')]:
    c=C(900,900,300); icon(c,450,180,540,CY); save(c,'nape__icon'+sfx,'label_outside 3x3in','icon 1.5in tall')
    c=C(900,900,300); s=wsize(2.6); word(c,450,450+capH('SemiBold',s)/2,s,W if col==CY else NV); save(c,'nape__wordmark'+sfx,'label_outside 3x3in','wordmark 2.6in')
# tee front: left-chest marks (wearer's left = viewer's right). Area 12x16in.
def chest(name,kind,col=W,h=4800,cx=2760,top=330):
    c=C(3600,h,300)
    if kind=='icon': icon(c,cx,top,1.55*300,CY)
    else: s=wsize(3.4); word(c,cx,top+capH('SemiBold',s),s,col)
    save(c,name,'front left chest',kind); return c
chest('tee__chest_icon','icon'); chest('tee__chest_word','word'); chest('tee__chest_word_navy','word',NV)
chest('hoodie__chest_icon','icon',h=3600,top=420)
c=C(3600,3600,300); icon(c,2760,420,1.55*300,AC); save(c,'hoodie__chest_icon_tonal','front left chest','cyan-dark tonal icon (deviation)')
# sleeves
c=C(1200,1050,300); s=wsize(2.8); word(c,600,525+capH('SemiBold',s)/2,s,NV); save(c,'tee__sleeve_word_navy','sleeve 4x3.5in')
c=C(900,3600,300); s=wsize(3.0); n=len(c.el); word(c,0,0,s,W,anchor='l'); g=''.join(c.el[n:]); del c.el[n:]
raw(c,f'<g transform="translate(450,600) rotate(90) translate(0,{capH("SemiBold",s)/2:.1f})">{g}</g>'); save(c,'hoodie__sleeve_word','hoodie left sleeve 3x12in','wordmark runs down the sleeve')

# ---------- FOUNDERS HOODIE ----------
c=C(3600,4800,300)  # A: back chart art
raw(c,f'<g opacity="1">'+''.join(f'<rect x="{300}" y="{900+i*450}" width="3000" height="4" fill="{AC}"/>' for i in range(7))+'</g>')
candles(c,300,800,3000,2700,n=34,seed=11,trend=1.4)
para(c,[('FOUNDING MEMBER','',)][0:0],'Bold',60,0,0)
c.text('FOUNDING MEMBER','SemiBold',90,300,3900,W,track=0.3); c.text('EST. 2026','SemiBold',90,3300,3900,CY,track=0.3,anchor='r')
save(c,'founders-A__back','back 12x16in','10in candlestick chart, micro-labels')
c=C(3600,3600,300)  # B: varsity front
arc_text(c,'FOUNDERS','ExtraBold',560,1800,3500,2400,W,stroke=CY,sw=26)
c.text('CLASS OF 26','Bold',180,1800,2050,CY,track=0.35,anchor='c'); icon(c,1800,2300,330,CY)
save(c,'founders-B__front','front 12x12in','varsity arch')

# ---------- PERFORMANCE HOODIE (basic): tonal icon chest + sleeve wordmark + nape ----------
# uses hoodie__chest_icon_tonal + hoodie__sleeve_word + nape__wordmark

# ---------- STAFF ----------
def staff(name,role,sub,col=W):
    c=C(3600,4800,300); s=520; c.text(role,'ExtraBold',s,1800,300+capH('ExtraBold',s),col,track=0.25,anchor='c')
    c.text(sub,'SemiBold',120,1800,300+capH('ExtraBold',s)+260,CY,anchor='c',tm=('™' in sub)) if '™' not in sub else None
    save(c,name,'back upper yoke 12in',f'{role}')
staff('admin__back','ADMIN','keeps the lights on.'); staff('mod__back','MOD','certified vibe checker.')
staff('ceo__back','CEO','Chief Execution Officer')

# ---------- HUMOR ----------
c=C(3600,4800,300)  # zoom out (A)
fx,fy,fw,fh=1150,250,1300,900
raw(c,f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="40" fill="none" stroke="{W}" stroke-width="14"/>')
candles(c,fx+80,fy+90,fw-160,fh-180,n=9,seed=5,trend=-2.5)
raw(c,f'<path d="M1800 {fy+fh+70} V{fy+fh+330} M1720 {fy+fh+250} L1800 {fy+fh+330} L1880 {fy+fh+250}" stroke="{CY}" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
candles(c,250,1650,3100,1500,n=60,seed=8,trend=1.8)
c.text('zoom out.','Bold',430,1800,3700,W,anchor='c')
save(c,'humor-zoom-out__front','front 12x16in')
c=C(3600,4800,300)  # buy high sell low (B)
for i,t in enumerate(['BUY HIGH.','SELL LOW.']):
    y=500+i*800+capH('ExtraBold',560); w=c.text(t,'ExtraBold',560,1800,y,W,anchor='c')
    raw(c,f'<rect x="{1800-w/2-60:.0f}" y="{y-capH("ExtraBold",560)/2-25:.0f}" width="{w+120:.0f}" height="50" fill="{CY}"/>')
c.text('a strategy we have retired.','Medium',150,1800,2350,CY,anchor='c')
save(c,'humor-buy-high__front','front 12x16in')
c=C(3600,4800,300)  # NDT hoodie A back: advisory-label parody
bx,by,bw,bh=700,300,2200,1500
raw(c,f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{W}"/><rect x="{bx+50}" y="{by+50}" width="{bw-100}" height="{bh-100}" fill="{NV}"/>')
c.text('NO DUMB','ExtraBold',330,1800,by+130+capH('ExtraBold',330),W,anchor='c',track=0.04)
raw(c,f'<rect x="{bx+50}" y="{by+620}" width="{bw-100}" height="420" fill="{W}"/>')
c.text('TRADES','ExtraBold',330,1800,by+620+210+capH('ExtraBold',330)/2,NV,anchor='c',track=0.12)
c.text('MARKET ADVISORY','Bold',110,1800,by+1180+capH('Bold',110),W,anchor='c',track=0.3)
c.text('CONTAINS EXPLICIT PATIENCE','SemiBold',72,1800,by+1340+capH('SemiBold',72),CY,anchor='c',track=0.25)
save(c,'ndt-A__back','back 12x16in, 7.3in label')
c=C(3600,3600,300); s=wsize(3.2)/1.05; c.text('no dumb trades.','SemiBold',150,2760,430+capH('SemiBold',150),W,anchor='c'); save(c,'ndt-A__front','front left chest')
c=C(3600,3600,300)  # NDT hoodie B: collegiate
arc_text(c,'NO DUMB','ExtraBold',520,1800,3000,2000,W,stroke=CY,sw=24)
stext(c,'TRADES','ExtraBold',600,1800,1950,W,CY,24,track=0.06)
c.text('CLUB  ·  MEMBERS ONLY','Bold',140,1800,2350,CY,anchor='c',track=0.3)
save(c,'ndt-B__front','front 12x12in')

# ---------- BRUTUS ----------
c=C(3600,4800,300); h=c.image(B+'judge.png',900,300,1800); c.text('Objection: FOMO.','Bold',300,1800,300+h+420,W,anchor='c')
c.text('— sustained.','Medium',150,1800,300+h+700,CY,anchor='c'); save(c,'brutus-objection__front','front 12x16in','raster Brutus 6in')
c=C(3600,4800,300); h=c.image(B+'cso.png',800,300,2000); raw(c,f'<rect x="700" y="{300+h-10:.0f}" width="2200" height="16" fill="{CY}"/>')
c.text('CHIEF SECURITY OFFICER','Bold',150,1800,300+h+260,W,anchor='c',track=0.25); c.text('has never once panic sold.','Medium',120,1800,300+h+470,CY,anchor='c')
save(c,'brutus-cso__back','back 12x16in')

# ---------- EMBROIDERY ----------
c=C(1200,1200,300); icon(c,600,(1200-420)/2,420,CY); save(c,'polo__chest_icon','embroidery_chest_left 4x4in','icon 1.18in w; K500 thread true cyan')
c=C(600,900,300); c.text('CEO','Bold',200,300,520,CY,track=0.15,anchor='c'); save(c,'polo__sleeve_ceo','embroidery sleeve')
c=C(1650,600,300); icon(c,825,40,520,CY); save(c,'hat-A__front','embroidery_front_large 5.5x2in','icon 1.46in w; 1695 Aqua/Teal thread')
c=C(1650,600,300); c.text('zoom out.','Bold',300,825,300+capH('Bold',300)/2,W,anchor='c'); save(c,'hat-B__front','embroidery_front_large','')
c=C(600,300,300); icon(c,300,30,240,CY); save(c,'hat-B__back','embroidery_back 2x1in','icon 0.67in (below 1.25in min — deviation)')
c=C(1770,600,300); c.text('BRUTUS SAID','Bold',190,885,250,W,anchor='c'); c.text('WAIT.','ExtraBold',230,885,520,CY,anchor='c'); save(c,'trucker__front','embroidery_front_large')

# ---------- MUGS (wrap 2700x1050 -> 2250x925 area, 7.5x3.08in): left panel = side A, right panel = side B ----------
def mark(c,cx,y,sz=95):  # small TradeShield mark: icon + wordmark
    iw=43/51*sz*1.6; ws=sz; tw=width('TradeShield','SemiBold',ws)+ws*0.7; x0=cx-(iw+iw*0.5+tw)/2
    c.shield(x0,y,sz*1.6); c.text('TradeShield','SemiBold',ws,x0+iw*1.5,y+sz*0.8+capH('SemiBold',ws)/2,W,tm=True)
def mug(name,A,Bs,img=None,pills=None,note='',tmA=False):
    c=C(2700,1050,300)
    def side(cx,spec,im=None,ptop=None):
        top=60; bot=820
        if im: h=c.image(B+im,cx-400,60,800*min(1,900/(800*Image.open(B+im).height/Image.open(B+im).width))); top=60+h+50
        if ptop: top=ptop
        if not spec: return
        mw=max(width(t,'ExtraBold',1) for t,_ in spec); fs=min(200,1080/mw,(bot-top)/(len(spec)*1.15))
        tot=capH('ExtraBold',fs)+(len(spec)-1)*fs*1.15; y=top+(bot-top-tot)/2
        for t,col in spec:
            y2=y+capH('ExtraBold',fs); c.text(t,'ExtraBold',fs,cx,y2,col,anchor='c',tm=(t=='Shield IQ')); y+=fs*1.15
    pt={}
    for (cx,cy,t,col) in pills or []: pill(c,cx,cy,t,col,80); pt[cx]=cy+110
    side(675,A,img,pt.get(675)); side(2025,Bs,None,pt.get(2025))
    mark(c,2025,900,55); save(c,name,'mug wrap 7.5x3.08in',note)
mug('mug-core-3am',[('SAFETY CHECK:',CY),('MY 3AM',W),('TRADE IDEA',W)],[('Go to',W),('sleep.',W)],pills=[(2025,150,'BLOCKED',RD)])
mug('mug-core-coffee',[('MY',W),('COFFEE.',W)],[('MY',W),('PORTFOLIO.',W)],pills=[(675,150,'CLEAR',GR),(2025,150,'CAUTION',AM)])
mug('mug-core-moon',[('"IT\'S GOING',W),('TO THE MOON."',W)],[('Shield IQ',CY),('says: maybe',W),('not today.',W)])
mug('mug-net-saw-it',[('SAW IT ON',W),('THE NETWORK',CY),('FIRST.',W)],[('(will remind',W),('you daily.)',W)])
mug('mug-net-groupchat',[('4,000 TRADERS.',W),('ONE CHAT.',CY)],[('Agreement',W),('reached: 0.',CY)])
mug('mug-net-signal',[('MOSTLY',W),('SIGNAL.',CY)],[('A little noise',W),('before coffee.',W)])
mug('mug-brutus-objection',[('OBJECTION:',W),('FOMO.',CY)],[('Sustained.',W),('— Brutus',CY)],img=None)
mug('mug-brutus-judge',[],[('Brutus does',W),('not chase.',CY)],img='judge.png')
mug('mug-brutus-cso',[],[('Has never once',W),('panic sold.',CY)],img='cso.png')
mug('mug-gen-candle',[("I'M NOT HOOKED",W),('ON CHARTS.',W)],[('I can stop',W),('any candle.',CY)])
mug('mug-gen-long-coffee',[('LONG',CY),('COFFEE.',W)],[('SHORT',CY),('SLEEP.',W)])
# ---------- TUMBLERS (3017x1200 @300 = 10.06x4in wrap) ----------
def tumb(name,lines,img=None,pills=None,chart=False):
    c=C(3017,1200,300)
    if chart: candles(c,150,700,1100,400,n=14,seed=2,trend=2)
    if img: c.image(B+img,200,120,700)
    para(c,lines,'ExtraBold',150,1508,330,lh=1.2)
    for (cx,cy,t,col) in pills or []: pill(c,cx,cy,t,col,80)
    mark(c,1508,1030,60); save(c,name,'tumbler wrap 10x4in')
tumb('tumbler-hedged',[('HYDRATED',W),('& HEDGED.',CY)],chart=True)
tumb('tumbler-core-check',[('SAFETY CHECK:',W),('HYDRATION',CY)],pills=[(1508,860,'CLEAR',GR)])
tumb('tumbler-brutus-size',[('BRUTUS IS WATCHING',W),('YOUR POSITION SIZE.',CY)],img='shades.png')
tumb('tumbler-net-room',[('READ THE ROOM.',W),('THEN THE CHART.',CY)])
# ---------- DESK MAT (9921x5197 area) ----------
c=C(9921,5197,300); raw(c,f'<rect width="9921" height="5197" fill="{NV}"/>')
for i in range(1,8): raw(c,f'<rect x="0" y="{i*650}" width="9921" height="5" fill="#1F2937"/>')
candles(c,400,700,9100,3700,n=56,seed=21,trend=1.2,sw=18)
mark(c,9921-900,4800,110); save(c,'desk-mat__chart','desk mat 32x16in full bleed','border #1F2937 gridlines')
# ---------- STICKER SHEET (1750x2482) ----------
c=C(1750,2482,300)
icon(c,437,150,500); s=wsize(1.6); raw(c,f'<rect x="900" y="230" width="760" height="300" rx="150" fill="{NV}"/>'); word(c,1280,380+capH('SemiBold',s)/2,s)
raw(c,f'<rect x="120" y="820" width="700" height="260" rx="130" fill="{NV}"/>'); c.text('zoom out.','Bold',120,470,950+capH('Bold',120)/2,W,anchor='c')
raw(c,f'<rect x="900" y="820" width="760" height="260" rx="40" fill="{NV}"/>'); c.text('no dumb trades.','Bold',95,1280,950+capH('Bold',95)/2,W,anchor='c')
c.image(B+'judge.png',150,1200,650); pill(c,1280,1350,'CLEAR',GR,110)
raw(c,f'<rect x="950" y="1600" width="660" height="380" rx="40" fill="{NV}"/>'); candles(c,1000,1650,560,280,n=8,seed=4,trend=2)
raw(c,f'<rect x="150" y="2050" width="1450" height="300" rx="150" fill="{NV}"/>'); c.text('Objection: FOMO.','Bold',130,875,2200+capH('Bold',130)/2,W,anchor='c')
save(c,'sticker-sheet','sticker sheet 5.83x8.27in')
json.dump(dict(LOG=LOG,INFO=INFO),open('/workspace/merch-design-r10/art/_log.json','w'),indent=1)
print(len(INFO),'files')
