import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0,_ROOT+'/tools')
from gedit import *
from PIL import Image,ImageDraw,ImageFont
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf'
def sfx_mask(text,maxw,maxh,shear=0.25):
    f=ImageFont.truetype(FONT,200)
    W=int(f.getlength(text))+200; im=Image.new('L',(W,300),0); dr=ImageDraw.Draw(im)
    dr.text((60,20),text,font=f,fill=255)
    im=im.transform(im.size,Image.AFFINE,(1,shear,-shear*150,0,1,0),Image.BICUBIC)
    a=np.array(im); ys=np.where(a.max(1)>0)[0]; xs=np.where(a.max(0)>0)[0]
    a=a[ys[0]:ys[-1]+1,xs[0]:xs[-1]+1]
    sx=maxw/a.shape[1]; sy=min(maxh/a.shape[0], sx*2.2)
    sm=Image.fromarray(a).resize((max(1,round(a.shape[1]*sx)),max(1,round(a.shape[0]*sy))),Image.BOX)
    sm=sm.rotate(8,resample=Image.BICUBIC,expand=True)
    sm=np.array(sm); ys=np.where(sm.max(1)>0)[0]; xs=np.where(sm.max(0)>0)[0]; sm=sm[ys[0]:ys[-1]+1,xs[0]:xs[-1]+1]
    if sm.shape[0]>maxh or sm.shape[1]>maxw:
        k=min(maxh/sm.shape[0],maxw/sm.shape[1]); sm=np.array(Image.fromarray(sm).resize((int(sm.shape[1]*k),int(sm.shape[0]*k)),Image.BOX))
    return sm>=110
def ramp(pal):
    idx=[k for k in range(1,16) if pal[k][3]]
    lum=lambda k: 0.3*pal[k][0]+0.59*pal[k][1]+0.11*pal[k][2]
    idx.sort(key=lum,reverse=True)
    return idx
def draw(G,i,text):
    px=G.px(i); h,w=px.shape; pal=G.pal(i); R=ramp(pal)
    px[:,:]=0
    m=sfx_mask(text,w-6,int(h*0.82))
    fill=R[:max(3,len(R)*2//3)]
    outline=R[-1]; mid=R[len(R)*3//4]
    y0=(h-m.shape[0])//2; x0=(w-m.shape[1])//2
    rows=[fill[min(len(fill)-1,int(r*len(fill)/m.shape[0]))] for r in range(m.shape[0])]
    render(px,m,x0,y0,rows,rings=[(mid,1),(outline,2)])
    # highlight: top pixel of each column inside the letter
    for x in range(m.shape[1]):
        col=np.where(m[:,x])[0]
        if len(col): px[y0+col[0],x0+x]=R[0]
    G.put(i,px)
POC={12:'WHAM!',15:'BAM!',33:'SLASH!',19:'BOOM!',21:'CLANG!',18:'DASH!'}
def job(i):
    return lambda G: draw(G,0,POC[i])
JOBS={i:job(i) for i in POC}
