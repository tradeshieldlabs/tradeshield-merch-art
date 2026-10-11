# Round 9: Brand Standard v2 (STRICT) sec 3/4/9 re-export. Lockup: icon H = 1.6 x wordmark cap height, gap = 0.5 x icon width,
# sub-label muted #94A3B8 left-aligned under wordmark; ™ 0.6em, min 0.09in. Lockups keep their round-8 overall width.
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
CY='#22D3EE'; WH='#FFFFFF'; NV='#0A0F1C'; AC='#0891B2'; MU='#94A3B8'
SRC='/workspace/merch-print/_src/inter/extras/ttf/'
FONTS={k:TTFont(SRC+f'Inter-{k}.ttf') for k in ['ExtraBold','Bold','SemiBold','Medium']}
OUT='/workspace/tradeshield-merch-art/files/round9'; os.makedirs(OUT,exist_ok=True)
TM_MIN_IN=0.09
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
    def __init__(s,w,h,ppi): s.w,s.h,s.ppi=w,h,ppi; s.el=[]; s.log={'tm_in':[],'small_in':[]}; s.locks=[]
    def tm_size(s,font,size):
        t=0.6*size; need=TM_MIN_IN*s.ppi
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
    def lockup(s,cx,top,H8,sub='MERCH',word='TradeShield',wcol=WH,anchor='c'):
        """v2 lockup. H8 = the round-8 icon height; the v2 lockup is solved to the same overall width."""
        tw8=s._w8(H8,sub,word); H=H8*tw8/s._wv2(H8,sub,word)
        ws=H/(1.6*capH('SemiBold',1)); ss=ws*0.5; iw=43/51*H; gap=0.5*iw
        tw=s._wv2(H,sub,word)
        x0={'c':cx-tw/2,'l':cx,'r':cx-tw}[anchor]
        top=top+(H8-H)/2
        s.shield(x0,top,H)
        blockH=capH('SemiBold',ws)+ss*0.55+capH('SemiBold',ss); by=top+(H-blockH)/2
        s.text(word,'SemiBold',ws,x0+iw+gap,by+capH('SemiBold',ws),wcol,tm=True)
        s.text(sub,'SemiBold',ss,x0+iw+gap,by+blockH,MU if wcol==WH else NV,track=0.2)
        s.locks.append(dict(iconH_in=round(H/s.ppi,3),capH_in=round(capH('SemiBold',ws)/s.ppi,3),ratio=round(H/capH('SemiBold',ws),3),gap_in=round(gap/s.ppi,3),iconW_in=round(iw/s.ppi,3),gap_ratio=round(gap/iw,3),width_in=round(tw/s.ppi,3),sub=MU if wcol==WH else NV,sub_x_eq_word_x=True))
        return tw,H
    def _tmw(s,ws):
        t=0.6*ws; need=TM_MIN_IN*s.ppi
        if tmH('SemiBold',t)<need: t=need/tmH('SemiBold',1)
        return ws*0.04+width('™','SemiBold',t)
    def _wv2(s,H,sub,word):
        ws=H/(1.6*capH('SemiBold',1)); iw=43/51*H
        return iw+0.5*iw+max(width(word,'SemiBold',ws)+s._tmw(ws),width(sub,'SemiBold',ws*0.5,0.2))
    def _w8(s,H,sub,word):
        ws=H*0.40/capH('SemiBold',1); iw=43/51*H; t=0.45*ws; need=0.08*s.ppi
        if tmH('SemiBold',t)<need: t=need/tmH('SemiBold',1)
        return iw+H*0.22+max(width(word,'SemiBold',ws)+ws*0.04+width('™','SemiBold',t),width(sub,'SemiBold',ws*0.5,0.2))
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
        LOG[name]=dict(tm_in=sorted(set(s.log['tm_in'])),smallest_in=min(s.log['small_in']) if s.log['small_in'] else None,lockups=s.locks)
LOG={}
def slogan_lines(c,cx,top,lines,size,lh=1.12,font='ExtraBold',fitw=None):
    fitw=fitw or c.w*0.86
    mw=max(width(t,font,size) for t,_ in lines)
    if mw>fitw: size=size*fitw/mw
    y=top
    for t,col in lines:
        y+=capH(font,size); c.text(t,font,size,cx,y,col,anchor='c'); y+=size*(lh-0.72)
    return y
# ---------- apparel (12x16in @300ppi) ----------
def back_std(name,sub='MERCH'):
    c=C(3600,4800,300); c.lockup(1800,500,520,sub); c.tagline(1800,1350,250)
    c.text('tradeshieldlabs.com','Medium',120,1800,2420,CY,anchor='c'); c.save(name)
def left_chest(name,sub='MERCH'):
    c=C(3600,4800,300); c.lockup(3350,700,300,sub,anchor='r'); c.save(name)
