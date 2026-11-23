"""Overflow report for the EXE message tables (2026-11-23).

The game sizes most boxes for the Japanese text: either a fixed box, or a box written into a script (battle popups,
fixed by tools/boxes.py), or measured from the text (those grow with the English). This lists every string whose
English is wider than its Japanese, in pixels as the game draws them (half-width 8, full-width 12, a {fcffff} value
counted as 24), so each one can be checked against the box it appears in. Strings in boxes that are known to grow
with the text, or that boxes.py resizes, are marked and left out of the count.

    python -X utf8 tools/overflow.py            -> work/overflow.txt
"""
import os as _os, sys; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))); sys.path.insert(0,_ROOT+'/tools')
import boxes
from msgs import dec
from encode import FW
_ONE={0x00:' ',0x40:'.',0x41:',',0x42:':',0x43:';',0x44:"'",0x45:'/',0x46:'=',0x47:'+',0x48:'-',0x4a:'%'}
_FW={0xf1*256+v if v<256 else v:k for k,v in FW.items()}
def show(b):
    """English bytes -> text (codes as {..})"""
    o=[];i=0
    while i<len(b):
        c=b[i]
        if c==0xfd: o.append(' / '); i+=1
        elif c==0xfc: n=5 if b[i+2]==0x3c else 3; o.append('{%s}'%b[i:i+n].hex()); i+=n
        elif c>=0xf0: o.append(_FW.get(c*256+b[i+1],'[%02x%02x]'%(c,b[i+1]))); i+=2
        elif 1<=c<=26: o.append(chr(64+c)); i+=1
        elif 0x1b<=c<=0x34: o.append(chr(c-0x1b+97)); i+=1
        elif 0x36<=c<=0x3f: o.append(chr(c-0x36+48)); i+=1
        else: o.append(_ONE.get(c,'<%02x>'%c)); i+=1
    return ''.join(o)
TABLES={0:('system',208),1:('menu',256),3:('items',256),4:('skills',255),8:('skill descs',192)}
AUTO={(0,i) for i in boxes.POPUPS}|{(0,136),(0,137)}     # popups resized by boxes.py / measured boxes
SCREEN=288                                               # widest text a 320-px screen box can hold
def rows():
    o=open(_ROOT+'/orig/SLPM_871.78','rb').read(); n=open(_ROOT+'/build/SLPM_871.78','rb').read()
    for t,(name,N) in TABLES.items():
        for i in range(N):
            try: jo=boxes.string(o,(t<<8)|i); en=boxes.string(n,(t<<8)|i)
            except Exception: continue
            if jo==en: continue
            jw=boxes.widths(jo); ew=boxes.widths(en)
            yield t,name,i,max(jw),max(ew),len(jw),len(ew),show(en)
def main():
    out=[]; bad=0
    for t,name,i,jw,ew,jl,el,txt in rows():
        flag=''
        limited=t in (1,3,4,8)   # build.py already checks these against their box limits (tools/limits.py)
        if ew>SCREEN: flag='SCREEN'
        elif ew>jw+4 and not limited: flag='wider'
        if el>jl: flag+=' +lines'
        if not flag: continue
        if (t,i) in AUTO: flag='(resized) '+flag
        else: bad+=1
        out.append('%-24s %-12s %3d  jp %3dpx/%d  en %3dpx/%d  %s'%(flag,name,i,jw,jl,ew,el,txt))
    open(_ROOT+'/work/overflow.txt','w',encoding='utf-8').write('\n'.join(out)+'\n')
    print('%d strings wider than their Japanese (not counting resized boxes); see work/overflow.txt'%bad)
if __name__=='__main__': main()
