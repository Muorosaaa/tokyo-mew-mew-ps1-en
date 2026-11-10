"""Title logo (D_SYSTEM 001, 320x236 8bpp): the 東京ミュウミュウ logo stays (it already carries "TOKYO MEW MEW");
only the ribbon underneath is translated (user's choice, 2026-11-08):
  登場新ミュウミュウ！          -> "Here Comes the New Mew Mew!"   (upper band)
  みんないっしょにご奉仕するにゃん♥ -> "We'll All Be at Your Service, Nya" + the original heart (lower band, follows its curve)
The Japanese is erased by refilling each column of the band from the band pixels above and below it (the bands are
shaded top to bottom), then the English is drawn with the original light fill and a deep-red outline.
"""
import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0,_ROOT+'/tools')
import numpy as np
from gedit import *

UPPER=dict(x0=84,x1=232,y0=112,y1=133,text=(88,118,229,131),line='Here Comes the New Mew Mew!')
LOWER=dict(x0=48,x1=248,y0=133,y1=157,line="We'll All Be at Your Service, Nya")   # ん ends at x 247, touching the heart (kept, see _heart)
FILL=[244,244,244,247]; OUTLINE=113

def _rgb(pal): return np.array([c[:3] for c in pal],int)

def _light(rgb): return (rgb[...,0]>=200)&(rgb[...,1]>=150)&(rgb[...,2]>=150)

def _band(px):
    """pixels inside the ribbon: not transparent and not the yellow border"""
    return px!=0

def _heart(P):
    """the original pink heart after にゃん: light pixels from x 246 on, minus ん's tail (x<=246, y>=142)"""
    L=_light(P); h=np.zeros_like(L)
    h[133:150,246:266]=L[133:150,246:266]; h[142:150,246]=False
    return h

def erase(px,pal,x0,x1,y0,y1):
    rgb=_rgb(pal); P=rgb[px]
    yellow=(P[...,2]<40)&(P[...,0]>140)&(P[...,1]>140)
    text=_light(P); text[:y0]=False; text[y1:]=False; text[:,:x0]=False; text[:,x1:]=False
    m=dil(text,1)                                          # light fill + its 1 px outline
    m&=(px!=0)&~yellow
    m&=~dil(_heart(P),1)
    used=sorted(set(px[y0:y1,x0:x1][~m[y0:y1,x0:x1]].tolist())-{0})
    U=rgb[used]; ok=~m&(px!=0)&~yellow
    for y in range(y0,y1):                                 # the bands are shaded by row: refill from the same row
        for x in range(x0,x1):
            if not m[y,x]: continue
            for r in (6,10,16,24):
                xs=[xx for xx in range(max(0,x-r),min(px.shape[1],x+r+1)) if ok[y,xx]]
                if len(xs)>=3: break
            if not xs: continue
            c=np.median(P[y,xs],0)
            px[y,x]=used[int(((U-c)**2).sum(1).argmin())]
    return px

def _curve(px,pal,x0,x1,y0,y1):
    """where the Japanese line ran: a parabola through the per-column centre of its light pixels"""
    L=_light(_rgb(pal)[px])
    xs=[];ys=[]
    for x in range(x0,x1):
        yy=np.where(L[y0:y1,x])[0]
        if len(yy): xs.append(x); ys.append(y0+yy.mean())
    k=np.polyfit(xs,ys,2)
    return lambda x: float(np.polyval(k,x))

def draw_curved(px,text,x0,x1,center,opts,fill,outline):
    ms,caph=lines_mask([text],x1-x0,99,opts)
    m,ct,ch=ms[0]
    h,w=m.shape; X=x0+((x1-x0)-w)//2
    canvas=np.zeros((h+40,w),bool); canvas[20:20+h]=m
    shifted=np.zeros_like(canvas)
    mid=center(X+w/2)
    used=canvas.any(0); j=0                                # shift whole letters (column runs), not single columns
    while j<w:
        if not used[j]: j+=1; continue
        k=j
        while k<w and used[k]: k+=1
        dy=int(round(center(X+(j+k)/2)-mid))
        shifted[:,j:k]=np.roll(canvas[:,j:k],dy,0); j=k
    top=int(round(mid-ch/2))-ct-20
    fr=[fill[min(len(fill)-1,max(0,int((r-20-ct)*len(fill)/max(1,ch))))] for r in range(shifted.shape[0])]
    render(px,shifted,X,top,fr,[(outline,1)])

def run(G):
    px=G.px(0); pal=G.pal(0)
    center=_curve(px,pal,LOWER['x0'],LOWER['x1'],LOWER['y0']+1,LOWER['y1'])
    for B in (UPPER,LOWER): erase(px,pal,B['x0'],B['x1'],B['y0'],B['y1'])
    x0,y0,x1,y1=UPPER['text']
    text_block(px,[UPPER['line']],(x0,y0,x1,y1),[('dvc',s,0) for s in (12,11,10,9)],FILL,rings=[(OUTLINE,1)])
    draw_curved(px,LOWER['line'],52,239,center,[('dvc',s,0) for s in (12,11,10,9)],FILL,OUTLINE)
    G.put(0,px)
