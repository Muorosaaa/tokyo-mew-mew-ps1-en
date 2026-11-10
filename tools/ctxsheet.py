import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,json,re
sys.path.insert(0,_ROOT+'/tools')
from font import glyph
from PIL import Image,ImageDraw,ImageFont
import numpy as np
hira="ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろわをん"
kata="ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロワヲンヴヵヶ"
d=open(_ROOT+'/orig/D_SCE.BIN','rb').read()
# gather lines as code lists
lines=[];i=0;cur=[]
while i<len(d)-1:
    b=d[i]
    if 0xf1<=b<=0xf9:
        cur.append((b-0xf1)*256+d[i+1]); i+=2; continue
    if b==0xfd and cur: cur.append(-1); i+=1; continue
    if len(cur)>=3: lines.append(cur)
    cur=[]; i+=1
ctx={}
for L in lines:
    for c in set(L):
        if 0x100<=c<0x64e and len(ctx.setdefault(c,[]))<2 and L not in ctx[c]: ctx[c].append(L)
used=sorted(ctx)
def render_line(L,hl,sc=2):
    L=[c for c in L if c!=-1][:34]
    im=np.full((16,16*len(L)),255,np.uint8)
    for k,c in enumerate(L):
        if 0<=c<0x64e: im[:,k*16:k*16+16]=(1-glyph(c))*255
        if c==hl: im[:,k*16:k*16+16]=np.where(im[:,k*16:k*16+16]==0,0,200)
    return Image.fromarray(im).resize((16*len(L)*sc,16*sc),Image.NEAREST)
def make(codes,name):
    W=1300; rh=80
    img=Image.new('L',(W,rh*len(codes)),255); dr=ImageDraw.Draw(img)
    f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',14)
    for r,c in enumerate(codes):
        y=r*rh
        dr.text((0,y+20),'%03x'%c,fill=0,font=f)
        g=Image.fromarray(((1-glyph(c))*255).astype(np.uint8)).resize((64,64),Image.NEAREST)
        img.paste(g,(40,y+4))
        for k,L in enumerate(ctx[c][:2]):
            img.paste(render_line(L,c),(120,y+4+k*36))
        dr.line((0,y+rh-1,W,y+rh-1),fill=180)
    img.save(name)
if __name__=='__main__':
    lo,hi=int(sys.argv[1],16),int(sys.argv[2],16)
    codes=[c for c in used if lo<=c<hi]
    for k in range(0,len(codes),16):
        make(codes[k:k+16],_ROOT+'/img/c_%03x.png'%codes[k]); print('%03x'%codes[k],len(codes[k:k+16]))
