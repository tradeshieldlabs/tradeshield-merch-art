import os,json,time,urllib.request,urllib.error,glob
TOK=os.environ['PRINTFUL_API_TOKEN']; SHA='66166a76b68760959edbe53b042dcbbf9c8c601e'
RAW=f'https://raw.githubusercontent.com/tradeshieldlabs/tradeshield-merch-art/{SHA}/files/round10/'
OUT='/workspace/merch-design-r10/mockups'
H={'Authorization':'Bearer '+TOK,'X-PF-Store-Id':'18882949','Content-Type':'application/json','User-Agent':'curl/8'}
def api(path,body=None):
    r=urllib.request.Request('https://api.printful.com'+path,data=json.dumps(body).encode() if body else None,headers=H,method='POST' if body else 'GET')
    try: return json.load(urllib.request.urlopen(r,timeout=60))
    except urllib.error.HTTPError as e: raise RuntimeError(f'{e.code} {e.read().decode()[:300]}')
A={(586,'front'):(1800,2400),(586,'back'):(1800,2400),(586,'label_outside'):(450,450),(586,'sleeve_left'):(600,525),
 (380,'front'):(1800,1800),(380,'back'):(1800,2400),(380,'label_outside'):(450,450),(380,'sleeve_left'):(450,1800),
 (340,'embroidery_chest_left'):(1200,1200),(340,'embroidery_sleeve_right_top'):(600,900),(206,'embroidery_front_large'):(1650,600),(206,'embroidery_back'):(600,300),
 (422,'embroidery_front_large'):(1770,600),(300,'default'):(2250,925),(742,'default'):(3017,1200),(853,'default'):(9921,5197),(505,'default'):(1750,2482)}
def pos(pid,pl):
    w,h=A[(pid,pl)]
    if pid==300: hh=round(w*1050/2700); return dict(area_width=w,area_height=h,width=w,height=hh,top=(h-hh)//2,left=0)
    return dict(area_width=w,area_height=h,width=w,height=h,top=0,left=0)
TG=["Men's","Men's 2","Flat"]; HG=["Men's Lifestyle","Men's Lifestyle 2","Flat, Premium"]
J=[]
def tee(lab,v,**pl): J.append((lab,586,v,pl,TG,None))
def hood(lab,v,**pl): J.append((lab,380,v,pl,HG,None))
BK,IV,HB,HN=15116,16525,10781,11493
hood('founders-hoodie-A',HB,front='hoodie__chest_icon',label_outside='nape__wordmark',back='founders-A__back')
hood('founders-hoodie-B',HB,front='founders-B__front',label_outside='nape__icon')
tee('classic-tee-A',BK,front='tee__chest_word',label_outside='nape__icon')
tee('classic-tee-B',IV,front='tee__chest_icon',label_outside='nape__wordmark_navy',sleeve_left='tee__sleeve_word_navy')
hood('performance-hoodie',HN,front='hoodie__chest_icon_tonal',label_outside='nape__wordmark',sleeve_left='hoodie__sleeve_word')
tee('staff-admin-tee',BK,front='tee__chest_icon',label_outside='nape__wordmark',back='admin__back')
tee('staff-mod-tee',BK,front='tee__chest_icon',label_outside='nape__wordmark',back='mod__back')
tee('staff-ceo-tee',BK,front='tee__chest_icon',label_outside='nape__wordmark',back='ceo__back')
tee('humor-tee-A-zoom-out',BK,front='humor-zoom-out__front',label_outside='nape__icon')
tee('humor-tee-B-buy-high',BK,front='humor-buy-high__front',label_outside='nape__icon')
hood('ndt-hoodie-A',HB,front='ndt-A__front',label_outside='nape__icon',back='ndt-A__back')
hood('ndt-hoodie-B',HB,front='ndt-B__front',label_outside='nape__icon')
tee('brutus-objection-tee',BK,front='brutus-objection__front',label_outside='nape__icon')
hood('brutus-cso-hoodie',HB,front='hoodie__chest_icon',label_outside='nape__wordmark',back='brutus-cso__back')
J.append(('polo',340,9900,dict(embroidery_chest_left='polo__chest_icon'),None,None))
J.append(('ceo-polo',340,9900,dict(embroidery_chest_left='polo__chest_icon',embroidery_sleeve_right_top='polo__sleeve_ceo'),None,None))
J.append(('hat-A',206,7857,dict(embroidery_front_large='hat-A__front'),None,None))
J.append(('hat-B',206,7857,dict(embroidery_front_large='hat-B__front',embroidery_back='hat-B__back'),None,None))
J.append(('trucker-brutus',422,11417,dict(embroidery_front_large='trucker__front'),None,None))
for m in ['core-3am','core-coffee','core-moon','net-saw-it','net-groupchat','net-signal','brutus-objection','brutus-judge','brutus-cso','gen-candle','gen-long-coffee']:
    J.append(('mug-'+m,300,9323,dict(default='mug-'+m),None,["Handle on Left","Handle on Right"]))
for t in ['hedged','core-check','brutus-size','net-room']:
    J.append(('tumbler-'+t,742,19107,dict(default='tumbler-'+t),None,["Front","Back"]))
J.append(('desk-mat',853,22327,dict(default='desk-mat__chart'),None,None))
J.append(('sticker-sheet',505,12917,dict(default='sticker-sheet'),None,None))
import sys
only=sys.argv[1:]
print(len(J),'jobs',flush=True)
for lab,pid,v,pls,groups,opts in J:
    if only and lab not in only: continue
    d=f'{OUT}/{lab}'
    if glob.glob(d+'/*.jpg'): continue
    body={'variant_ids':[v],'format':'jpg','files':[dict(placement=p,image_url=RAW+f+'.png',position=pos(pid,p)) for p,f in pls.items()]}
    if groups: body['option_groups']=groups
    if opts: body['options']=opts
    t=None
    for _ in range(12):
        try: t=api(f'/mockup-generator/create-task/{pid}',body)['result']['task_key']; break
        except RuntimeError as e:
            if str(e).startswith('429'): time.sleep(62); continue
            print(lab,'FAIL',e,flush=True); break
        except Exception as e: print(lab,'ERR',e,flush=True); time.sleep(20)
    if not t: continue
    r={'status':'pending'}
    for _ in range(60):
        time.sleep(8)
        try: r=api(f'/mockup-generator/task?task_key={t}')['result']
        except Exception: continue
        if r['status']!='pending': break
    if r['status']!='completed': print(lab,'FAILED',r.get('status'),r.get('error'),flush=True); continue
    os.makedirs(d,exist_ok=True); n=0
    for m in r['mockups']:
        for e in [{'url':m['mockup_url'],'title':m.get('placement')}]+m.get('extra',[]):
            n+=1; name=(e.get('option_group','') or '')+'_'+(e.get('option','') or e.get('title','') or '')
            urllib.request.urlretrieve(e['url'],f'{d}/{n:02d}-{name.replace(" ","").replace("/","").replace(chr(39),"")[:40]}.jpg')
    print(lab,n,flush=True); time.sleep(8)
print('DONE',flush=True)
