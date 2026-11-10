import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,json,importlib;sys.path.insert(0,_ROOT+'/tools');sys.path.insert(0,_ROOT+'/tr')
from encode import encode
from fit import check
def run(mod,todofile):
    L=json.load(open(todofile)); T=importlib.import_module(mod).T; bad=0
    for i,en in T.items():
        j,slot,spk,w=L[i]; e=check(en)
        try:
            n=len(encode(en))
            if n>slot: e.append('over %d'%(n-slot))
        except Exception as x: e.append(str(x))
        if e: bad+=1; print(i,slot,e,repr(en),'|',j)
    print('issues',bad,'of',len(T))
if __name__=='__main__': run(sys.argv[1],sys.argv[2])
