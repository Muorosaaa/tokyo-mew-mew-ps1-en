import struct,numpy as np
def bgr(c):
    r=(c&31)<<3; g=((c>>5)&31)<<3; b=((c>>10)&31)<<3
    return (r,g,b,0 if c==0 else 255)
def parse(d):
    m,c=struct.unpack_from('<HH',d,0)
    E=[]
    for i in range(c):
        off,=struct.unpack_from('<I',d,4+16*i); a=d[8+16*i:12+16*i]
        w,h,x,y=struct.unpack_from('<HHHH',d,12+16*i)
        E.append(dict(i=i,off=off,a=a,w=w,h=h,x=x,y=y))
    return m,E
def palettes(d,m,E):
    p=4+16*len(E)
    if m&0xff==0x71:
        n,=struct.unpack_from('<I',d,p); p+=4
        return [[bgr(struct.unpack_from('<H',d,p+2*(16*k+j))[0]) for j in range(16)] for k in range(n//16)],p
    if m&0xff==0x51:
        n,=struct.unpack_from('<I',d,p); p+=4
        return [[bgr(struct.unpack_from('<H',d,p+2*j)[0]) for j in range(n)]],p
    return None,p
def image(d,m,e,pals):
    w,h,o=e['w'],e['h'],e['off']
    if m&0xff==0x71:
        a=np.frombuffer(d[o:o+w*h//2],np.uint8)
        if a.size<w*h//2: return None
        px=np.stack([a&15,a>>4],1).reshape(h,w)
        pal=pals[e['a'][0]] if e['a'][0]<len(pals) else pals[0]
    else:
        a=np.frombuffer(d[o:o+w*h],np.uint8)
        if a.size<w*h: return None
        px=a.reshape(h,w); pal=pals[0]
    lut=np.array(pal+[(0,0,0,0)]*(256-len(pal)),np.uint8)
    return px,lut[px]
