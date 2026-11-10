import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,collections;sys.path.insert(0,_ROOT+'/tools')
import importlib,sdis;importlib.reload(sdis)
from sdis import *
d=open(_ROOT+'/orig/D_SCE.BIN','rb').read()
B=entry_bounds(d)
fails=collections.Counter(); ok=0; ex={}
for k,(s,t) in enumerate(B):
    e=d[s:t]
    if len(e)<8: continue
    hdr,hs=header(e); a=hs; trail=[]
    try:
        while a<len(e):
            n=ilen(e,a); trail.append((a,n)); a+=n
        starts={x for x,_ in trail}
        bad=[h for h in hdr if h not in starts and h<len(e)]
        if a!=len(e) or bad:
            fails['misalign']+=1; ex.setdefault('mis',[]).append(k)
        else: ok+=1
    except Exception as x:
        prev=trail[-4:]
        key='%02x'%e[a] + (':%02x'%e[a+1] if e[a] in (0x40,0x43,0x44) else '')
        fails[key]+=1; ex.setdefault(key,(k,hex(a),[(hex(p),e[p:p+n].hex(' ')) for p,n in prev],e[a:a+16].hex(' ')))
print('ok',ok,'of',sum(1 for s,t in B if t-s>=8)); print(fails.most_common(12))
for k,v in list(ex.items())[:4]: print(k,v)
