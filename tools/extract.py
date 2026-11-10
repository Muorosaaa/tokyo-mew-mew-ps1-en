import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,struct
sys.path.insert(0,_ROOT+'/tools')
from table import load
T=load()
def entries(d):
    n=struct.unpack_from('<I',d,0)[0]//4
    offs=[struct.unpack_from('<I',d,i*4)[0] for i in range(n)]
    return offs
def strings(buf):
    """find text strings: maximal runs of (Fx yy | FD) ending in FF"""
    res=[];i=0;n=len(buf)
    while i<n-2:
        if 0xf1<=buf[i]<=0xf9:
            j=i;codes=[]
            while j<n-1 and (0xf1<=buf[j]<=0xf9 or buf[j]==0xfd or (buf[j]==0 and (0xf1<=buf[j+1]<=0xf9 or buf[j+1] in (0,0xfd)))):
                if buf[j]==0xfd: codes.append(-1); j+=1
                elif buf[j]==0: codes.append(-2); j+=1
                else: codes.append((buf[j]-0xf1)*256+buf[j+1]); j+=2
            if j<n and buf[j]==0xff and len([c for c in codes if c>=0])>=1:
                res.append((i,j+1,codes)); i=j+1; continue
        i+=1
    return res
def render(codes):
    return ''.join('\n' if c==-1 else '‹p›' if c==-2 else T.get(c,'[%03x]'%c) for c in codes)
