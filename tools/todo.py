import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,json;sys.path.insert(0,_ROOT+'/tools')
from sdis import entry_bounds
from patcher import find_messages
from msgs import dec
def todo(entries,MEM):
    d=open(_ROOT+'/orig/D_SCE.BIN','rb').read(); B=entry_bounds(d); out={}
    for n in entries:
        s,t=B[n]
        if t-s<8: continue
        for k,m in enumerate(find_messages(d[s:t])):
            j=dec(d[s+m['text_at']:s+m['end']-1])
            if j in MEM: continue
            slot=m['end']-m['at']-len(m['hdr'])-1
            if j not in out: out[j]=dict(slot=slot,spk=m['spk'],where=[(n,k)])
            else: out[j]['slot']=min(out[j]['slot'],slot); out[j]['where'].append((n,k))
    return out
