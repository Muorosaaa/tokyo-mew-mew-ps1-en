"""Greedy LZ encoder that never lets output run further ahead of input than `maxlead` bytes
(the game appears to decompress effect data in place)."""
import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0,_ROOT+'/tools')
from lzc import W
def lead_profile(d,pos,size):
    """max(out - consumed) while decoding an original stream starting at pos"""
    start=pos; out=0; flags=0; cnt=0x80; best=0
    def bit():
        nonlocal flags,cnt,pos
        cnt<<=1
        if cnt&0x100: cnt=1; flags=d[pos]; pos+=1
        flags<<=1; return 1 if flags&0x100 else 0
    while True:
        if bit(): pos+=1; out+=1
        elif bit():
            w=(d[pos]<<8)|d[pos+1]; pos+=2; k=w&7
            if k==0:
                k=d[pos]; pos+=1
                if k==0: break
                k+=1
            else: k+=2
            out+=k
        else:
            k=(bit()<<1|bit())+2; pos+=1; out+=k
        best=max(best,out-(pos-start))
    return best
def compress(data,maxlead):
    n=len(data); w=W(); p=0; head={}; prev=[-1]*n
    def ins(q):
        if q+2<n: k=data[q:q+3]; prev[q]=head.get(k,-1); head[k]=q
    def best(p):
        bl=bo=0
        if p+2<n:
            q=head.get(data[p:p+3],-1); t=0
            while q>=0 and p-q<=8191 and t<64:
                l=3; mx=min(255,n-p)
                while l<mx and data[q+l]==data[p+l]: l+=1
                if l>bl: bl,bo=l,p-q
                q=prev[q]; t+=1
        if bl<3 and p+1<n:
            for q in range(p-1,max(-1,p-256),-1):
                if data[q]==data[p] and data[q+1]==data[p+1]: bl,bo=2,p-q; break
        return bl,bo
    while p<n:
        l,o=best(p)
        if l>=2:
            cost=2 if (o<=255 and l<=5) else (2 if l<=9 else 3)
            if o<=255 and l<=5: cost=1
            # lead after this token must stay within limit (bytes in so far ~ len(w.out)+cost)
            allowed=maxlead+len(w.out)+cost-p
            if allowed<l: l=min(l,allowed)
            if l>=3 or (l==2 and o<=255): pass
            else: l=0
        if l>=2 and o<=255 and l<=5:
            w.bit(0);w.bit(0);c=l-2;w.bit(c>>1);w.bit(c&1);w.byte(0x100-o)
        elif l>=3:
            v=(0x2000-o)<<3; w.bit(0);w.bit(1)
            if l<=9: v|=l-2; w.byte(v>>8); w.byte(v&255)
            else: w.byte(v>>8); w.byte(v&255); w.byte(l-1)
        else:
            w.bit(1); w.byte(data[p]); ins(p); p+=1; continue
        for k in range(l): ins(p+k)
        p+=l
    w.bit(0); w.bit(1); w.byte(0); w.byte(0); w.byte(0)
    return bytes(w.out)
