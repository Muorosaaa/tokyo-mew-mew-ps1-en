import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys;sys.path.insert(0,_ROOT+'/tools');sys.path.insert(0,_ROOT+'/pilot')
from msgs import messages,dec; from encode import encode; from scene0 import TR
d=bytearray(open(_ROOT+'/orig/D_SCE.BIN','rb').read())
BASE=0x400; e=bytes(d[BASE:0x73f4]); M=messages(e)
for k,t in TR.items():
    h,s,j,sp=M[k]; b=encode(t); budget=j-s
    assert len(b)<=budget,(k,len(b),budget)
    from fit import check; assert not check(t),(k,check(t))
    new=b+b'\xff'+b'\x23'*(budget-len(b))
    assert len(new)==budget+1
    d[BASE+s:BASE+j+1]=new
open(_ROOT+'/pilot/D_SCE.BIN','wb').write(d)
orig=open(_ROOT+'/orig/D_SCE.BIN','rb').read()
assert len(d)==len(orig)
diff=[i for i in range(len(d)) if d[i]!=orig[i]]
print('size',len(d),'changed bytes',len(diff),'range',hex(min(diff)),hex(max(diff)))
