import sys,struct,os
d=open(sys.argv[1],'rb').read(); out=sys.argv[2]; os.makedirs(out,exist_ok=True)
first=struct.unpack_from('<I',d,0)[0]; n=first//4
offs=[struct.unpack_from('<I',d,i*4)[0] for i in range(n)]
offs=[o for o in offs]
ents=[]
for i,o in enumerate(offs):
    if o==0 or o>len(d): continue
    nxt=[x for x in offs[i+1:] if x>o]
    end=min(nxt) if nxt else len(d)
    open(f'{out}/{i:03d}.bin','wb').write(d[o:end]); ents.append((i,o,end-o))
print(len(ents),'entries; table slots',n)
for e in ents[:8]: print(e)
