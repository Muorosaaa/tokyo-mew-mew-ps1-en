import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,json,numpy as np
sys.path.insert(0,_ROOT+'/tools')
from font import glyph,NGLYPH
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import distance_transform_edt as edt
cands=[]
for hi in list(range(0x82,0xa0))+list(range(0xe0,0xeb)):
    for lo in range(0x40,0xfd):
        try: c=bytes([hi,lo]).decode('cp932')
        except: continue
        if len(c)==1 and not c.isspace(): cands.append(c)
cands+=list('ー、。？！…「」・～')
cands=list(dict.fromkeys(cands))
S=20
def crop(a):
    ys,xs=np.nonzero(a)
    if len(ys)==0: return None
    return a[ys.min():ys.max()+1, xs.min():xs.max()+1]
def place(a):
    out=np.zeros((S,S),bool); h,w=a.shape
    if h>S or w>S: return None
    out[(S-h)//2:(S-h)//2+h,(S-w)//2:(S-w)//2+w]=a; return out
refs=[]
paths=['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc']
for p in paths[:1]:
  for size in (12,13):
    f=ImageFont.truetype(p,size,index=0)
    for c in cands:
        im=Image.new('1',(24,24),0); dr=ImageDraw.Draw(im); dr.fontmode='1'
        dr.text((2,0),c,font=f,fill=1)
        a=crop(np.array(im))
        if a is None: continue
        a=place(a)
        if a is None: continue
        refs.append((c,a,edt(~a)))
C=[r[0] for r in refs]; A=np.array([r[1] for r in refs]); D=np.array([r[2] for r in refs])
print(len(refs),file=sys.stderr)
out={}
for code in range(NGLYPH):
    g=crop(glyph(code).astype(bool))
    if g is None: continue
    g=place(g)
    if g is None: continue
    gd=edt(~g)
    # symmetric chamfer distance
    d1=(D*g).sum((1,2))/max(g.sum(),1)
    d2=(A*gd).sum((1,2))/A.sum((1,2)).clip(1)
    s=-(d1+d2)
    idx=np.argsort(-s)
    best=[];seen=set()
    for i in idx:
        if C[i] in seen: continue
        seen.add(C[i]); best.append((C[i],round(float(s[i]),3)))
        if len(best)==5: break
    out[code]=best
json.dump(out,open(_ROOT+'/data/match2.json','w'),ensure_ascii=False)