def slogan_front(name,lines,sub='MERCH',size=430,brutus=None,foot=None,bw=1600):
    c=C(3600,4800,300); y=420
    if brutus: h=c.image(BRUTUS+brutus,1800-bw/2,y,bw); y+=h+120
    y=slogan_lines(c,1800,y,lines,size)
    if foot: y+=60; c.rule(1800,y,1500,26); y+=200; c.text(foot,'SemiBold',120,1800,y,WH,track=0.2,anchor='c'); y+=60
    c.lockup(1800,y+260,330,sub); c.save(name)
W,CYn=WH,CY
slogan_front('network-awareness-over-hype__front',[('AWARENESS',W),('OVER HYPE.',CY)],'NETWORK')
slogan_front('network-brutus-approved__front',[('BRUTUS',W),('APPROVED.',CY)],'NETWORK',brutus='brutus-thumbsup-approved.webp',size=380)
slogan_front('network-see-what-traders-are-seeing__front',[('SEE WHAT',W),('TRADERS ARE',W),('SEEING.',CY)],'NETWORK',size=400)
slogan_front('network-the-network-saw-it-first__front',[('THE NETWORK',W),('SAW IT FIRST.',CY)],'NETWORK',size=380)
slogan_front('network-patience-is-a-position__front',[('PATIENCE IS',W),('A POSITION.',CY)],'NETWORK',size=400)
slogan_front('network-signal-over-noise__front',[('SIGNAL',W),('OVER NOISE.',CY)],'NETWORK')
slogan_front('network-built-for-the-network-hoodie__front',[('BUILT FOR',W),('THE NETWORK',CY)],'NETWORK',size=380)
slogan_front('network-network-intelligence-unit-hoodie__front',[('NETWORK',W),('INTELLIGENCE',W),('UNIT',CY)],'NETWORK',size=380)
slogan_front('network-signal-crew-hoodie__front',[('SIGNAL',W),('CREW',CY)],'NETWORK',size=520)
slogan_front('risk-manager-tee__front',[('RISK',W),('MANAGER',CY)],foot='POSITION SIZED. STRESS TESTED.',size=520)
slogan_front('side-eye-before-buy-tee__front',[('SIDE-EYE',W),('BEFORE BUY',CY)],foot='DUE DILIGENCE, DAILY.',size=440)
slogan_front('no-dumb-trades-hoodie__front',[('NO DUMB',W),('TRADES',CY)],foot='THINK. VERIFY. TRADE.',size=520)
slogan_front('brutus-approved-tee__front',[('BRUTUS',W),('APPROVED.',CY)],brutus='brutus-thumbsup-approved.webp',size=380)
slogan_front('cso-hoodie__front',[('CHIEF SECURITY',W),('OFFICER',CY)],foot='BRUTUS APPROVED',brutus='brutus-cso-portrait.webp',size=300,bw=700)
slogan_front('ask-shield-iq-tee__front',[('ASK',W),('SHIELD IQ',CY)],foot='ASK. VERIFY. TRADE.',size=520)
# Shield IQ needs ™: draw slogan with tm
c=C(3600,4800,300); y=420+capH('ExtraBold',520); c.text('ASK','ExtraBold',520,1800,y,W,anchor='c'); y+=520*0.4+capH('ExtraBold',520); c.text('SHIELD IQ','ExtraBold',520,1800,y,CY,tm=True,anchor='c'); y+=200; c.rule(1800,y,1500,26); y+=200; c.text('ASK. VERIFY. TRADE.','SemiBold',120,1800,y,W,track=0.2,anchor='c'); c.lockup(1800,y+320,330,'MERCH'); c.save('ask-shield-iq-tee__front')
for t,lines,size in [('revenge-trading',[('REVENGE TRADING',W),('IS NOT A',W),('STRATEGY.',CY)],330),('risk-managed',[('RISK MANAGED.',CY),('FEELINGS',W),('NOT.',W)],400),('trade-the-plan',[('TRADE THE PLAN.',W),('NOT THE',CY),('PANIC.',CY)],360)]:
    slogan_front(f'humor-{t}__front',lines,size=size)
