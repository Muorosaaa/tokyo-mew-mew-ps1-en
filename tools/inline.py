import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys;sys.path.insert(0,_ROOT+'/tools')
from rawdec import dec
def spans(d,a,b):
    """text spans: start at first text byte after an FF/non-text, end at terminating FF (stepping over fc operands)"""
    out=[];i=a
    while i<b:
        if 0xf0<=d[i]<=0xfa and (i==a or not (0xf0<=d[i-2]<=0xfa)):
            s=i
            # extend back over immediately preceding fc codes / fd / 00 / '　'
            j=i
            while True:
                if j-3>=a and d[j-3]==0xfc: j-=3; continue
                break
            s=j; k=i
            while k<b:
                x=d[k]
                if x==0xff: break
                if 0xf0<=x<=0xfa: k+=2
                elif x==0xfc: k+=3
                elif x in (0xfd,0xfe,0x00) or x<0x4b: k+=1
                else: k=-1; break
            if k>0 and k<b and d[k]==0xff:
                out.append((s,k)); i=k+1; continue
        i+=1
    return out
