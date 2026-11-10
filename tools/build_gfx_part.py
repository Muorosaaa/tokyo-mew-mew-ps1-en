"""Rebuild only some entries of an archive and splice them into the existing build/ARC.BIN.
python -X utf8 tools/build_gfx_part.py D_SYSTEM 24 55
Every entry is written in place at its original offset, so entries rebuilt alone can be copied over the full build."""
import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys; sys.path.insert(0,_ROOT+'/tools')
import build_gfx, repack
arc=sys.argv[1]; idx=[int(x) for x in sys.argv[2:]]
J={'D_EFFECT':build_gfx.effect_jobs,'D_SYSTEM':build_gfx.system_jobs,'D_UNIT':build_gfx.unit_jobs}[arc]()
tmp=_ROOT+'/build/_%s.part.BIN'%arc
print(build_gfx.build(arc,{i:J[i] for i in idx},tmp,True))
orig=open(_ROOT+'/orig/%s.BIN'%arc,'rb').read(); part=open(tmp,'rb').read()
full=bytearray(open(_ROOT+'/build/%s.BIN'%arc,'rb').read())
n,o=repack.entries(orig)
diff=[k for k in range(len(orig)) if orig[k]!=part[k]] if False else None
for i in idx:
    a,b=o[i],o[i+1] if i+1<len(o) else len(orig)
    full[a:b]=part[a:b]
# nothing outside the rebuilt entries may differ between part and orig
import numpy as np
P=np.frombuffer(part,np.uint8); O=np.frombuffer(orig,np.uint8); ok=np.ones(len(O),bool)
for i in idx: ok[o[i]:(o[i+1] if i+1<len(o) else len(O))]=False
assert not (P[ok]!=O[ok]).any(), 'rebuild touched other entries'
open(_ROOT+'/build/%s.BIN'%arc,'wb').write(full); _os.remove(tmp); print('spliced',idx)
