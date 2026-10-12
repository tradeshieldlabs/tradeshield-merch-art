# Printful rejects outside-label + back print together, so the nape mark is merged into the top of the back file.
import re,cairosvg
def inner(f): s=open(f).read(); return re.search(r'<svg[^>]*>(.*)</svg>',s,re.S).group(1), re.search(r'<svg[^>]*>',s).group(0)
for back,nape,shift in [('founders-A__back','nape__wordmark',0),('admin__back','nape__wordmark',600),('mod__back','nape__wordmark',600),('ceo__back','nape__wordmark',600),('ndt-A__back','nape__icon',600),('brutus-cso__back','nape__wordmark',600),('ls__back_upper','nape__icon',500)]:
    b,head=inner(back+'.svg'); n,_=inner(nape+'.svg')
    top=-330 if 'wordmark' in nape else -150
    svg=head+f'<g transform="translate(1350,{top})">{n}</g><g transform="translate(0,{shift})">{b}</g></svg>'
    open(back+'_nape.svg','w').write(svg); cairosvg.svg2png(bytestring=svg.encode(),write_to=back+'_nape.png',output_width=3600,output_height=4800); print(back)
