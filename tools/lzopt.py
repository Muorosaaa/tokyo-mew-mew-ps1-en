"""Optimal-parse compressor for the game's LZ format."""
import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0,_ROOT+'/tools')
from lzc import W
def compress(data,tries=48):
    n=len(data)
    # candidate matches per position
    head2={}; prev2=[-1]*n; head3={}; prev3=[-1]*n
    cands=[None]*n
    for p in range(n):
        c=[]
        if p+1<n:
            q=head2.get(data[p:p+2],-1); t=0
            while q>=0 and p-q<=255 and t<16:
                l=2
                while l<5 and p+l<n and data[q+l]==data[p+l]: l+=1
                c.append((p-q,l,'s')); q=prev2[q]; t+=1
        if p+2<n:
            q=head3.get(data[p:p+3],-1); t=0; bestl=0
            mx=min(256,n-p)
            while q>=0 and p-q<=8191 and t<tries:
                l=3
                while l<mx and data[q+l]==data[p+l]: l+=1
                if l>bestl: c.append((p-q,l,'l')); bestl=l
                if l==mx: break
                q=prev3[q]; t+=1
        cands[p]=c
        if p+1<n: k=data[p:p+2]; prev2[p]=head2.get(k,-1); head2[k]=p
        if p+2<n: k=data[p:p+3]; prev3[p]=head3.get(k,-1); head3[k]=p
    INF=1<<60; cost=[INF]*(n+1); cost[n]=0; ch=[None]*n
    for p in range(n-1,-1,-1):
        bc=9+cost[p+1]; bch=None
        for o,l,kind in cands[p]:
            if kind=='s':
                for k in range(2,l+1):
                    v=12+cost[p+k]
                    if v<bc: bc,bch=v,(o,k,'s')
            else:
                ls=list(range(3,min(l,9)+1))+([l] if l>9 else [])+([k for k in (16,32,64,128) if 9<k<l])
                for k in ls:
                    v=(18 if k<=9 else 26)+cost[p+k]
                    if v<bc: bc,bch=v,(o,k,'l')
        cost[p]=bc; ch[p]=bch
    w=W(); p=0
    while p<n:
        c=ch[p]
        if c is None: w.bit(1); w.byte(data[p]); p+=1; continue
        o,l,kind=c
        if kind=='s':
            w.bit(0); w.bit(0); x=l-2; w.bit(x>>1); w.bit(x&1); w.byte(0x100-o)
        else:
            v=(0x2000-o)<<3
            w.bit(0); w.bit(1)
            if l<=9: v|=l-2; w.byte(v>>8); w.byte(v&255)
            else: w.byte(v>>8); w.byte(v&255); w.byte(l-1)
        p+=l
    w.bit(0); w.bit(1); w.byte(0); w.byte(0); w.byte(0)  # end marker (game's decoder stops here)
    return bytes(w.out)
