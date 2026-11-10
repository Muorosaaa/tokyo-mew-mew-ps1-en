"""Rebuild one script entry with translated messages.
Lines that fit go in place (padded with no-op 0x23). Lines that don't fit are moved
into 'caves' carved from other messages' spare space, reached via op 01 (rel jump).
op 01 lo hi : pc = addr + 1 + s16
"""
import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import struct,sys
sys.path.insert(0,_ROOT+'/tools')
from sdis import textlen
from encode import encode
NOP=0x23
def find_messages(e):
    from table import load
    T=load(); out=[]; i=0
    while i<len(e)-4:
        if e[i]==0x78:
            m=e[i+1]; h=2+(2 if m&1 else 0)
            p=i+h
            if p<len(e) and (0xf0<=e[p]<=0xfa or e[p] in (0,0xfd)) :
                try: n=textlen(e,p)
                except IndexError: n=0
                body=e[p:p+n-1]
                # validate: all 2-byte codes known
                ok=n>1; j=0
                while ok and j<len(body):
                    b=body[j]
                    if 0xf0<=b<=0xfa:
                        ok=((b-0xf1)*256+body[j+1]) in T; j+=2
                    elif b==0xfc: j+= 5 if body[j+2]==0x3c else 3
                    elif 0x4b<=b<0xf0 or b in (0xfb,0xfe): ok=False
                    else: j+=1
                if ok:
                    out.append(dict(at=i,hdr=e[i:p],text_at=p,end=p+n,spk=(e[i+2] if m&1 else None),mode=m)); i=p+n; continue
        i+=1
    return out
def jmp(at,target):
    v=target-(at+1); assert -32768<=v<32768
    return b'\x01'+struct.pack('<h',v)
def rebuild(e,msgs,tr):
    e=bytearray(e)
    over=[]; free=[]
    for k,m in enumerate(msgs):
        if k not in tr:
            continue
        body=m['hdr']+encode(tr[k])+b'\xff'
        slot=m['end']-m['at']
        if len(body)<=slot:
            e[m['at']:m['end']]=body+bytes([NOP])*(slot-len(body))
            if slot-len(body)>=8: free.append([m['at']+len(body),m['end']])
        else:
            over.append((k,body))
    # place overflow
    for k,body in sorted(over,key=lambda x:-len(x[1])):
        m=msgs[k]; need=len(body)+3
        cave=None
        for f in sorted(free,key=lambda f:f[1]-f[0]):
            if f[1]-f[0]>=need+3: cave=f; break
        if cave is None: raise RuntimeError('no space for msg %d (%d bytes)'%(k,need))
        a,b=cave
        e[a:a+3]=jmp(a,b)                 # guard: skip over cave
        c=a+3
        e[c:c+len(body)]=body
        e[c+len(body):c+len(body)+3]=jmp(c+len(body),m['end'])   # back to after original slot
        cave[0]=c+len(body)+3
        # keep the guard valid: the remaining region now starts after our code; next cave adds its own guard
        slot=m['end']-m['at']
        e[m['at']:m['end']]=jmp(m['at'],c)+bytes([NOP])*(slot-3)
    return bytes(e),len(over)