c=C(3600,4800,300); y=slogan_lines(c,1800,420,[('SMALL DOG.',W)],160); y=slogan_lines(c,1800,y+60,[('BIG RISK',W),('CONTROLS.',CY)],460); c.rule(1800,y+80,1500,26); c.text('OFFICE OF THE C.S.O.','SemiBold',130,1800,y+300,W,track=0.2,anchor='c'); c.lockup(1800,y+560,330,'MERCH'); c.save('cso-hoodie__back')
back_std('tee__back_std'); back_std('hoodie__back_std'); back_std('tee__back_std_network','NETWORK')
left_chest('tee__front_LC'); left_chest('hoodie__front_LC'); left_chest('tee__front_LC_network','NETWORK')
# staff
c=C(3600,4800,300); y=slogan_lines(c,1800,420,[('ADMIN',CY)],620); y=slogan_lines(c,1800,y+40,[('KEEPER OF THE KEYS',W)],170); c.text('$ sudo trade --safer','SemiBold',150,1800,y+260,CY,anchor='c'); c.lockup(1800,y+520,330,'MERCH'); c.save('staff-admin__tee_back')
for k,lines,size in [('M1-vibe-checker',[('MOD',CY),('PROFESSIONAL',W),('VIBE CHECKER',W)],420),('M2-capitulate',[('I MODERATE',W),('SO YOU DON\'T',W),('CAPITULATE.',CY)],360),('M3-report-fud',[('REPORT FUD.',CY),('NOT',W),('FEELINGS.',W)],400)]:
    c=C(3600,4800,300); y=slogan_lines(c,1800,420,lines,size); c.lockup(1800,y+300,330,'NETWORK'); c.save(f'staff-mod__tee_back_{k}')
c=C(3600,4800,300); y=slogan_lines(c,1800,420,[('THE BUCK',W),('STOPS AT THE',W),('STOP LOSS.',CY)],380); c.lockup(1800,y+300,330,'MERCH'); c.save('staff-ceo__hoodie_back_buck')
c=C(3600,4800,300); y=slogan_lines(c,1800,420,[('CHIEF',W),('EXECUTIVE',W),('OFFICER',CY)],400); y+=200; c.tagline(1800,y,220); c.lockup(1800,y+1150,330,'MERCH'); c.save('staff-ceo__hoodie_back_crest')
c=C(3600,4800,300); y=slogan_lines(c,1800,420,[('FOUNDERS',CY),('EST. 2026',W)],420); y+=200; c.tagline(1800,y,220); c.lockup(1800,y+1150,330,'MERCH'); c.save('founders__hoodie_back')
# ---------- embroidery / hats / polos ----------
def emb(name,w,h,ppi,lines=None,sub=None,iconH=None):
    c=C(w,h,ppi)
    if sub: c.lockup(w/2,(h-iconH)/2,iconH,sub)
    else:
        ih=h*0.62; iw=43/51*ih; size=ih*0.38; tws=[width(t,'Bold',size) for t,_ in lines]; tw=iw+ih*0.18+max(tws)
        if tw>w*0.7: k=w*0.7/tw; ih*=k; iw*=k; size*=k; tw*=k
        x0=(w-tw)/2
        c.shield(x0,(h-ih)/2,ih); y=(h-ih)/2+ih*0.12
        for t,col in lines: y+=capH('Bold',size); c.text(t,'Bold',size,x0+iw+ih*0.18,y,col); y+=size*0.42
    c.save(name)
emb('polo__chest_lockup',1200,1200,300,sub='MERCH',iconH=190)
c=C(600,900,300); c.text('CEO','Bold',200,300,520,CY,track=0.15,anchor='c'); c.save('polo__sleeve_ceo')
emb('cso-hat__front',1650,600,300,lines=[('CSO',W)])
emb('verified-signal-hat__front',1650,600,300,lines=[('VERIFIED',W),('SIGNAL',CY)])
emb('rumor-control-hat__front',1650,600,300,lines=[('RUMOR',W),('CONTROL',CY)])
emb('stay-aware-hat__front',1650,600,300,lines=[('STAY',W),('AWARE',CY)])
emb('trucker__brutus-said-wait',1770,600,300,lines=[('BRUTUS SAID',W),('WAIT.',CY)])
emb('puff-hat__front_lockup',1650,600,300,sub='MERCH',iconH=420)
# ---------- mugs (2700x1050 canvas, Printful 300 area) ----------
def mug(name,lines,sub='MERCH',brutus=None,size=150):
    c=C(2700,1050,300)
    c.lockup(675,170,170,sub); c.tagline(675,460,95)
    x=2025; y=140
    if brutus: c.image(BRUTUS+brutus,x-180,90,360); y=520; size=110
    slogan_lines(c,x,y,lines,size,fitw=950)
    c.save(name)
