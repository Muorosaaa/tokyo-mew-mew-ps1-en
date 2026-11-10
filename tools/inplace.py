import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import struct,sys; sys.path.insert(0,_ROOT+'/tools')
import repack
EXACT=True   # set False to reproduce builds made before 2026-11-09
def inplace(orig,repl,hdr=None,leadlimit=False):
    """write recompressed entries at their ORIGINAL offsets (no entry moves). returns (bytes, report)"""
    n,o=repack.entries(orig); out=bytearray(orig); rep=[]
    starts=sorted(set(o))
    for i,data in repl.items():
        s=o[i]; nxt=min(x for x in starts if x>s)
        slot=nxt-s
        from lzopt import compress
        if leadlimit:
            import lzlead
            ml=lzlead.lead_profile(orig,s+4,0)
            ok=None
            for tol in (0,2,4,6):
                for m in range(-8,64):
                    c=lzlead.compress(data,ml-m)
                    if lzlead.lead_profile(c,0,0)<=ml+tol and 4+len(c)<=slot: ok=c; break
                if ok and tol and EXACT:
                    # 2026-11-09: prefer an exact-lead stream from the optimal packer over a greedy one that overshoots
                    import lzopt2
                    c2=lzopt2.compress_lead(data,ml,slot)
                    if c2 is not None: ok=c2; tol=0
                if ok: rep.append(('tol',i,tol)); break
            if ok is None:
                # greedy packer failed: optimal parse topped up to the original's lead (lzopt2, 2026-11-09).
                # Only used here, so entries that already fit keep their exact old streams.
                import lzopt2
                for tol in (0,2,4,6):
                    ok=lzopt2.compress_lead(data,ml+tol,slot)
                    if ok is not None: rep.append(('opt',i,tol)); break
            if ok is None:
                rep.append(('SKIPPED',i,0)); continue
            c=ok
            pass
        else: c=compress(data)
        b=struct.pack('<I',hdr[i] if hdr else len(data))+c; b+=b'\0'*(-len(b)%4)
        rep.append((i,slot,len(b)))
        if len(b)>slot: raise ValueError('entry %d too big: %d > slot %d'%(i,len(b),slot))
        out[s:s+len(b)]=b; out[s+len(b):nxt]=b'\0'*(slot-len(b))
    return bytes(out),rep
