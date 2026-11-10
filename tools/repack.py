import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import struct,sys; sys.path.insert(0,_ROOT+'/tools')
from lz import decompress
from lzopt import compress
def entries(d):
    n=struct.unpack_from('<I',d,0)[0]//4
    return n,[struct.unpack_from('<I',d,4*i)[0]+4*i for i in range(n)]
def raw(d,i):
    n,o=entries(d); s=o[i]; sz=struct.unpack_from('<I',d,s)[0]
    return decompress(d,s+4,sz)[0][:sz]
_cache={}
def comp(data):
    k=hash(data)
    if k not in _cache: 
        b=struct.pack('<I',len(data))+compress(data); _cache[k]=b+b'\0'*(-len(b)%4)
    return _cache[k]
def repack(orig,repl,extra_recompress=()):
    """repl: {index: new decompressed bytes}; entries sharing an original start offset stay shared."""
    n,o=entries(orig); L=len(orig)
    starts=sorted(set(o[:n-1]))
    nxt={s:(starts[k+1] if k+1<len(starts) else o[n-1]) for k,s in enumerate(starts)}
    groups={}
    for i in range(n-1): groups.setdefault(o[i],[]).append(i)
    out=bytearray(o[0]); newstart={}
    for s in starts:
        members=groups[s]
        rs=[i for i in members if i in repl]
        if rs:
            datas=set(repl[i] for i in rs); assert len(datas)==1,('aliased entries differ',members)
            if len(rs)!=len(members):  # some aliases untouched -> require same content
                pass
            b=comp(repl[rs[0]])
        elif any(i in extra_recompress for i in members):
            b=comp(raw(orig,members[0]))
        else: b=orig[s:nxt[s]]
        newstart[s]=len(out); out+=b
    for i in range(n-1): struct.pack_into('<I',out,4*i,newstart[o[i]]-4*i)
    over=len(out)-L
    if over>0: return None,over
    if o[n-1]==L: struct.pack_into('<I',out,4*(n-1),L-4*(n-1)); out+=b'\0'*(L-len(out))
    else:
        struct.pack_into('<I',out,4*(n-1),o[n-1]-4*(n-1)); out+=b'\0'*(L-len(out))
    return bytes(out),over
