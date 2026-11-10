import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys;sys.path.insert(0,_ROOT+'/tools')
from table import load
T=load()
def dec(b):
    out='';i=0
    while i<len(b):
        x=b[i]
        if 0xf1<=x<=0xf9: out+=T.get((x-0xf1)*256+b[i+1],'[%03x]'%((x-0xf1)*256+b[i+1])); i+=2
        elif x==0xfd: out+='/'; i+=1
        elif x==0: out+='_'; i+=1
        else: out+='<%02x>'%x; i+=1
    return out
def messages(e):
    res=[];i=0
    while i<len(e)-4:
        if e[i]==0x78 and e[i+1]==0x13 and e[i+3]==0 and (0xf1<=e[i+4]<=0xf9 or e[i+4]<=0x4a or e[i+4]==0xfd):
            s=i+4; j=s
            while e[j]!=0xff:
                j+= 2 if 0xf1<=e[j]<=0xf9 else 1
            res.append((i,s,j,e[i+2])); i=j+1
        elif e[i]==0x78 and e[i+1]==0xa0 and 0xf1<=e[i+2]<=0xf9:
            s=i+2; j=s
            while e[j]!=0xff: j+= 2 if 0xf1<=e[j]<=0xf9 else 1
            res.append((i,s,j,'menu')); i=j+1
        else: i+=1
    return res
