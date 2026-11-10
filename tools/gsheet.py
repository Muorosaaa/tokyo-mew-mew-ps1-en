import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,os; sys.path.insert(0,_ROOT+'/tools')
from gfx import *
from PIL import Image,ImageDraw
def render_arc(arc,files=None,maxw=1400,maxh=1800,prefix=None,scale=1,bg=(60,60,90)):
    items=[]
    for f in files or sorted(os.listdir(_ROOT+'/dec/'+arc)):
        d=open(_ROOT+'/dec/%s/%s'%(arc,f),'rb').read()
        try:
            m,E=parse(d); pals,_=palettes(d,m,E)
        except Exception: continue
        if not pals: continue
        for e in E:
            if e['w']==0 or e['h']==0 or e['w']>1024 or e['h']>512: continue
            try: r=image(d,m,e,pals)
            except Exception: continue
            if r is None: continue
            im=Image.fromarray(r[1],'RGBA')
            if scale!=1: im=im.resize((im.width*scale,im.height*scale),Image.NEAREST)
            items.append(('%s:%d'%(f[:3],e['i']),im))
    sheets=[];x=y=rowh=0;cur=Image.new('RGB',(maxw,maxh),bg);dr=ImageDraw.Draw(cur)
    for lab,im in items:
        if im.width+4>maxw: im=im.resize((maxw-4,int(im.height*(maxw-4)/im.width)))
        if x+im.width+4>maxw: x=0;y+=rowh+12;rowh=0
        if y+im.height+12>maxh:
            sheets.append(cur);cur=Image.new('RGB',(maxw,maxh),bg);dr=ImageDraw.Draw(cur);x=y=rowh=0
        dr.text((x,y),lab,fill=(255,255,0)); cur.paste(im,(x,y+10),im)
        x+=max(im.width,40)+6; rowh=max(rowh,im.height)
    sheets.append(cur.crop((0,0,maxw,min(maxh,y+rowh+14))))
    out=[]
    for k,s in enumerate(sheets):
        p=_ROOT+'/gfxout/%s_%02d.png'%(prefix or arc,k); s.save(p); out.append(p)
    return out
if __name__=='__main__':
    print(render_arc(sys.argv[1]))
