import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import struct,sys
sys.path.insert(0,_ROOT+'/tools')
from encode import encode
def strend(d,p):
    """index just past the FF terminator, stepping over multi-byte codes (fc has operands that may be FF)"""
    i=p
    while True:
        b=d[i]
        if b==0xff: return i+1
        if 0xf0<=b<=0xfa: i+=2
        elif b==0xfc: i+= 5 if d[i+2]==0x3c else 3
        else: i+=1
def read_raw(d,S,N):
    out=[]
    for i in range(N):
        p=S+4*i+struct.unpack_from('<I',d,S+4*i)[0]
        out.append(bytes(d[p:strend(d,p)-1]))
    return out
def extent(d,S,N):
    return max(strend(d,S+4*i+struct.unpack_from('<I',d,S+4*i)[0]) for i in range(N))
def rebuild(d,S,N,tr):
    d=bytearray(d); raw=read_raw(d,S,N); END=extent(d,S,N)
    new=[encode(tr[i]) if i in tr else raw[i] for i in range(N)]
    pool={}; blob=bytearray(); base=S+4*N; offs=[]
    for i,b in enumerate(new):
        if b not in pool: pool[b]=base+len(blob); blob+=b+b'\xff'
        offs.append(pool[b]-(S+4*i))
    assert base+len(blob)<=END,('block overflow',hex(S),base+len(blob)-END)
    for i,o in enumerate(offs): struct.pack_into('<I',d,S+4*i,o)
    d[base:base+len(blob)]=blob; d[base+len(blob):END]=b'\xff'*(END-base-len(blob))
    return bytes(d),END-base-len(blob)
