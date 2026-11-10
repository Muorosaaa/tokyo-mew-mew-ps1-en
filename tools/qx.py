import struct
def parse(d):
    magic,cnt=struct.unpack_from('<HH',d,0)
    ents=[]
    for i in range(cnt):
        off,a,w,h,z=struct.unpack_from('<IIHHI',d,4+i*16)
        ents.append(dict(off=off,a=a,w=w,h=h,z=z))
    return magic,ents
