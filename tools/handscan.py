import os as _os; _ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
import re,struct,json
ins={};order=[]
for l in open(_ROOT+'/exe.asm'):
    m=re.match(r'\s+([0-9a-f]+):\s+(?:[0-9a-f]{2} ){4}\s*(.*)',l)
    if m:
        a=int(m.group(1),16)+0x80010000; ins[a]=m.group(2).split(' <')[0]
def body(h,maxn=600):
    out=[];a=h
    seen=0
    while a in ins and len(out)<maxn:
        out.append((a,ins[a]))
        if ins[a].startswith('jr\t$ra'): 
            seen+=1
            if seen>=1: out.append((a+4,ins.get(a+4,''))); break
        a+=4
    return out
def writes48(h):
    return [ (hex(a),t) for a,t in body(h) if re.search(r'^sw\t\$\w+, 0x48\(',t) or re.search(r'^sh\t\$\w+, 0x4[89]\(',t)]
