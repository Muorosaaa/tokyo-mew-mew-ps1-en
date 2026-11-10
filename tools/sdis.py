import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import struct,json
L=json.load(open(_ROOT+'/data/oplen.json'))
JUMPS={0x01:(1,2),0x02:(1,4),0x03:(1,2),0x04:(1,4),0x07:(2,2),0x14:(1,2),0x15:(1,2),0xc7:(2,2)}
def textlen(e,p):
    i=p
    while True:
        b=e[i]
        if b==0xff: return i+1-p
        if 0xf0<=b<=0xfa: i+=2
        elif b==0xfc: i+= 5 if e[i+2]==0x3c else 3
        else: i+=1
SUB={0x40:{0:4,1:9,5:4,6:6,8:4,9:4,0xa:3,0xd:3,0x11:3,0x1a:3,0x1b:3,0x1c:6,0x1d:7,0x1e:4,0x20:10},
     0x43:{4:3,5:8,7:9,8:3,9:6,0xa:6},
     0x44:{0:5,1:34,4:10,7:6,0xa:3,0xb:4}}
def ilen(e,a):
    op=e[a]
    if op in SUB: return SUB[op].get(e[a+1],2)
    if op==0x78:
        m=e[a+1]; n=2+(2 if m&1 else 0)
        return n+textlen(e,a+n)
    n=L[op]
    if n==0: raise ValueError('unknown op %02x at %x'%(op,a))
    return n
def entry_bounds(d):
    offs=[struct.unpack_from('<I',d,i*4)[0] for i in range(256)]
    st=[offs[i]+4*i for i in range(256)]
    return [(st[i], st[i+1] if i<255 else len(d)) for i in range(256)]
def header(e):
    # self-relative u16 table; first entry gives header size (absent in some entries)
    v=struct.unpack_from('<H',e,0)[0]
    if v==0 or v%2 or v>=len(e) or v>0x400: return [],0
    n=v//2
    return [2*k+struct.unpack_from('<H',e,2*k)[0] for k in range(n)], n*2
def sweep(e):
    hdr,hs=header(e); a=hs; ins=[]
    while a<len(e):
        n=ilen(e,a); ins.append((a,n)); a+=n
    return hdr,ins,a
