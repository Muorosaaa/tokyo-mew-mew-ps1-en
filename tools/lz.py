import struct
def decompress(d, pos=4, limit=None):
    if limit is None: limit=struct.unpack_from('<I',d,0)[0]
    out=bytearray(); flags=0; cnt=0x80
    def bit():
        nonlocal flags,cnt,pos
        cnt<<=1
        if cnt&0x100:
            cnt=1; flags=d[pos]; pos+=1
        flags<<=1
        return 1 if flags&0x100 else 0
    while len(out)<limit:
        if bit():
            out.append(d[pos]); pos+=1; continue
        if bit():
            w=(d[pos]<<8)|d[pos+1]; pos+=2
            off=(w>>3)-0x2000; n=w&7
            if n==0:
                n=d[pos]; pos+=1
                if n==0: break
                n+=1
            else: n+=2
        else:
            n=(bit()<<1|bit())+2
            off=d[pos]-0x100; pos+=1
        s=len(out)+off
        for k in range(n): out.append(out[s+k])
    return bytes(out),pos
