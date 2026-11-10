import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,os; sys.path.insert(0,_ROOT+'/tools')
from gfx import *
import numpy as np
def is_tile(px):
    fr=(px!=0).mean()
    return 0.12<fr<0.75 and len(set(px.ravel().tolist()))<=16
def scan(lo=0,hi=700):
    out={}
    for f in sorted(os.listdir(_ROOT+'/dec/D_EFFECT')):
        n=int(f[:3])
        if not lo<=n<hi: continue
        d=open(_ROOT+'/dec/D_EFFECT/'+f,'rb').read()
        try: m,E=parse(d); pals,_=palettes(d,m,E)
        except Exception: continue
        if not pals or m&0xff!=0x71: continue
        T=[]
        for e in E:
            if not(14<=e['w']<=64 and 20<=e['h']<=72): continue
            try: r=image(d,m,e,pals)
            except Exception: continue
            if r is None or not is_tile(r[0]): continue
            pal=pals[e['a'][0]] if e['a'][0]<len(pals) else pals[0]
            bg=pal[0][:3]
            # tile bg must be a vivid flat color (kana tiles) not the grey-green sprite bg
            if bg in ((96,144,128),(88,136,120)) : continue
            T.append(dict(i=e['i'],w=e['w'],h=e['h'],pal=e['a'][0],px=r[0],rgb=r[1],bg=bg))
        if T: out[n]=T
    return out
def groups(T):
    G=[];cur=[]
    for t in T:
        if cur and (t['pal']!=cur[-1]['pal'] or t['i']!=cur[-1]['i']+1 and t['i']-cur[-1]['i']>1): G.append(cur);cur=[]
        cur.append(t)
    if cur: G.append(cur)
    return G
def key(px):
    from PIL import Image
    m=(px!=0).astype(np.uint8)*255
    s=np.array(Image.fromarray(m).resize((10,14),Image.BOX))>100
    return s
