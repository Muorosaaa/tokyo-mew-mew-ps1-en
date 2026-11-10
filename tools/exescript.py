import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys;sys.path.insert(0,_ROOT+'/tools')
from patcher import find_messages
from msgs import dec
from encode import encode
from fit import check,width
from pxfit import raw_lines_w
def apply(d,a,b,TR):
    d=bytearray(d); seg=bytes(d[a:b]); M=find_messages(seg); n=0; iss=[]
    for m in M:
        j=dec(seg[m['text_at']:m['end']-1])
        if j not in TR: continue
        en=TR[j]; ow=raw_lines_w(seg[m['text_at']:m['end']-1])
        if len(ow)>3:
            e=[]; lim=max(30,max(ow))
            if len(en.split('\n'))>len(ow): e.append('lines')
            e+=['wide %s'%l for l in en.split('\n') if width(l)>lim]
        else: e=check(en)
        body=m['hdr']+encode(en)+b'\xff'; slot=m['end']-m['at']
        if len(body)>slot: e.append('over %d'%(len(body)-slot))
        if e: iss.append((j,en,e)); continue
        d[a+m['at']:a+m['end']]=body+b'\x23'*(slot-len(body)); n+=1
    return bytes(d),n,iss
