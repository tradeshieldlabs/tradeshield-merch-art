# Round 10 add-on: long sleeve, kids line, beanie, tote.
s=open('/workspace/merch-design-r10/src/gen10.py').read(); exec(s[:s.index('# ---------- shared small marks')])
import os; LOGF='/workspace/merch-design-r10/art/_log_b.json'
def coin(c,cx,cy,r,col=CY,fg=NV):
    raw(c,f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/><circle cx="{cx}" cy="{cy}" r="{r*0.72}" fill="none" stroke="{fg}" stroke-width="{r*0.1}"/>')
    c.text('$','ExtraBold',r*1.0,cx,cy+capH('ExtraBold',r)/2,fg,anchor='c')
# ---- LONG SLEEVE (WWE-style: big front graphic, small upper-back hit, nape mark)
c=C(3600,4800,300)
c.text('WAIT FOR','ExtraBold',520,1800,600+capH('ExtraBold',520),W,anchor='c')
c.text('THE SETUP.','ExtraBold',520,1800,1250+capH('ExtraBold',520),CY,anchor='c')
candles(c,300,2200,3000,1300,n=40,seed=17,trend=0.4)
raw(c,f'<rect x="300" y="3600" width="3000" height="10" fill="{W}"/>'); save(c,'ls__front','front 12x16in')
c=C(3600,4800,300); s2=wsize(4.0); word(c,1800,250+capH('SemiBold',s2),s2,W); save(c,'ls__back_upper','back upper hit 4in','WWE-style small upper-back logo')
c=C(900,3600,300); candles(c,150,200,600,3200,n=14,seed=9,trend=1.5)
save(c,'ls__sleeve_chart','sleeve 3x12in','vertical candle strip')
# ---- KIDS (navy art on light garments; cyan accents; no gambling/real-money trading)
c=C(3000,3600,300)  # youth tee
h=c.image(B+'thumbs.png',700,250,1600)
c.text('LITTLE SAVER','ExtraBold',330,1500,250+h+150+capH('ExtraBold',330),NV,anchor='c')
for i,x in enumerate([1050,1500,1950]):
    for j in range(i+1): coin(c,x,250+h+900-j*170,120)
c.text('save a little, grow a lot.','SemiBold',150,1500,250+h+1250,NV,anchor='c')
save(c,'kids-youth__front','youth front 10x12in','raster Brutus')
c=C(2100,2400,300)  # toddler tee: jar
c.text("I'M SAVING UP","ExtraBold",190,1050,300,NV,anchor='c'); c.text('FOR SNACKS.','ExtraBold',190,1050,520,NV,anchor='c')
raw(c,f'<rect x="650" y="800" width="800" height="1050" rx="120" fill="none" stroke="{NV}" stroke-width="40"/><rect x="760" y="700" width="580" height="130" rx="30" fill="{NV}"/>')
for j,(x,y) in enumerate([(850,1680),(1050,1700),(1250,1680),(950,1500),(1150,1510),(1050,1330)]): coin(c,x,y,95)
save(c,'kids-toddler__front','toddler front 7x8in')
c=C(2100,2400,300)  # onesie
c.text('TINY','ExtraBold',330,1050,700,NV,anchor='c'); c.text('BUT','ExtraBold',330,1050,1100,NV,anchor='c'); c.text('COMPOUNDING.','ExtraBold',220,1050,1480,NV,anchor='c')
raw(c,f'<path d="M500 2050 Q1050 2040 1600 1650" fill="none" stroke="{CY}" stroke-width="40" stroke-linecap="round"/>')
save(c,'kids-onesie__front','onesie front 7x8in')
c=C(3300,3300,300)  # kids hoodie on navy
for i,(lab,x) in enumerate([('COUNT',650),('SAVE',1650),('GROW',2650)]):
    if i==0: coin(c,x,900,330,CY)
    if i==1: raw(c,f'<rect x="{x-300}" y="650" width="600" height="560" rx="90" fill="none" stroke="{W}" stroke-width="36"/>'); coin(c,x,950,160)
    if i==2: raw(c,f'<path d="M{x} 1250 V780 M{x} 900 Q{x-250} 820 {x-280} 600 Q{x-40} 620 {x} 900 M{x} 820 Q{x+260} 720 {x+300} 520 Q{x+40} 540 {x} 820" fill="none" stroke="{CY}" stroke-width="40" stroke-linecap="round" stroke-linejoin="round"/>')
    c.text(lab,'ExtraBold',190,x,1600,W,anchor='c',track=0.08)
c.text('learning money, one coin at a time.','SemiBold',130,1650,1950,CY,anchor='c'); save(c,'kids-hoodie__front','kids hoodie front 11x11in')
c=C(3000,3600,300); icon(c,1500,150,360,CY); save(c,'kids__back_nape','back top (kids blanks lack outside-label)','icon 1.0in')
# ---- BEANIE, TOTE
c=C(1500,525,300); icon(c,750,30,465,CY); save(c,'beanie__front','embroidery_front 5x1.75in','icon 1.31in w')
c=C(3000,3000,300); candles(c,250,400,2500,1900,n=22,seed=31,trend=1.3); word(c,1500,2700,wsize(3.0),W); save(c,'tote__front','tote front 10x10in')
json.dump(dict(LOG=LOG,INFO=INFO),open(LOGF,'w'),indent=1); print(len(INFO))
