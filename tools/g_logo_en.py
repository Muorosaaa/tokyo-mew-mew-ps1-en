"""English title logo (D_SYSTEM 001, 320x236 8bpp, 256 colours, index 0 = transparent).

Source art: data/logo/logo_en_source.png (the user's own English redraw of the logo, 2026-11-15).
It is scaled to fit the original logo's area (bottom at y 160, so the New Game menu and copyright line below
stay clear), given hard edges (the PS1 has no partial transparency), rounded to the PS1's 15-bit colours and
reduced to 32 colours without dithering (dithering would bloat the compressed entry, which must fit back
into its original 13,300-byte slot).
"""
import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys, struct; sys.path.insert(0,_ROOT+'/tools')
import numpy as np
from PIL import Image

SRC=_ROOT+'/data/logo/logo_en_source.png'
BOX=(247,140)          # same width as the original logo (x 32-278); it sits above the menu
COLOURS=32             # flat colours keep the compressed entry inside its slot (255 overflowed it)
CX, BOTTOM = 155, 160  # same horizontal centre and bottom edge as the original

def logo_pixels(src=SRC, box=BOX):
    im=Image.open(src).convert('RGBA')
    im=im.crop(im.getbbox())
    a=np.asarray(im).astype(np.float64)/255.0
    s=min(box[0]/im.width, box[1]/im.height)
    W,H=max(1,round(im.width*s)),max(1,round(im.height*s))
    # premultiplied resize so the transparent surroundings don't darken the edges
    pm=np.dstack([a[...,:3]*a[...,3:4],a[...,3:4]])
    chans=[np.asarray(Image.fromarray(pm[...,k].astype(np.float32),'F').resize((W,H),Image.LANCZOS),np.float64) for k in range(4)]
    chans=[np.clip(c,0,1) for c in chans]
    al=chans[3]; rgb=np.dstack(chans[:3])/np.maximum(al,1e-6)[...,None]
    rgb=np.clip(rgb,0,1)
    opaque=al>=0.5
    rgb5=(np.round(rgb*31)).astype(int)            # PS1 colours are 5 bits per channel
    return rgb5, opaque

def quantize(rgb5, opaque, n=COLOURS):
    pts=rgb5[opaque]
    strip=Image.fromarray((pts*8).astype(np.uint8).reshape(1,-1,3),'RGB')
    q=strip.quantize(colors=n, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal=np.array(q.getpalette()[:3*n],int).reshape(-1,3)
    idx=np.asarray(q).reshape(-1)
    return pal, idx

def bgr555(rgb):
    r,g,b=[int(round(v/8)) for v in rgb]
    r,g,b=[min(31,max(0,v)) for v in (r,g,b)]
    v=r|(g<<5)|(b<<10)
    return v if v else 0x0421                     # 0x0000 would be transparent: use the darkest visible colour

def run(G):
    e=G.E[0]; w,h=e['w'],e['h']                   # 320x236
    rgb5,opaque=logo_pixels()
    H,W=opaque.shape
    pal,idx=quantize(rgb5,opaque)
    px=np.zeros((h,w),np.uint8)
    x0=int(round(CX-W/2)); y0=BOTTOM-H+1
    sub=np.zeros((H,W),np.uint8); sub[opaque]=idx+1   # palette index 0 stays transparent
    px[y0:y0+H,x0:x0+W]=sub
    G.put(0,px)
    # palette: u32 count at 20, then count x u16 BGR555 (entry 0 = 0x0000 transparent)
    p=4+16*len(G.E); cnt,=struct.unpack_from('<I',G.d,p); assert cnt==256
    vals=[0]+[bgr555(c) for c in pal]+[0x0421]*(255-len(pal))
    struct.pack_into('<256H',G.d,p+4,*vals)
    return dict(size=(W,H),pos=(x0,y0),colours=len(pal))

if __name__=='__main__':                          # preview: python tools/g_logo_en.py out.png
    rgb5,opaque=logo_pixels(); pal,idx=quantize(rgb5,opaque)
    out=np.zeros(opaque.shape+(4,),np.uint8); out[opaque,:3]=pal[idx]; out[opaque,3]=255
    Image.fromarray(out,'RGBA').save(sys.argv[1] if len(sys.argv)>1 else 'logo_preview.png'); print(opaque.shape, len(pal))