mug('mug__coffee-before-charts',[('COFFEE',W),('BEFORE',CY),('CHARTS',CY)])
mug('mug__signal-over-noise',[('SIGNAL',W),('OVER',CY),('NOISE',CY)])
mug('mug__the-network-knows',[('THE',W),('NETWORK',W),('KNOWS.',CY)],'NETWORK')
mug('mug__coffee-before-consensus',[('COFFEE',W),('BEFORE',W),('CONSENSUS.',CY)],'NETWORK',size=140)
mug('mug__brutus-said-wait',[('BRUTUS SAID',W),('WAIT.',CY)],brutus='brutus-avatar.png')
mug('mug__market-opens-brutus-judges',[('MARKET OPENS.',W),('BRUTUS JUDGES.',CY)],brutus='brutus-shades-approved.webp')
mug('mug__shield-before-coffee',[('CHECK MY',W),('SHIELD BEFORE',CY),('MY COFFEE.',W)],size=130)
# ---------- straw tumbler 742 (3017x1200) ----------
c=C(3017,1200,300)
for cx in (754,2263): c.lockup(cx,200,190,'MERCH'); c.tagline(cx,560,105)
c.save('straw-tumbler__wrap')
# ---------- desk mats 853 (9921x5197 @ 310ppi ~ 32x16.8in) ----------
def mat(name,title,sub,brutus=None):
    c=C(9921,5197,310); c.el.append(f'<rect width="9921" height="5197" fill="{NV}"/>'); c.lockup(2300,1500,900,sub); c.tagline(2300,2900,330)
    if brutus: c.image(BRUTUS+brutus,6400,1100,2600)
    else: slogan_lines(c,7300,1700,[(t,col) for t,col in title],520,fitw=4200)
    c.text('tradeshieldlabs.com','Medium',170,9921-500,5197-300,CY,anchor='r'); c.save(name)
mat('desk-mat__brutus',None,'MERCH',brutus='brutus-shades-approved.webp')
mat('desk-mat__community-signal-command',[('COMMUNITY',W),('SIGNAL',W),('COMMAND',CY)],'NETWORK')
# ---------- journal 867 (4065x2850: back | front) ----------
c=C(4065,2850,300); c.el.append(f'<rect width="4065" height="2850" fill="{NV}"/>')
c.lockup(3050,800,330,'MERCH'); c.text('TRADE JOURNAL','Bold',200,3050,1500,CY,track=0.1,anchor='c'); c.tagline(3050,1750,150)
c.text('tradeshieldlabs.com','Medium',90,1016,2500,CY,anchor='c'); c.save('journal__cover')
# ---------- sticker sheet 505 (1750x2482) ----------
c=C(1750,2482,300)
for (x,y,w,h) in [(120,110,1510,380),(120,550,1510,380),(120,990,1510,560),(140,1610,640,760),(970,1610,640,760)]: c.el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="60" fill="{NV}"/>')
c.lockup(875,180,230,'MERCH'); c.lockup(875,620,230,'NETWORK'); c.tagline(875,1100,120)
c.image(BRUTUS+'brutus-thumbsup-approved.webp',180,1650,560); c.image(BRUTUS+'brutus-shades-approved.webp',1010,1650,560)
c.save('sticker-sheet')
for n in ['no-dumb-trades-hoodie__front','cso-hoodie__front','network-built-for-the-network-hoodie__front','network-network-intelligence-unit-hoodie__front','network-signal-crew-hoodie__front']:
    im=Image.open(f'{OUT}/{n}.png'); bb=im.getbbox(); art=im.crop(bb); k=min(3200/art.width,2550/art.height,1.0); print(n,"scale",round(k,2)); art=art.resize((int(art.width*k),int(art.height*k)),Image.LANCZOS)
    sq=Image.new('RGBA',(3600,3600),(0,0,0,0)); sq.alpha_composite(art,((3600-art.width)//2,1000)); sq.save(f'{OUT}/{n.replace("__front","__front_sq")}.png')

LOG_DONE=True
print(len(LOG),'files; min ™',min(min(v['tm_in']) for v in LOG.values() if v['tm_in']),'in')

# ---------- BOLD option B (approved 2026-10-11), same overall sizes as round 8 ----------
def lw(H,sub='MERCH'):
    c=C(100,100,300); return c._w8(H,sub,'TradeShield')
def Hfor(target): return 300*target/lw(300)
# left chest ~4in wide (1200px), canvas = full print area
c=C(3600,4800,300); H=Hfor(1200); c.lockup(3350,450,H,'MERCH',anchor='r'); c.save('bold__tee_front_LC')
c=C(3600,3600,300); H=Hfor(1200); c.lockup(3590,250,H,'MERCH',anchor='r')  # 78adf88: clear of drawstrings; c.save('bold__hoodie_front_LC')
# back ~11.5in wide lockup, big tagline
c=C(3600,4800,300); H=Hfor(3450); c.lockup(1800,350,H,'MERCH')
ts=420*min(1,3000/width('Learn Together.','SemiBold',420)); y=350+H+330; c.tagline(1800,y,ts)
c.text('tradeshieldlabs.com','Medium',150,1800,y+capH('SemiBold',ts)+2*ts*1.28+420,CY,anchor='c'); c.save('bold__back')
print({k:v for k,v in LOG.items() if k.startswith('bold')}, 'H',H)

json.dump(LOG,open(OUT+'/tm-log.json','w'),indent=1)
