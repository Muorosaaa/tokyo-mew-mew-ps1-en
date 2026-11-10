import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,json,numpy as np
sys.path.insert(0,_ROOT+'/tools')
from font import glyph,NGLYPH
from PIL import Image,ImageDraw,ImageFont,ImageFilter
N=32
def norm(arr):
    ys,xs=np.nonzero(arr)
    if len(ys)==0: return None
    a=arr[ys.min():ys.max()+1, xs.min():xs.max()+1].astype(np.uint8)*255
    h,w=a.shape; s=max(h,w)
    pad=np.zeros((s,s),np.uint8); pad[(s-h)//2:(s-h)//2+h,(s-w)//2:(s-w)//2+w]=a
    im=Image.fromarray(pad).resize((N,N),Image.BILINEAR).filter(ImageFilter.GaussianBlur(1.2))
    v=np.asarray(im,np.float32).ravel(); v-=v.mean(); n=np.linalg.norm(v)
    return v/n if n else None
# candidate chars: JIS X 0208 full
cands=[]
for hi in list(range(0x81,0xa0))+list(range(0xe0,0xeb)):
    for lo in range(0x40,0xfd):
        if lo==0x7f: continue
        try: c=bytes([hi,lo]).decode('cp932')
        except: continue
        if len(c)==1 and not c.isspace(): cands.append(c)
cands=list(dict.fromkeys(cands))
fonts=[ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',14,index=0),
       ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',28,index=0)]
import glob
uni=glob.glob('/usr/share/fonts/**/unifont*.otf',recursive=True)+glob.glob('/usr/share/fonts/**/unifont*.ttf',recursive=True)
if uni: fonts.append(ImageFont.truetype(uni[0],16))
refs=[]
for f in fonts:
    M=[];C=[]
    for c in cands:
        im=Image.new('L',(40,40),0); ImageDraw.Draw(im).text((4,2),c,font=f,fill=255)
        a=np.asarray(im)>100
        v=norm(a)
        if v is not None: M.append(v);C.append(c)
    refs.append((np.array(M),C))
print('fonts',len(fonts),'cands',len(cands),file=sys.stderr)
out={}
for code in range(0,NGLYPH):
    v=norm(glyph(code))
    if v is None: continue
    scores={}
    for M,C in refs:
        s=M@v
        for idx in np.argsort(-s)[:5]:
            scores[C[idx]]=max(scores.get(C[idx],-1),float(s[idx]))
    best=sorted(scores.items(),key=lambda x:-x[1])[:4]
    out[code]=best
json.dump(out,open(_ROOT+'/data/match.json','w'),ensure_ascii=False)
