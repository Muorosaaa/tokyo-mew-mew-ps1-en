import sys,struct,os; sys.path.insert(0,os.path.dirname(__file__))
from lz import decompress
def unpack(path,outdir):
    d=open(path,'rb').read(); os.makedirs(outdir,exist_ok=True)
    n=struct.unpack_from('<I',d,0)[0]//4
    offs=[struct.unpack_from('<I',d,i*4)[0] for i in range(n)]
    good=0;fail=[]
    for i,o in enumerate(offs):
        if not 0<o<len(d): continue
        done=False
        for s in [o+4*i+k for k in (0,-4,4,-8,8)]:
            if not 0<=s<len(d)-4: continue
            sz=struct.unpack_from('<I',d,s)[0]
            if not 0<sz<0x400000: continue
            try:
                out,p=decompress(d,s+4,sz)
                if len(out)>=sz:
                    open(f'{outdir}/{i:03d}.bin','wb').write(out[:sz]); good+=1; done=True; break
            except Exception: pass
        if not done: fail.append(i)
    return len(offs),good,fail
if __name__=='__main__':
    t,g,f=unpack(sys.argv[1],sys.argv[2]); print(sys.argv[1],t,g,'fail',f[:20],len(f))
