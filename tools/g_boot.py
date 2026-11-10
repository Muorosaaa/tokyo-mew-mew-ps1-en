"""Boot warning screen (D_SYSTEM 055, 320x240 8bpp): ゲームをする時は お部屋を 明るくするにゃん!
-> "When you play, / keep your room / bright, nya!"

The Japanese lettering overlaps Ichigo's boot, so it is removed by colour/connectivity, the boot pixels under it are
filled from their neighbours, and the English is set left of her (x < 150) in a rounded font (M PLUS Rounded 1c,
OFL, data/fonts/) with white fill and pink rings like the original.
"""
import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0,_ROOT+'/tools')
from collections import Counter, deque
import numpy as np
import gedit
from gedit import text_block

gedit.FONTS['mpr']=_ROOT+'/data/fonts/MPLUSRounded1c-ExtraBold.ttf'
gedit.FONTS['mprb']=_ROOT+'/data/fonts/MPLUSRounded1c-Black.ttf'
GREEN=251
BANDS=((126,151),(153,178),(180,201))
LINES=['When you play,','keep your room','bright, nya!']

def label(full):
    H,W=full.shape; lab=np.zeros((H,W),int); n=0
    for y in range(H):
        for x in range(W):
            if full[y,x] and not lab[y,x]:
                n+=1; q=deque([(y,x)]); lab[y,x]=n
                while q:
                    a,b=q.popleft()
                    for da in (-1,0,1):
                        for db in (-1,0,1):
                            c,e=a+da,b+db
                            if 0<=c<H and 0<=e<W and full[c,e] and not lab[c,e]: lab[c,e]=n; q.append((c,e))
    return lab

def erase_mask(px,pal):
    lab=label(px!=GREEN)
    mask=np.zeros(px.shape,bool); merged=[]
    for y0,y1 in BANDS:
        for i in set(np.unique(lab[y0:y1,0:260]).tolist())-{0}:
            ys,xs=np.where(lab==i)
            if ys.min()>=y0-2 and ys.max()<=y1+1:      # a glyph on its own
                mask|=lab==i
            else: merged.append((i,y0,y1))
    # colours of the lettering (fill, outline, shadow, antialiasing): whatever the free-standing glyphs use
    T=set(np.unique(px[mask]).tolist())-{GREEN}
    inT=np.isin(px,list(T))
    rgb=np.array([c[:3] for c in pal],int)[px]; R,Gc,B=rgb[...,0],rgb[...,1],rgb[...,2]
    ys,xs=np.mgrid[0:px.shape[0],0:px.shape[1]]
    boot=np.zeros_like(mask)
    for i,y0,y1 in merged:
        comp=lab==i
        if comp.sum()<3000:                             # glyph touching a star: lettering colours only (stars are yellow)
            sel=comp&inT&(ys>=y0)&(ys<y1+3)
        elif y0==BANDS[0][0]:                           # Ichigo, line 1: は; its right stroke lies on the skirt (see SKIRT)
            sel=comp&inT&(ys>=y0)&(ys<y1)&((xs<176)|((xs<=185)&(ys>=144)))
        elif y0==BANDS[2][0]:                           # Ichigo, line 3: on the boot the lettering is light or green-tinted
            on=comp&(ys>=y0)&(ys<y1+3)
            sel=on&(xs<=205)&((B>=110)|(Gc>R)); boot|=sel
            sel|=on&(xs>205)&(xs<=240)&inT                # ん! right of the boot
        else: continue
        mask|=sel
    return mask,boot,(B<110)&~(Gc>R)

def inpaint(px,mask,boot,dark):
    """Removed lettering becomes background, except on the boot, where it is filled from the boot's own dark pixels."""
    px=px.copy(); px[mask&~boot]=GREEN; todo=boot.copy(); H,W=px.shape
    src=~mask&(dark|(px==GREEN))
    while todo.any():
        ys,xs=np.where(todo); done=[]
        for y,x in zip(ys,xs):
            c=Counter()
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    a,b=y+dy,x+dx
                    if (dy or dx) and 0<=a<H and 0<=b<W and src[a,b]: c[int(px[a,b])]+=1
            if sum(c.values())>=3: done.append((y,x,c.most_common(1)[0][0]))
        if not done:
            for y,x in zip(ys,xs): px[y,x]=GREEN
            break
        for y,x,v in done: px[y,x]=v; todo[y,x]=False; src[y,x]=True
    return px

SKIRT=(176,190,129,144)   # x0,x1,y0,y1: skirt under は's right stroke, refilled from the pleats 13 px to the right

def warn(G):
    px=G.px(0)
    m,boot,dark=erase_mask(px,G.pal(0))
    px=inpaint(px,m,boot,dark)
    x0,x1,y0,y1=SKIRT
    for y in range(126,144):                            # specks of は left of the skirt edge
        for x in range(160,int(round(178+(y-122)*0.68))): px[y,x]=GREEN
    for y in range(y0,y1):
        edge=int(round(178+(y-122)*0.68))              # the skirt's lower-left edge runs diagonally
        for x in range(x0,x1):
            px[y,x]=px[y,x+13] if x>=edge else GREEN
    pal=G.pal(0)
    for y in range(190,204):                            # last speck of the ! next to the right boot
        for x in range(206,241):
            if min(pal[px[y,x]][:3])>=200: px[y,x]=GREEN
    opts=[("mpr",s,0) for s in range(26,12,-1)]
    text_block(px,LINES,(4,127,152,200),opts,[232,232,233,234],rings=[(166,1),(168,2)],shadow=(58,1,1),gap=7)
    G.put(0,px)

JOBS={55:warn}
