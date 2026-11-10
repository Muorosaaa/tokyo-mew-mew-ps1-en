"""Compressor for the game's LZ format (inverse of lz.decompress)."""
class W:
    def __init__(s): s.out=bytearray(); s.fpos=None; s.nb=8
    def bit(s,b):
        if s.nb==8: s.fpos=len(s.out); s.out.append(0); s.nb=0
        if b: s.out[s.fpos]|=0x80>>s.nb
        s.nb+=1
    def byte(s,b): s.out.append(b)
def compress(data):
    n=len(data); w=W(); i=0
    head={}; prev=[-1]*n
    def ins(p):
        if p+2<n:
            k=data[p:p+3]; prev[p]=head.get(k,-1); head[k]=p
    def best(p):
        bl=0; bo=0
        if p+1<n:
            # short 2-byte matches within 256
            for q in range(p-1,max(-1,p-256),-1):
                if data[q]==data[p] and data[q+1]==data[p+1]:
                    l=2
                    while l<5 and p+l<n and data[q+l]==data[p+l]: l+=1
                    if l>bl: bl,bo=l,p-q
                    if l==5: break
        if p+2<n:
            q=head.get(data[p:p+3],-1); tries=0
            while q>=0 and p-q<=8192 and tries<256:
                l=3; mx=min(256,n-p)
                while l<mx and data[q+l]==data[p+l]: l+=1
                if l>bl: bl,bo=l,p-q
                if l==mx: break
                q=prev[q]; tries+=1
        if bl>=2 and bl<=5 and bo>256 and bl<3: bl=0
        return bl,bo
    while i<n:
        l,o=best(i)
        if l>=2:
            l2,o2=best(i+1) if i+1<n else (0,0)
            if l2>l+1:
                w.bit(1); w.byte(data[i]); ins(i); i+=1; continue
        if l>=2 and o<=256 and l<=5:
            w.bit(0); w.bit(0); c=l-2; w.bit(c>>1); w.bit(c&1); w.byte(0x100-o)
        elif l>=3:
            v=(0x2000-o)<<3
            if l<=9: v|=l-2; w.bit(0); w.bit(1); w.byte(v>>8); w.byte(v&255)
            else: w.bit(0); w.bit(1); w.byte(v>>8); w.byte(v&255); w.byte(l-1)
        else:
            w.bit(1); w.byte(data[i]); ins(i); i+=1; continue
        for k in range(l): ins(i+k)
        i+=l
    return bytes(w.out)
