import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,re,struct,json;sys.path.insert(0,_ROOT+'/tools')
from handscan import body,ins
d=open(_ROOT+'/orig/SLPM_871.78','rb').read()
rd=lambda a:struct.unpack_from('<I',d,a-0x80010000+0x800)[0]
L=json.load(open(_ROOT+'/data/oplen.json'))
H=[int(l.split()[1],16) for l in open(_ROOT+'/ophandlers.txt')]
DISP={0x1b:-0x534c,0x1e:-0x52ec,0x1f:-0x52ac,0x40:-0x526c,0x43:-0x51cc,0x44:-0x518c,0x50:-0x5120,0x51:-0x50ec,0x52:-0x50d8,0x53:-0x50c8,0x54:-0x50b8,0x58:-0x5094,0x59:-0x5068,0x5a:-0x5054,0x5b:-0x5000,0x5f:-0x4ff8,0x62:-0x4f90,0x64:-0x4e10,0x65:-0x4df0,0xb0:-0x4cbc,0xc3:-0x4bf8,0xc4:-0x4bc8,0xc8:-0x4b9c,0xce:-0x4b78,0xe0:-0x4b54,0xe1:-0x4b44}
def classify(h):
    b=body(h,1500); res=[]
    for k,(a,t) in enumerate(b):
        if not (re.search(r'^sw\t\$\w+, 0x48\(',t) and '$sp' not in t): continue
        reg=t.split('\t')[1].split(',')[0]
        if reg=='$zero': res.append(('wait',)); continue
        win=b[max(0,k-16):k]
        reads=sorted(set(int(x,16)-0x54 for x in re.findall(r'lbu\t\$\w+, (0x5[5-9a-f]|0x6[0-9a-f])\(','\n'.join(w for _,w in win))))
        kind=None
        for a2,t2 in reversed(win):
            m=re.match(r'addiu\t%s, %s, (-?0x[0-9a-f]+)$'%(re.escape(reg),re.escape(reg)),t2)
            if m:
                v=int(m.group(1),16)
                prev='\n'.join(w for _,w in win)
                if re.search(r'lw\t%s, 0x48\('%re.escape(reg),prev) and not reads: kind=('add',v)
                elif reads and ('sra' in prev): kind=('jump',min(reads),v,len(reads))
                else: kind=('add?',v,reads)
                break
            m=re.match(r'addiu\t%s, \$zero, (0x[0-9a-f]+)$'%re.escape(reg),t2)
            if m: kind=('set',int(m.group(1),16)); break
        res.append(kind or ('?',reads))
    return res
def tables():
    starts=sorted((0x80100000+v,op) for op,v in DISP.items())
    out={}
    for i,(a,op) in enumerate(starts):
        end=starts[i+1][0] if i+1<len(starts) else a+0x100
        n=(end-a)//4; subs=[]
        for k in range(n):
            h=rd(a+4*k)
            if not (0x80010000<h<0x800f0000): break
            subs.append(h)
        out[op]=subs
    return out
if __name__=='__main__':
    T=tables(); res={}
    for op,subs in sorted(T.items()):
        for k,h in enumerate(subs):
            c=classify(h); res['%02x:%02x'%(op,k)]=c
            print('%02x:%02x len%d'%(op,k,L[op]),hex(h),c)
    json.dump(res,open(_ROOT+'/data/subclass.json','w'))
