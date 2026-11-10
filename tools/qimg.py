import struct,numpy as np
from PIL import Image
def entries(d):
    m,c=struct.unpack_from('<HH',d,0)
    return [dict(zip(('off','a','w','h','z'),struct.unpack_from('<IIHHI',d,4+i*16))) for i in range(c)]
def img4(d,e,pal=None):
    w,h=e['w'],e['h']; o=e['off']
    a=np.frombuffer(d[o:o+w*h//2],np.uint8)
    px=np.stack([a&15,a>>4],1).reshape(h,w)
    return px
def sheet(path,out,maxw=None):
    d=open(path,'rb').read(); E=entries(d)
    ims=[]
    for i,e in enumerate(E):
        if e['w']*e['h']>256*64: continue
        try: px=img4(d,e)
        except Exception: continue
        if px.size==0: continue
        ims.append((i,Image.fromarray((px*17).astype(np.uint8)).resize((px.shape[1]*2,px.shape[0]*2),Image.NEAREST)))
    if not ims: return
    W=max(im.width for _,im in ims)+40; H=sum(im.height+6 for _,im in ims)
    S=Image.new('L',(W,H),90); y=0
    from PIL import ImageDraw; dr=ImageDraw.Draw(S)
    for i,im in ims:
        dr.text((0,y),str(i),fill=255); S.paste(im,(30,y)); y+=im.height+6
    S.save(out)
