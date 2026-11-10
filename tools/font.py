import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import numpy as np
EXE=_ROOT+'/orig/SLPM_871.78'; BASE=0xde5b0
_d=open(EXE,'rb').read()
PERM=[0,1,3,2,4,5,7,6,8,9,11,10,12,13,15,14]
NGLYPH=(len(_d)-BASE)//32
def glyph(code):
    o=BASE+code*32
    g=np.unpackbits(np.frombuffer(_d[o:o+32],np.uint8)).reshape(16,16)
    return g[:,PERM]
def sheet(start,n,cols,name,scale=3,label=True):
    from PIL import Image,ImageDraw
    rows=(n+cols-1)//cols; cw=20; ch=28
    img=Image.new('L',(cols*cw*scale,rows*ch*scale),255); dr=ImageDraw.Draw(img)
    for i in range(n):
        r,c=divmod(i,cols); g=glyph(start+i)
        gi=Image.fromarray(((1-g)*255).astype(np.uint8)).resize((16*scale,16*scale),Image.NEAREST)
        img.paste(gi,(c*cw*scale,r*ch*scale+10*scale))
        if label: dr.text((c*cw*scale,r*ch*scale),'%03x'%(start+i),fill=0)
    img.save(name)
