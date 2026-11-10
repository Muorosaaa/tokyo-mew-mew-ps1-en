import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,struct,numpy as np; sys.path.insert(0,_ROOT+'/tools')
from gfx import parse,palettes,image
from PIL import Image,ImageDraw,ImageFont
FONTS={'dvo':'/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf','dvcr':'/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf','dv':'/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','dvc':'/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf','bold':'/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf','black':'/usr/share/fonts/truetype/google-fonts/Poppins-Black.ttf','xb':'/usr/share/fonts/truetype/google-fonts/Poppins-ExtraBold.ttf','semi':'/usr/share/fonts/truetype/google-fonts/Poppins-SemiBold.ttf','med':'/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'}
class Gfx:
    def __init__(s,path,data=None):
        s.path=path; s.d=bytearray(data if data is not None else open(path,'rb').read()); s.m,s.E=parse(bytes(s.d)); s.pals,_=palettes(bytes(s.d),s.m,s.E)
    def px(s,i): return image(bytes(s.d),s.m,s.E[i],s.pals)[0].copy()
    def put(s,i,px):
        e=s.E[i]; w,h=e['w'],e['h']; assert px.shape==(h,w)
        if s.m&0xff==0x71:
            p=px.reshape(-1,2).astype(np.uint8); b=(p[:,0]|(p[:,1]<<4)).astype(np.uint8)
            s.d[e['off']:e['off']+w*h//2]=b.tobytes()
        else: s.d[e['off']:e['off']+w*h]=px.astype(np.uint8).tobytes()
    def pal(s,i): return s.pals[s.E[i]['a'][0]] if s.m&0xff==0x71 else s.pals[0]
def textmask(text,font='bold',size=11,track=0,maxw=None):
    f=ImageFont.truetype(FONTS[font],size)
    W=sum(f.getbbox(c)[2] if c!=' ' else size//3 for c in text)+track*len(text)+20
    im=Image.new('1',(W,size*2),0); dr=ImageDraw.Draw(im); dr.fontmode='1'
    x=2
    for c in text:
        dr.text((x,0),c,font=f,fill=1)
        x+=(f.getlength(c))+track
    a=np.array(im,bool)
    ys=np.where(a.any(1))[0]; xs=np.where(a.any(0))[0]
    return a[ys[0]:ys[-1]+1,xs[0]:xs[-1]+1]
def fit_mask(text,maxw,maxh,font='bold',sizes=range(20,6,-1),track=0):
    for sz in sizes:
        for tr in (track,track-1) if track>=0 else (track,):
            m=textmask(text,font,sz,tr)
            if m.shape[1]<=maxw and m.shape[0]<=maxh: return m
    m=textmask(text,font,min(sizes) if not isinstance(sizes,range) else sizes[-1],-1)
    return m
def dilate(m,diag=True):
    o=m.copy()
    h,w=m.shape
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if not diag and dx and dy: continue
            sh=np.zeros_like(m); 
            ys=slice(max(dy,0),h+min(dy,0)); yd=slice(max(-dy,0),h+min(-dy,0))
            xs=slice(max(dx,0),w+min(dx,0)); xd=slice(max(-dx,0),w+min(-dx,0))
            sh[ys,xs]=m[yd,xd]; o|=sh
    return o
def stamp(px,mask,x0,y0,fill_rows,outline=None,shadow=None,diag=True,pad=1):
    """fill_rows: list of indices per mask row (stretched); outline index; shadow (index,dx,dy)"""
    h,w=mask.shape
    big=np.zeros((h+2*pad+2,w+2*pad+2),bool); big[pad:pad+h,pad:pad+w]=mask
    X=x0-pad; Y=y0-pad
    def put(mm,val):
        ys,xs=np.where(mm)
        for y,x in zip(ys,xs):
            yy,xx=Y+y,X+x
            if 0<=yy<px.shape[0] and 0<=xx<px.shape[1]:
                px[yy,xx]=val(y-pad) if callable(val) else val
    if shadow is not None:
        si,dx,dy=shadow; sm=np.zeros_like(big); sm[dy:,dx:]=dilate(big,diag)[:big.shape[0]-dy,:big.shape[1]-dx] if outline is not None else big[:big.shape[0]-dy,:big.shape[1]-dx]; put(sm,si)
    if outline is not None: put(dilate(big,diag),outline)
    put(big,lambda r: fill_rows[min(len(fill_rows)-1,max(0,int(r*len(fill_rows)/max(1,h))))])
    return px
def rowfill(px,x0,x1,ignore=()):
    from collections import Counter
    for y in range(px.shape[0]):
        c=Counter(int(v) for v in px[y,x0:x1] if int(v) not in ignore)
        if c: px[y,x0:x1]=c.most_common(1)[0][0]
    return px
def preview(G,idxs,path,scale=5):
    ims=[]
    for i in idxs:
        px=G.px(i); pal=G.pal(i)
        lut=np.array([p[:3] for p in pal]+[(0,0,0)]*(256-len(pal)),np.uint8)
        ims.append(Image.fromarray(lut[px]).resize((px.shape[1]*scale,px.shape[0]*scale),Image.NEAREST))
    W=max(i.width for i in ims); H=sum(i.height+6 for i in ims)
    S=Image.new('RGB',(W,H),(30,30,50)); y=0
    for i in ims: S.paste(i,(0,y)); y+=i.height+6
    S.save(path)
def hmask(text,cap=8,font='xb',maxw=None,thr=0.5,space=0.32,track=0.04,minsx=0.7):
    """render text so that capital height == cap pixels; descenders extra. horizontal squeeze to fit maxw"""
    S=8; f=ImageFont.truetype(FONTS[font],200)
    capH=f.getbbox('H')[3]-f.getbbox('H')[1]
    asc=f.getbbox('H')[1]
    W=int(f.getlength(text)*1.2)+400
    im=Image.new('L',(W,320),0); dr=ImageDraw.Draw(im)
    x=50
    for c in text:
        if c==' ': x+=200*space; continue
        dr.text((x,20),c,font=f,fill=255); x+=f.getlength(c)+200*track
    a=np.array(im)
    ys=np.where(a.max(1)>0)[0]; xs=np.where(a.max(0)>0)[0]
    top=20+asc  # cap top
    a=a[:,xs[0]:xs[-1]+1]
    scale=cap/capH
    neww=max(1,round(a.shape[1]*scale)); 
    if maxw and neww>maxw:
        sx=max(minsx,maxw/neww); neww=max(1,round(neww*sx))
    newh=round(a.shape[0]*scale)
    small=np.array(Image.fromarray(a).resize((neww,newh),Image.BOX))/255.0
    m=small>=thr
    ys=np.where(m.any(1))[0]
    return m[ys[0]:ys[-1]+1]

def label(text,maxw,maxh,sizes=(12,11,10,9,8),fonts=('dv','dvc')):
    for sz in sizes:
        for fn in fonts:
            for tr in (0,-1):
                m=textmask(text,fn,sz,tr)
                if m.shape[1]<=maxw and m.shape[0]<=maxh: return m
    return textmask(text,fonts[-1],sizes[-1],-1)
def tmask(text,font='dv',size=11,track=0):
    """returns (mask, captop_row) mask rows cover [top of tallest glyph .. bottom of descenders]; captop = row index where cap height starts"""
    f=ImageFont.truetype(FONTS[font],size)
    asc,desc=f.getmetrics()
    W=int(f.getlength(text))+track*len(text)+20
    im=Image.new('1',(W,asc+desc+4),0); dr=ImageDraw.Draw(im); dr.fontmode='1'
    x=2
    for c in text:
        dr.text((x,2),c,font=f,fill=1); x+=f.getlength(c)+track
    a=np.array(im,bool)
    capt=2+f.getbbox('H')[1]; base=2+asc
    xs=np.where(a.any(0))[0]; a=a[:,xs[0]:xs[-1]+1]
    ys=np.where(a.any(1))[0]
    top=min(ys[0],capt)
    return a[top:ys[-1]+1], capt-top, base-capt
def label2(text,maxw,opts=(('dv',11,0),('dvc',11,0),('dv',10,0),('dvc',10,0),('dvc',9,0),('dvc',8,0),('dvc',8,-1))):
    for fn,sz,tr in opts:
        m=tmask(text,fn,sz,tr)
        if m[0].shape[1]<=maxw: return m
    return m
def place(px,text,x0,x1,captop,fill_rows,outline=None,shadow=None,opts=None,diag=True,align='c'):
    m,ct,caph=label2(text,x1-x0,opts) if opts else label2(text,x1-x0)
    w=m.shape[1]
    x=x0+(x1-x0-w)//2 if align=='c' else x0
    rows=[fill_rows[min(len(fill_rows)-1,max(0,int((r-ct)*len(fill_rows)/max(1,caph))))] for r in range(m.shape[0])]
    stamp(px,m,x,captop-ct,rows,outline,shadow,diag)
    return w
def dil(m,n,diag=True):
    for _ in range(n): m=dilate(m,diag)
    return m
def render(px,mask,x,y,fill_rows,rings=(),shadow=None,diag=True):
    """rings: list of (index, radius) applied outermost first; shadow=(index,dx,dy) of the outermost shape"""
    h,w=mask.shape; P=8
    big=np.zeros((h+2*P,w+2*P),bool); big[P:P+h,P:P+w]=mask
    X=x-P; Y=y-P; H,W=px.shape
    def put(mm,val):
        ys,xs=np.where(mm)
        for yy,xx in zip(ys,xs):
            a,b=Y+yy,X+xx
            if 0<=a<H and 0<=b<W: px[a,b]=val(yy-P) if callable(val) else val
    rmax=max([r for _,r in rings],default=0)
    if shadow:
        si,dx,dy=shadow; o=dil(big,rmax,diag); s=np.zeros_like(o); s[dy:,dx:]=o[:o.shape[0]-dy,:o.shape[1]-dx]; put(s&~o,si)
    for idx,r in sorted(rings,key=lambda t:-t[1]): put(dil(big,r,diag),idx)
    put(big,lambda r: fill_rows[min(len(fill_rows)-1,max(0,r))])
    return px
def lines_mask(lines,maxw,maxh,opts,gap=1):
    """try options (font,size,track) until all lines fit in maxw and total height<=maxh; returns list of (mask,captop,caph)"""
    for fn,sz,tr in opts:
        ms=[tmask(t,fn,sz,tr) for t in lines]
        if max(m[0].shape[1] for m in ms)<=maxw:
            caph=ms[0][2]; tot=caph*len(lines)+gap*(len(lines)-1)
            if tot<=maxh: return ms,caph
    return ms,ms[0][2]
def text_block(px,lines,box,opts,fill,rings=(),shadow=None,gap=2,diag=True,valign='c',bold=0):
    """box=(x0,y0,x1,y1) area for cap-height-aligned text (descenders may go below)"""
    x0,y0,x1,y1=box; ms,caph=lines_mask(lines,x1-x0-(bold or 0),y1-y0,opts,gap)
    if bold and caph<10: bold=0
    tot=caph*len(ms)+gap*(len(ms)-1)
    cy=y0+((y1-y0)-tot)//2 if valign=='c' else y0
    for (m,ct,ch) in ms:
        fr=[fill[min(len(fill)-1,max(0,int((r-ct)*len(fill)/max(1,ch))))] for r in range(m.shape[0])]
        x=x0+((x1-x0)-m.shape[1])//2
        if bold:
            mm=np.zeros((m.shape[0],m.shape[1]+bold),bool)
            for k in range(bold+1): mm[:,k:k+m.shape[1]]|=m
            m=mm
        render(px,m,x,cy-ct,fr,rings,shadow,diag); cy+=caph+gap
    return caph
def auto_style(px,bg=0):
    from collections import Counter
    nz=px!=bg
    if not nz.any(): return None
    edge=nz & dilate(~nz,False)
    oc=Counter(px[edge].tolist()).most_common(1)[0][0]
    inner=nz&~edge
    ys=np.where(nz.any(1))[0]; xs=np.where(nz.any(0))[0]
    rows=[]
    for y in range(ys[0],ys[-1]+1):
        c=Counter(px[y][inner[y]].tolist())
        c.pop(oc,None)
        if c: rows.append(c.most_common(1)[0][0])
    if not rows: rows=[oc]
    return dict(fill=rows,outline=oc,box=(xs[0],ys[0],xs[-1]+1,ys[-1]+1))
def relabel(px,text,opts,bg=0,align=None,pad=1,bold=0):
    st=auto_style(px,bg)
    h,w=px.shape
    px[:,:]=bg
    x0,y0,x1,y1=st['box']
    al=align or ('l' if x0<=2 and w>40 else 'c')
    ms,caph=lines_mask([text],w-2*pad-2,h-2,opts)
    m,ct,ch=ms[0]
    if bold and caph>=9:
        mm=np.zeros((m.shape[0],m.shape[1]+1),bool); mm[:,:-1]|=m; mm[:,1:]|=m; m=mm
    fill=st['fill']
    # trim outline-ish rows from fill list ends
    fr=[fill[min(len(fill)-1,max(0,int((r-ct)*len(fill)/max(1,ch))))] for r in range(m.shape[0])]
    x=pad+1 if al=='l' else (w-m.shape[1])//2
    y=(h-caph)//2-ct
    if m.shape[0]-ct>caph: y=max(1-ct, (h-(m.shape[0]-ct)) //2 - ct) if False else (h-caph)//2-ct
    render(px,m,x,y,fr,rings=[(st['outline'],1)])
    return px
