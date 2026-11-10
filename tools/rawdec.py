import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys;sys.path.insert(0,_ROOT+'/tools')
from table import load
T=load()
def dec(b):
    o='';i=0
    while i<len(b):
        x=b[i]
        if 0xf0<=x<=0xfa and i+1<len(b): o+=T.get((x-0xf1)*256+b[i+1],'[%03x]'%((x-0xf1)*256+b[i+1])); i+=2
        elif x==0xfc:
            n=5 if b[i+2]==0x3c else 3; o+='{'+b[i:i+n].hex()+'}'; i+=n
        elif x==0xfd: o+='/'; i+=1
        elif x==0: o+='_'; i+=1
        else: o+='<%02x>'%x; i+=1
    return o
