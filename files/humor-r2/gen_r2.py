import sys,re; sys.path.insert(0,'/workspace/merch-humor/r2')
from tslib import *
RED='#EF4444'
BV='/workspace/brutus/v2/'
def brutus(c,name,x,y,w,crop):
    t=open(BV+name).read(); vb=[float(v) for v in re.search(r'viewBox="([^"]+)"',t).group(1).split()]
    inner=t[t.index('>',t.index('<svg'))+1:t.rindex('</svg>')]
    hc=vb[3]*crop; h=w*hc/vb[2]
    c.el.append(f'<svg x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" viewBox="0 0 {vb[2]} {hc}" overflow="hidden">{inner}</svg>'); return h
CROP={'brutus-thumbsup-approved.svg':0.615,'brutus-shades-chain-approved.svg':0.625,'brutus-cso-portrait.svg':0.72}
def R(c,x,y,w,h,fill,rx=0,stroke=None,sw=0,extra=''):
    c.el.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+f' {extra}/>')
def P(c,d,fill='none',stroke=None,sw=0,extra=''):
    c.el.append(f'<path d="{d}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else '')+f' {extra}/>')
def candle(c,x,yt,yb,wt,wb,w,col,sw):
    P(c,f'M{x} {wt}V{wb}',stroke=col,sw=sw); R(c,x-w/2,yt,w,yb-yt,col,rx=w*0.08)
def tee_front(name,draw,lines,size=400,foot=None):
    c=C(3600,4800,300); y=draw(c)
    y=slogan_lines(c,1800,y+90,lines,size,fitw=3000)
    if foot: y+=40; c.text(foot,'SemiBold',125,1800,y+150,WH,track=0.18,anchor='c'); y+=150
    c.lockup(1800,y+230,300,'MERCH'); fit_save(c,name)
def fit_save(c,name,tw=3150,maxh=4560):
    c.save(name); bb=Image.open(f'{OUT}/{name}.png').getbbox(); x0,y0,x1,y1=bb
    k=min(tw/(x1-x0),maxh/(y1-y0)); tx=1800-k*(x0+x1)/2; ty=120-k*y0
    c.el=[f'<g transform="translate({tx:.1f},{ty:.1f}) scale({k:.4f})">']+c.el+['</g>']; c.save(name)

# 1 Brutus Ate My Revenge Trade
def d1(c):
    h=brutus(c,'brutus-thumbsup-approved.svg',1800-850,300,1700,CROP['brutus-thumbsup-approved.svg'])
    # chewed order ticket in front of chin
    x0,y0,w,hh=1260,300+h-420,1080,640
    bites=''.join(f'a70 70 0 0 1 -140 0' for _ in range(3))
    d=f'M{x0} {y0+hh}V{y0+60}L{x0+90} {y0}H{x0+w-430}{bites}L{x0+w} {y0+80}V{y0+hh}Z'
    P(c,d,fill=WH,extra=f'transform="rotate(-7 {x0+w/2} {y0+hh/2})"')
    g=f'transform="rotate(-7 {x0+w/2} {y0+hh/2})"'
    c.el.append(f'<g {g}>')
    c.text('ORDER TICKET','Bold',70,x0+70,y0+190,NV,track=0.15)
    c.text('REVENGE TRADE','ExtraBold',105,x0+70,y0+340,RED)
    c.text('SIZE: 3X   STOP: NONE','SemiBold',62,x0+70,y0+450,NV,track=0.05)
    R(c,x0+60,y0+300,w-200,16,NV)
    c.text('STATUS: EATEN','Bold',62,x0+70,y0+560,AC,track=0.1)
    c.el.append('</g>')
    for i,(dx,dy) in enumerate([(-90,-40),(1170,40),(1120,-120)]): R(c,x0+dx,y0+hh+dy,46,28,WH,rx=8,extra=f'transform="rotate({30*i-20} {x0+dx} {y0+hh+dy})"')
    return 300+h+340
tee_front('brutus-ate-my-revenge-trade__front',d1,[('BRUTUS ATE MY',WH),('REVENGE TRADE.',CY)],380,foot='GOOD BOY. NO NOTES.')

# 2 Just A Pullback (Day 47)
def d2(c):
    x=520; top=380; ys=[]
    for i in range(9):
        yt=top+i*150; yb=yt+280; col=RED if i==8 else (CY if i%3==2 else WH)
        if i%3==2: yt2,yb2=yt+120,yt+220; candle(c,x+i*300,yt2,yb2,yt2-40,yb2+40,150,CY,22)
        else: candle(c,x+i*300,yt,yb,yt-60,yb+60,150,col,22)
    # little flag on last candle
    fx=x+8*300+120; fy=top+8*150-140
    P(c,f'M{fx} {fy+330}V{fy-60}',stroke=WH,sw=18); P(c,f'M{fx} {fy-60}h300l-60 70l60 70h-300z',fill=CY)
    c.text('DAY 47','ExtraBold',70,fx+40,fy+30,NV)
    for k in range(5): P(c,f'M{560+k*70} {2140}l0 -230',stroke=AC,sw=26)
    P(c,'M520 2110L900 1940',stroke=AC,sw=26)
    return 2200
tee_front('just-a-pullback-day-47__front',d2,[("IT'S JUST A",WH),('PULLBACK.',CY)],430,foot='(DAY 47)')

# 3 Sit. Stay. Don't Click Buy.
def d3(c):
    h=brutus(c,'brutus-shades-chain-approved.svg',1800-760,260,1520,CROP['brutus-shades-chain-approved.svg'])
    by=260+h+90
    R(c,1800-700,by,1400,380,'none',rx=190,stroke=CY,sw=34)
    c.text('BUY','ExtraBold',230,1800,by+190+capH('ExtraBold',230)/2,CY,anchor='c',track=0.1)
    # paw covering button corner
    px,py=2330,by+40
    for dx,dy,r in [(0,90,95),(-120,-30,48),(-40,-90,48),(60,-90,48),(140,-30,48)]: c.el.append(f'<circle cx="{px+dx}" cy="{py+dy}" r="{r}" fill="{WH}"/>')
    return by+380+60
tee_front('sit-stay-dont-click-buy__front',d3,[('SIT. STAY.',WH),("DON'T CLICK BUY.",CY)],360)
back_std('tee__back_std_r2')

# 4 Trucker: Good Dog. Bad Entry. (embroidery 1770x600, cyan/white/red threads)
c=C(1770,600,300); AQ='#3399FF'; TR='#CC3333'
c.shield(150,150,300,col=AQ)
slogan_lines(c,1000,95,[('GOOD DOG.',WH),('BAD ENTRY.',AQ)],190,lh=1.18,fitw=1250)
candle(c,1640,250,430,200,480,52,TR,14)
c.save('good-dog-bad-entry__trucker_front')

# mugs 2250x925 full wrap navy. left panel = joke, right = lockup + tagline
def mug(name,draw,lines,size=120):
    c=C(2250,925,300)
    c.el.append('<g transform="translate(150,40) scale(0.8)">'); draw(c); c.el.append('</g>')
    slogan_lines(c,560,520,lines,size,lh=1.12,fitw=640)
    c.lockup(1690,170,150,'MERCH'); c.tagline(1690,420,80); c.save(name)
def m1(c):
    P(c,'M140 200H980',stroke=WH,sw=10); c.text('MARKET FLOOR','SemiBold',34,150,180,WH,track=0.2)
    pts='M150 120L330 150L470 110L600 180L690 470'
    P(c,pts,stroke=CY,sw=16)
    # basement stairs
    P(c,'M690 470V540H770V500H850V460H930V420H990',stroke=AC,sw=10)
    for i,t in enumerate(['B1','B2','B3']): c.text(t,'Bold',40,520,300+i*80,AC)
    candle(c,700,400,500,380,520,40,RED,8)
mug('bought-the-dip-basement__mug',m1,[('BOUGHT THE DIP.',WH),('IT HAD A',CY),('BASEMENT.',CY)],90)
def m2(c):
    steps=[('DAY 1','SCALP'),('DAY 3','SWING'),('DAY 30','INVESTMENT'),('DAY 300','HEIRLOOM')]
    for i,(a,b) in enumerate(steps):
        y=130+i*95; c.text(a,'Bold',44,170,y,AC,track=0.08); c.text(b,'ExtraBold',56,400,y,RED if i==3 else WH)
    P(c,'M820 110L880 190L930 260L980 420',stroke=CY,sw=12)
mug('accidental-long-term-investor__mug',m2,[('ACCIDENTAL',WH),('LONG-TERM',CY),('INVESTOR.',CY)],90)

# stickers 4x4 (1200x1200) navy die w/ lockup + tagline
def sticker(name,draw,lines,size=120):
    c=C(1200,1200,300); R(c,30,30,1140,1140,NV,rx=150,stroke=CY,sw=14)
    y=draw(c)
    if lines: y=slogan_lines(c,600,y,lines,size,lh=1.12,fitw=960)
    c.lockup(600,y+40,105,'MERCH'); c.tagline(600,y+190,46,lh=1.3); c.save(name)
def s1(c):
    # heart made of a chart line with a dashed stop line under
    P(c,'M600 470C600 470 330 320 330 200C330 120 400 80 465 80C530 80 580 130 600 170C620 130 670 80 735 80C800 80 870 120 870 200C870 320 600 470 600 470Z',stroke=CY,sw=22)
    P(c,'M280 540H920',stroke=RED,sw=12,extra='stroke-dasharray="40 26"')
    c.text('STOP','Bold',40,925,530,RED,anchor='r'); return 600
sticker('emotional-support-stop-loss__sticker',s1,[('EMOTIONAL SUPPORT',WH),('STOP LOSS',CY)],100)
def s2(c):
    h=brutus(c,'brutus-shades-chain-approved.svg',600-260,70,520,CROP['brutus-shades-chain-approved.svg'])
    # bag at the side
    bx,by=1000,330
    P(c,f'M{bx-90} {by+150}Q{bx-120} {by+20} {bx-40} {by-20}L{bx-60} {by-70}H{bx+60}L{bx+40} {by-20}Q{bx+120} {by+20} {bx+90} {by+150}Z',fill=WH)
    c.text('BAG','ExtraBold',52,bx,by+100,NV,anchor='c')
    candle(c,200,by-40,by+80,by-80,by+110,40,RED,9)
    y=slogan_lines(c,600,70+h+30,[('DROP IT.',CY)],150)
    c.text('BRUTUS, ON YOUR BAGS','SemiBold',44,600,y+40,WH,track=0.15,anchor='c'); return y+60
sticker('drop-it-brutus__sticker',s2,[],110)
c=C(600,1050,300); R(c,0,0,600,1050,NV); c.el.append(f'<circle cx="300" cy="80" r="28" fill="none" stroke="{CY}" stroke-width="5"/>')
c.lockup(300,200,110,'MERCH'); slogan_lines(c,300,420,[('GOOD DOG.',WH),('BAD ENTRY.',CY)],80,fitw=480); c.text('tradeshieldlabs.com','Medium',34,300,980,CY,anchor='c'); c.save('good-dog-bad-entry__hangtag_front')
c=C(600,1050,300); R(c,0,0,600,1050,NV); c.el.append(f'<circle cx="300" cy="80" r="28" fill="none" stroke="{CY}" stroke-width="5"/>')
c.tagline(300,330,62,lh=1.4); c.rule(300,620,300,8); c.text('EMBROIDERED FOR TRADERS','SemiBold',26,300,720,WH,track=0.15,anchor='c'); c.text('WHO KNOW BETTER.','SemiBold',26,300,770,WH,track=0.15,anchor='c'); c.save('good-dog-bad-entry__hangtag_back')
json.dump(LOG,open(OUT+'/tm-log.json','w'),indent=1); print(json.dumps(LOG))
