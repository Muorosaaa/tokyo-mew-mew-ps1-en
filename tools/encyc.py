import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import sys,json
sys.path.insert(0,_ROOT+'/tools'); sys.path.insert(0,_ROOT+'/tr')
from pxfit import eng_w
from encode import encode
def wrap(text,lim):
    out=[]
    for para in text.split('\n'):
        if para=='': out.append(''); continue
        lead=len(para)-len(para.lstrip(' ')); words=para.split(' '); cur=''
        for w in words:
            t=(cur+' '+w) if cur else w
            if eng_w(t)<=lim or not cur: cur=t
            else: out.append(cur); cur=w
        out.append(cur)
    return '\n'.join(out)
def build():
    from guide_en import G
    from animal_en import A
    TR={}; iss=[]
    U=json.load(open(_ROOT+'/data/guide.json'))
    for i,t in G.items():
        j,w,n=U[i]
        if 208<=i<=231: lim=34.0
        elif n>1: lim=26.1
        elif 180<=i<=207: lim=28.6
        else: lim=max(w,18.85)
        e=wrap(t,lim) if (n>1 or 208<=i<=231) else t
        TR[j]=e
        for ln in e.split('\n'):
            if eng_w(ln)>lim+0.01: iss.append(('G',i,ln))
        if n==1 and not 208<=i<=231 and '\n' in e: iss.append(('G',i,'multiline'))
    U=json.load(open(_ROOT+'/data/animal.json'))
    for i,t in A.items():
        j,w,n=U[i]
        if n>1:
            lim=34.8; e=wrap(t,lim)
        else:
            lim=17.0; pre=j[0] if j[0]!='<' else None
            e=('<00>' if j[0]=='_' else j[:4])+t
        TR[j]=e
        for ln in e.split('\n'):
            if eng_w(ln)>lim+0.01: iss.append(('A',i,ln))
    for j,e in TR.items(): encode(e)
    return TR,iss
if __name__=='__main__':
    TR,iss=build()
    for x in iss: print(x)
    print(len(TR),'issues',len(iss))
