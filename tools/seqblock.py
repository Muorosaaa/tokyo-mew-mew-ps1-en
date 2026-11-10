"""Rewrite a contiguous region of FF-terminated strings sequentially, fixing every
self-relative u32 pointer table that points into it (including pointers to start+1)."""
import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import struct,sys
sys.path.insert(0,_ROOT+'/tools')
from exeblock import strend
from rawdec import dec
from encode import encode
def strings(d,lo,hi):
    p=lo; out=[]
    while p<hi:
        q=strend(d,p); out.append((p,bytes(d[p:q-1]))); p=q
    return out
def apply(d,lo,hi,tables,TR):
    d=bytearray(d); S=strings(d,lo,hi); starts=[p for p,_ in S]
    import bisect
    ptrs=[]
    for T,N in tables:
        for i in range(N):
            a=T+4*i; t=a+struct.unpack_from('<I',d,a)[0]
            k=bisect.bisect_right(starts,t)-1; ptrs.append((a,k,t-starts[k]))
    out=bytearray(); newstart=[]; n=0
    for p,r in S:
        newstart.append(lo+len(out))
        j=dec(r)
        if j in TR:
            b=encode(TR[j]); n+=1
        else: b=r
        out+=b+b'\xff'
    assert len(out)<=hi-lo,('region overflow',len(out)-(hi-lo))
    for a,k,o in ptrs:
        if o:
            j=dec(S[k][1]); 
            if j in TR: assert encode(TR[j])[:o]==S[k][1][:o],('prefix changed',j)
        struct.pack_into('<I',d,a,newstart[k]+o-a)
    d[lo:lo+len(out)]=out; d[lo+len(out):hi]=b'\xff'*(hi-lo-len(out))
    return bytes(d),n,hi-lo-len(out)
